from collections import defaultdict

from labkey.api_wrapper import APIWrapper
from labkey.query import QueryFilter

labkey_server = "localhost:8080"
container_path = "Tutorials/HIV Study"  # Full project/folder container path
api = APIWrapper(labkey_server, container_path, use_ssl=False)

###################
# Create a data class domain
###################
simple_molecules_domain = api.domain.create({
    "kind": "DataClass",
    "domainDesign": {
        "name": "SimpleMolecules",
        "fields": [
            {"name": "formula", "label": "Chemical Formula", "rangeURI": "string"},
            {"name": "molarMass", "label": "Molar Mass (g/mol)", "rangeURI": "double"},
        ]
    }
})

api.query.insert_rows("exp.data", "SimpleMolecules", [
    {"name": "Water", "formula": "H20", "molarMass": 18.01528},
    {"name": "Salt", "formula": "NaCl", "molarMass": 58.443}
])

###################
# Create a second data class domain
###################
substances_domain = api.domain.create({
    "kind": "DataClass",
    "domainDesign": {
        "name": "Substances",
        "fields": [
            {"name": "type", "rangeURI": "string"},
            {"name": "fromNature", "rangeURI": "boolean"},
        ]
    }
})

api.query.insert_rows("exp.data", "Substances", [
    {"name": "Ocean Water", "type": "liquid", "fromNature": True, "DataInputs/SimpleMolecules": "Water, Salt"},
    {"name": "Bath Water", "type": "liquid", "fromNature": False, "DataInputs/SimpleMolecules": "Water"}
])

###################
# Create a sample type domain
###################
field_samples_domain = api.domain.create({
    "kind": "SampleSet",
    "domainDesign": {
        "name": "FieldSamples",
        "fields": [
            {"name": "name", "rangeURI": "string"},
            {"name": "receivedDate", "rangeURI": "dateTime"},
            {"name": "volume_mL", "rangeURI": "int"},
        ]
    }
})

api.query.insert_rows("samples", "FieldSamples", [
    {"name": "OC-1", "receivedDate": "05/12/2025", "volume_mL": 400, "DataInputs/Substances": "Ocean Water"},
    {"name": "OC-2", "receivedDate": "05/13/2025", "volume_mL": 600, "DataInputs/Substances": "Ocean Water"},
    {"name": "OC-3", "receivedDate": "05/14/2025", "volume_mL": 800, "DataInputs/Substances": "Ocean Water"},

    {"name": "BW-1", "receivedDate": "05/12/2025", "volume_mL": 400, "DataInputs/Substances": "Bath Water"},
    {"name": "BW-2", "receivedDate": "05/13/2025", "volume_mL": 600, "DataInputs/Substances": "Bath Water"},
    {"name": "BW-3", "receivedDate": "05/14/2025", "volume_mL": 800, "DataInputs/Substances": "Bath Water"},

    {"name": "Mixed-1", "receivedDate": "05/18/2025", "volume_mL": 50, "DataInputs/Substances": "\"Bath Water\", \"Ocean Water\""},
])

###################
# Query the lineage
###################

# Specification for which entity to query
schema_name = "exp.data"
query_name = "Substances"
entity_name = "Ocean Water"

# Fetch the LSID of the "seed" for the lineage request. In this case, we'll query for the "Ocean Water" entity in Substances.
result = api.query.select_rows(schema_name, query_name, columns="Name, LSID", filter_array=[QueryFilter("name", entity_name)])
seed_lsid = result["rows"][0]["LSID"]

# Lineage results includes the following:
# "seed": The LSID of all furnished seed nodes. A string if only a single seed, otherwise, an array of strings.
# "nodes": A dictionary of lineage node objects keyed by each node's LSID. Nodes are linked together by their "parents" and "children" edges.
#
# On each node the following properties allow for traversal of the flattened graph structure.
# "parents": An array of objects representing edges in the graph from nodes that refer to this node.
# "children": An aray of objects representing edges in the graph to nodes to which this node refers.
lineage_result = api.experiment.lineage([seed_lsid], depth=10)

###################
# Traverse the lineage
###################
def traverse_lineage(node_lsid, lineage_result, depth=0, visited=None, nodes_by_depth=None):
    if visited is None:
        visited = set()
    if nodes_by_depth is None:
        nodes_by_depth = defaultdict(set)

    if node_lsid in visited:
        return nodes_by_depth

    visited.add(node_lsid)
    node = lineage_result["nodes"][node_lsid]

    def process_edges(edges, offset):
        new_depth = depth + offset
        for edge in edges:
            related_lsid = edge["lsid"]
            related_node = lineage_result["nodes"][related_lsid]
            nodes_by_depth[new_depth].add(related_node['name'])

            traverse_lineage(related_lsid, lineage_result, new_depth, visited.copy(), nodes_by_depth)

    process_edges(node.get("parents", []), -1)
    process_edges(node.get("children", []), 1)

    return nodes_by_depth


nodes_by_depth = traverse_lineage(seed_lsid, lineage_result)

print("\n===== LINEAGE BY DEPTH =====\n")

# Print parents (negative depths) from furthest to closest
for depth in range(min(nodes_by_depth.keys()), 0):
    if depth in nodes_by_depth:
        print(f"parent (depth = {depth}):")
        for node in sorted(nodes_by_depth[depth]):
            print(f"\t{node}")

seed_node = lineage_result["nodes"][seed_lsid]
print(f"Seed: {seed_node["name"]}")

# Print children (positive depths) from closest to furthest
for depth in range(1, max(nodes_by_depth.keys()) + 1):
    if depth in nodes_by_depth:
        print(f"children (depth = {depth}):")
        for node in sorted(nodes_by_depth[depth]):
            print(f"\t{node}")

###################
# Output:
#
# ===== LINEAGE BY DEPTH =====
#
# parent (depth = -2):
# 	Salt
# 	Water
# parent (depth = -1):
# 	Derive data from Salt, Water
# Seed: Ocean Water
# children (depth = 1):
# 	Derive 3 samples from Ocean Water
# 	Derive sample from Ocean Water, Bath Water
# children (depth = 2):
# 	Mixed-1
# 	OC-1
# 	OC-2
# 	OC-3
###################
