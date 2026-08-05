# LabKey Experiment API Support

The Experiment API reads and writes LabKey assay data. Assay data is organized into a three level hierarchy:

- **Batch** — a group of runs imported together. Batch level fields are stored in the assay's batch domain.
- **Run** — a single import of data, e.g. one instrument file. Run level fields are stored in the assay's run domain.
- **Data rows** — the individual result rows of a run, matching the assay's results domain.

Every call is made against a specific assay design, identified by its **assay protocol id** (the `assay_id` argument).
You can find this id in the URL when viewing an assay design in the server UI (e.g.
`.../assay-assayBegin.view?rowId=3315`), or by querying the `assay.AssayList` table with `select_rows`.

The module also exposes the experiment lineage endpoint. See [lineage.md](lineage.md) for that API.

### Additional details from LabKey Documentation:
- [Assay Data](https://www.labkey.org/Documentation/wiki-page.view?name=instrumentData)

## Interfaces

The classes below are imported from `labkey.experiment`. Each constructor accepts keyword arguments, and each
accepts either the Python style name or the server's JSON name (e.g. `data_rows` or `dataRows`), so objects
returned by the server can be modified and passed straight back to a save method.

```python
from labkey.experiment import Batch, Data, Run
```

### `ExpObject`

Base class for all experiment objects. Not used directly.

| Property                   | Type   | Description                                                              |
|----------------------------|--------|--------------------------------------------------------------------------|
| `lsid`                     | `str`  | Life Science Identifier. Assigned by the server.                         |
| `name`                     | `str`  | Display name.                                                            |
| `id` / `row_id`            | `int`  | Primary key. Assigned by the server; set it to update an existing object. |
| `comment`                  | `str`  | Free text comment.                                                       |
| `created` / `modified`     | `str`  | Timestamps. Assigned by the server.                                      |
| `created_by`/`modified_by` | `str`  | User display names. Assigned by the server.                              |
| `properties`               | `dict` | Domain field values, keyed by field name.                                 |

### `Batch`

A group of runs. Extends `ExpObject`.

| Property            | Type        | Description                                                          |
|---------------------|-------------|----------------------------------------------------------------------|
| `runs`              | `List[Run]` | The runs contained in this batch.                                    |
| `batch_protocol_id` | `int`       | Protocol id of the batch. Defaults to `id`.                          |
| `hidden`            | `bool`      | Whether the batch is hidden in the UI. Defaults to `False`.          |

`properties` on a `Batch` holds the batch domain field values.

### `Run`

A single data import. Extends `ExpObject`.

| Property           | Type               | Description                                                                                         |
|--------------------|--------------------|-----------------------------------------------------------------------------------------------------|
| `data_rows`        | `List[dict]`       | Result rows, each keyed by results domain column name.                                              |
| `data_file`        | `TextIO`           | An open file handle to import results from a file instead of `data_rows`. **`import_run()` only.**  |
| `data_inputs`      | `List[Data]`       | Data objects consumed by the run.                                                                   |
| `data_outputs`     | `List[dict]`       | Data objects produced by the run.                                                                   |
| `material_inputs`  | `List[dict]`       | Samples/materials consumed by the run.                                                              |
| `material_outputs` | `List[dict]`       | Samples/materials produced by the run.                                                              |
| `experiments`      | `List[dict]`       | Experiments (run groups) the run belongs to.                                                        |
| `file_path_root`   | `str`              | Server side root path for the run's files.                                                          |
| `protocol`         | `dict`             | The run's protocol.                                                                                 |
| `plate_metadata`   | `dict`             | Well group property values for plate based assays. See [Plate based assays](#plate-based-assays).   |
| `workflow_task`    | `int`              | Row id of a workflow (Sample Manager / LIMS) task to associate the run with.                        |

`properties` on a `Run` holds the run domain field values. Empty values are dropped from the request payload;
the server supplies its own defaults for keys that are absent.

### `RunItem`

Base class for run inputs and outputs. Extends `ExpObject`.

| Property              | Type         | Description                                       |
|-----------------------|--------------|---------------------------------------------------|
| `source_protocol`     | `dict`       | Protocol that produced this item.                 |
| `run`                 | `dict`       | The run this item belongs to.                      |
| `target_applications` | `List[dict]` | Protocol applications that consume this item.      |
| `successor_runs`      | `List[dict]` | Runs derived from this item.                       |
| `cpas_type`           | `str`        | LSID of the item's sample type or data class.      |

### `Data`

A data object (typically a file) used as a run input or output. Extends `RunItem`.

| Property        | Type  | Description                                                        |
|-----------------|-------|--------------------------------------------------------------------|
| `data_type`     | `str` | The data type, e.g. `"Data"`.                                      |
| `data_file_url` | `str` | URL of the underlying file.                                        |
| `pipeline_path` | `str` | Path to the file relative to the container's pipeline root.        |
| `role`          | `str` | The role this data plays in the run.                               |

### Plate based assays

Assays configured for plate support add two requirements to each `Run`:

- `properties["PlateTemplate"]` is required and must be the LSID of the plate template the run uses. For standard
  assays the available templates and their LSIDs can be read with
  `api.query.select_rows("assay.General", "PlateTemplate", columns="Name, Lsid")`.
- `data_rows` must identify the well each result belongs to, using the assay's well location column
  (`WellLocation` in the default plate design).

`plate_metadata` optionally supplies property values for the template's well groups. It is a two level dict:
well group type (`"control"`, `"sample"`, ...) → well group name → a dict of property name/value pairs. The
property names must exist on the corresponding well group domain, and the well group names must match those
defined in the plate template.

```python
run.plate_metadata = {
    "control": {"positive": {"dilution": 0.005}, "negative": {"dilution": 1.0}},
    "sample": {
        "SA01": {"dilution": 1.0, "Barcode": "BC_111", "Concentration": 0.0125},
        "SA02": {"dilution": 2.0, "Barcode": "BC_222"},
    },
}
```

Properties may be omitted per well group; in the example above only `SA01` sets `Concentration`.

## Methods

All methods are available on the `experiment` member of an `APIWrapper` instance.

| Method                                | Returns                 | Description                                                                          |
|---------------------------------------|-------------------------|--------------------------------------------------------------------------------------|
| `load_batch(assay_id, batch_id)`      | `Optional[Batch]`       | Load a batch, its runs, and its run data from the server.                            |
| `save_batch(assay_id, batch)`         | `Optional[Batch]`       | Save one batch and its runs. Returns the saved batch with server assigned ids.       |
| `save_batches(assay_id, batches)`     | `Optional[List[Batch]]` | Save several batches in one request. Returns the saved batches.                      |
| `import_run(assay_id, run)`           | `dict`                  | Import a single run without creating or updating a batch explicitly.                  |
| `lineage(lsids, ...)`                 | `dict`                  | Query the experiment lineage graph. See [lineage.md](lineage.md).                     |

Notes:

- `save_batch()` / `save_batches()` create a batch when `id` is not set, and update the existing batch when it is.
  Every run must be supplied on each save; runs omitted from a saved batch are removed from it.
- `import_run()` is the only method that accepts `Run.data_file`. It always stores the imported results as a file
  on the server, and it is the method to use when associating a run with a `workflow_task`.
- `save_batches()` raises an exception if any element of `batches` is not a `Batch` instance.

### Examples

Every example below uses an `APIWrapper` instance to make its requests. See [api_wrapper.md](api_wrapper.md) for the
full set of `APIWrapper` arguments, including how to configure the container path, context path, SSL, and
authentication.

#### Save and load an assay batch

```python
from labkey.api_wrapper import APIWrapper
from labkey.experiment import Batch, Run

labkey_server = "www.example.com"
container_path = "Tutorials/HIV Study"  # Full project/folder container path
context_path = "labkey"
api = APIWrapper(labkey_server, container_path, context_path)

assay_id = 3315  # provide one from your server

###################
# Save an assay batch
###################
run = Run()
run.name = "python upload"
run.data_rows = [
    {
        # ColumnName: Value
        "SampleId": "Sample 1",
        "TimePoint": "2008/11/02 11:22:33",
        "DoubleData": 4.5,
        "HiddenData": "another data point",
    },
    {
        "SampleId": "Sample 2",
        "TimePoint": "2008/11/02 14:00:01",
        "DoubleData": 3.1,
        "HiddenData": "fozzy bear",
    },
]
run.properties["RunFieldName"] = "Run Field Value"

batch = Batch()
batch.name = "python batch"
batch.runs = [run]
batch.properties["PropertyName"] = "Property Value"

saved_batch = api.experiment.save_batch(assay_id, batch)

###################
# Load an assay batch
###################
run_group = api.experiment.load_batch(assay_id, saved_batch.row_id)

if run_group is not None:
    print("Batch Id: " + str(run_group.id))
    print("Created By: " + run_group.created_by)
    for loaded_run in run_group.runs:
        print("Run: " + loaded_run.name + ", rows: " + str(len(loaded_run.data_rows)))
else:
    print("load_batch: no batch returned")
```

#### Add a run to an existing batch

Load the batch, append a run, and save it back. The existing runs must remain in `batch.runs`.

```python
from labkey.api_wrapper import APIWrapper
from labkey.experiment import Run

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

assay_id = 3315
batch_id = 1234

batch = api.experiment.load_batch(assay_id, batch_id)

new_run = Run(
    name="second upload",
    data_rows=[{"SampleId": "Monkey 4", "DoubleData": 2.7}],
)
batch.runs.append(new_run)

api.experiment.save_batch(assay_id, batch)
```

#### Save multiple batches in one request

```python
from labkey.api_wrapper import APIWrapper
from labkey.experiment import Batch, Run

api = APIWrapper("www.example.com", "Tutorials/HIV Study", "labkey")

assay_id = 3315

batches = [
    Batch(
        name="plate 1",
        runs=[{"name": "plate 1 run", "data_rows": [{"SampleId": "Monkey 1", "DoubleData": 4.5}]}],
    ),
    Batch(
        name="plate 2",
        runs=[{"name": "plate 2 run", "data_rows": [{"SampleId": "Monkey 2", "DoubleData": 3.1}]}],
    ),
]

saved_batches = api.experiment.save_batches(assay_id, batches)

for saved in saved_batches:
    print(saved.name + " -> rowId " + str(saved.row_id))
```

#### Save a batch for a plate based assay

The run supplies the plate template LSID as a run property, locates each result row in a well, and maps property
values onto the template's well groups. See [Plate based assays](#plate-based-assays) for the
`plate_metadata` structure.

```python
from labkey.api_wrapper import APIWrapper
from labkey.experiment import Batch, Run

api = APIWrapper("www.example.com", "Tutorials/assay", "labkey")

assay_id = 310  # a plate enabled assay design on your server

run = Run()
run.name = "python upload"
run.data_rows = [
    {
        # ColumnName: Value
        "ParticipantId": "1234",
        "VisitId": 111,
        "WellLocation": "A1",
    },
    {"ParticipantId": "5678", "VisitId": 222, "WellLocation": "B11"},
    {"ParticipantId": "9123", "VisitId": 333, "WellLocation": "F12"},
]

# Required run property for plate enabled assays: the plate template LSID
run.properties["PlateTemplate"] = (
    "urn:lsid:labkey.com:PlateTemplate.Folder-6:d8bbec7d-34cd-1038-bd67-b3bd777822f8"
)

# Well group properties, keyed by well group type then well group name
run.plate_metadata = {
    "control": {"positive": {"dilution": 0.005}, "negative": {"dilution": 1.0}},
    "sample": {
        "SA01": {"dilution": 1.0, "Barcode": "BC_111", "Concentration": 0.0125},
        "SA02": {"dilution": 2.0, "Barcode": "BC_222"},
        "SA03": {"dilution": 3.0, "Barcode": "BC_333"},
        "SA04": {"dilution": 4.0, "Barcode": "BC_444"},
    },
}

batch = Batch()
batch.name = "python batch"
batch.runs = [run]
batch.properties["PropertyName"] = "Property Value"

saved_batch = api.experiment.save_batch(assay_id, batch)
```

#### Import a run and associate it with a workflow task

Use `import_run()` when you have a single run to import and no batch level properties to set. Passing
`workflow_task` links the resulting run to a Sample Manager or LIMS workflow job task.

```python
from labkey.api_wrapper import APIWrapper
from labkey.experiment import Run

api = APIWrapper("www.example.com", "Biologics")

assay_id = 22858
workflow_task = 50574

rows = [
    {"Sample": 404208, "Sample/Name": "S-97", "Value": "1"},
    {"Sample": 404207, "Sample/Name": "S-96", "Value": "2"},
    {"Sample": 404206, "Sample/Name": "S-95", "Value": "3"},
]

run = Run(name="My Python Run", workflow_task=workflow_task, data_rows=rows)

result = api.experiment.import_run(assay_id, run)
print(result)
```

#### Import a run from a data file

Assign an open file handle to `Run.data_file` instead of supplying `data_rows`. The file must be in a format the
assay design accepts, for example a TSV whose column headers match the results domain.

```python
from labkey.api_wrapper import APIWrapper
from labkey.experiment import Run

api = APIWrapper("www.example.com", "Biologics")

assay_id = 22858

with open("assay_data.tsv", "r") as run_file:
    run = Run(name="My Python File Run", data_file=run_file)
    result = api.experiment.import_run(assay_id, run)

print(result)
```
