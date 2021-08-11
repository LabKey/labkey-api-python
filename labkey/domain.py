#
# Copyright (c) 2018 LabKey Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import functools
from typing import Dict, List, Union, Tuple

from .server_context import ServerContext
from labkey.query import QueryFilter


def strip_none_values(data: dict, do_strip: bool = True):
    if do_strip:
        for k in list(data.keys()):
            if data[k] is None:
                del data[k]
    return data


# modeled on org.labkey.api.gwt.client.model.GWTPropertyDescriptor
class PropertyDescriptor:
    def __init__(self, **kwargs):
        self.concept_uri = kwargs.pop("concept_uri", kwargs.pop("conceptURI", None))

        formats = kwargs.pop("conditional_formats", kwargs.pop("conditionalFormats", []))
        format_instances = []
        for f in formats:
            format_instances.append(ConditionalFormat(**f))
        self.conditional_formats = format_instances

        self.container = kwargs.pop("container", None)
        self.default_display_value = kwargs.pop(
            "default_display_value", kwargs.pop("defaultDisplayValue", None)
        )
        self.default_scale = kwargs.pop("default_scale", kwargs.pop("defaultScale", None))
        self.default_value = kwargs.pop("default_value", kwargs.pop("defaultValue", None))
        self.default_value_type = kwargs.pop(
            "default_value_type", kwargs.pop("defaultValueType", None)
        )
        self.description = kwargs.pop("description", None)
        self.dimension = kwargs.pop("dimension", None)
        self.disable_editing = kwargs.pop("disable_editing", kwargs.pop("disableEditing", None))
        self.exclude_from_shifting = kwargs.pop(
            "exclude_from_shifting", kwargs.pop("excludeFromShifting", None)
        )
        self.faceting_behavior_type = kwargs.pop(
            "faceting_behavior_type", kwargs.pop("facetingBehaviorType", None)
        )
        self.format = kwargs.pop("format", None)
        self.hidden = kwargs.pop("hidden", None)
        self.import_aliases = kwargs.pop("import_aliases", kwargs.pop("importAliases", None))
        self.label = kwargs.pop("label", None)
        self.lookup_container = kwargs.pop("lookup_container", kwargs.pop("lookupContainer", None))
        self.lookup_description = kwargs.pop(
            "lookup_description", kwargs.pop("lookupDescription", None)
        )
        self.lookup_query = kwargs.pop("lookup_query", kwargs.pop("lookupQuery", None))
        self.lookup_schema = kwargs.pop("lookup_schema", kwargs.pop("lookupSchema", None))
        self.measure = kwargs.pop("measure", None)
        self.mv_enabled = kwargs.pop("mv_enabled", kwargs.pop("mvEnabled", None))
        self.name = kwargs.pop("name", None)
        self.ontology_uri = kwargs.pop("ontology_uri", kwargs.pop("ontologyURI", None))
        self.phi = kwargs.pop("phi", None)
        self.prevent_reordering = kwargs.pop(
            "prevent_reordering", kwargs.pop("preventReordering", None)
        )
        self.property_id = kwargs.pop("property_id", kwargs.pop("propertyId", None))
        self.property_uri = kwargs.pop("property_uri", kwargs.pop("propertyURI", None))

        validators = kwargs.pop("property_validators", kwargs.pop("propertyValidators", []))
        validator_instances = []
        for v in validators:
            validator_instances.append(PropertyValidator(**v))
        self.property_validators = validator_instances

        self.range_uri = kwargs.pop("range_uri", kwargs.pop("rangeURI", None))
        self.recommended_variable = kwargs.pop(
            "recommended_variable", kwargs.pop("recommendedVariable", None)
        )
        self.redacted_text = kwargs.pop("redacted_text", kwargs.pop("redactedText", None))
        self.required = kwargs.pop("required", None)
        self.scale = kwargs.pop("scale", None)
        self.search_terms = kwargs.pop("search_terms", kwargs.pop("searchTerms", None))
        self.semantic_type = kwargs.pop("semantic_type", kwargs.pop("semanticType", None))
        self.set_dimension = kwargs.pop("set_dimension", kwargs.pop("setDimension", None))
        self.set_exclude_from_shifting = kwargs.pop(
            "set_exclude_from_shifting", kwargs.pop("setExcludeFromShifting", None)
        )
        self.set_measure = kwargs.pop("set_measure", kwargs.pop("setMeasure", None))
        self.shown_in_details_view = kwargs.pop(
            "shown_in_details_view", kwargs.pop("shownInDetailsView", None)
        )
        self.shown_in_insert_view = kwargs.pop(
            "shown_in_insert_view", kwargs.pop("shownInInsertView", None)
        )
        self.shown_in_update_view = kwargs.pop(
            "shown_in_update_view", kwargs.pop("shownInUpdateView", None)
        )
        self.type_editable = kwargs.pop("type_editable", kwargs.pop("typeEditable", None))
        self.url = kwargs.pop("url", None)

    def to_json(self, strip_none=True):
        # TODO: Likely only want to include those that are not None
        data = {
            "conceptURI": self.concept_uri,
            "container": self.container,
            "defaultDisplayValue": self.default_display_value,
            "defaultScale": self.default_scale,
            "defaultValue": self.default_value,
            "defaultValueType": self.default_value_type,
            "description": self.description,
            "dimension": self.dimension,
            "disableEditing": self.disable_editing,
            "excludeFromShifting": self.exclude_from_shifting,
            "facetingBehaviorType": self.faceting_behavior_type,
            "format": self.format,
            "hidden": self.hidden,
            "importAliases": self.import_aliases,
            "label": self.label,
            "lookupContainer": self.lookup_container,
            "lookupDescription": self.lookup_description,
            "lookupQuery": self.lookup_query,
            "lookupSchema": self.lookup_schema,
            "measure": self.measure,
            "mvEnabled": self.mv_enabled,
            "name": self.name,
            "ontologyURI": self.ontology_uri,
            "phi": self.phi,
            "preventReordering": self.prevent_reordering,
            "propertyId": self.property_id,
            "propertyURI": self.property_uri,
            "rangeURI": self.range_uri,
            "recommendedVariable": self.recommended_variable,
            "redactedText": self.redacted_text,
            "required": self.required,
            "scale": self.scale,
            "searchTerms": self.search_terms,
            "semanticType": self.semantic_type,
            "setDimension": self.set_dimension,
            "setExcludeFromShifting": self.set_exclude_from_shifting,
            "setMeasure": self.set_measure,
            "shownInDetailsView": self.shown_in_details_view,
            "shownInInsertView": self.shown_in_insert_view,
            "shownInUpdateView": self.shown_in_update_view,
            "typeEditable": self.type_editable,
            "url": self.url,
        }

        json_formats = []
        for f in self.conditional_formats:
            json_formats.append(f.to_json())
        data["conditionalFormats"] = json_formats

        json_validators = []
        for p in self.property_validators:
            json_validators.append(p.to_json())
        data["propertyValidators"] = json_validators

        return strip_none_values(data, strip_none)


class PropertyValidator:
    def __init__(self, **kwargs):
        self.description = kwargs.pop("description", None)
        self.error_message = kwargs.pop("error_message", kwargs.pop("errorMessage", None))
        self.expression = kwargs.pop("expression", None)
        self.name = kwargs.pop("name", None)
        self.new = kwargs.pop("new", None)
        self.properties = kwargs.pop("properties", None)
        self.row_id = kwargs.pop("row_id", kwargs.pop("rowId", None))
        self.type = kwargs.pop("type", None)

    def to_json(self, strip_none=True):
        data = {
            "description": self.description,
            "errorMessage": self.error_message,
            "expression": self.expression,
            "name": self.name,
            "new": self.new,
            "properties": self.properties,
            "rowId": self.row_id,
            "type": self.type,
        }

        return strip_none_values(data, strip_none)


class ConditionalFormat:
    def __init__(self, **kwargs):
        self.background_color = kwargs.pop("background_color", kwargs.pop("backgroundColor", None))
        self.bold = kwargs.pop("bold", None)
        self.filter = kwargs.pop("filter", None)
        self.italic = kwargs.pop("italic", None)
        self.strike_through = kwargs.pop("strike_through", kwargs.pop("strikethrough", None))
        self.text_color = kwargs.pop("text_color", kwargs.pop("textColor", None))

    def to_json(self):
        data = {
            "backgroundcolor": self.background_color,
            "bold": self.bold,
            "filter": self.filter,
            "italic": self.italic,
            "strikethrough": self.strike_through,
            "textcolor": self.text_color,
        }

        return data


# modeled on org.labkey.api.gwt.client.model.GWTDomain
class Domain:
    def __init__(self, **kwargs):
        self.container = kwargs.pop("container", None)
        self.description = kwargs.pop("description", None)
        self.domain_id = kwargs.pop("domain_id", kwargs.pop("domainId", None))
        self.domain_uri = kwargs.pop("domain_uri", kwargs.pop("domainURI", None))
        self.name = kwargs.pop("name", None)
        self.query_name = kwargs.pop("query_name", kwargs.pop("queryName", None))
        self.schema_name = kwargs.pop("schema_name", kwargs.pop("schemaName", None))
        self.template_description = kwargs.pop(
            "template_description", kwargs.pop("templateDescription", None)
        )

        fields = kwargs.pop("fields", [])
        fields_instances = []

        for field in fields:
            fields_instances.append(PropertyDescriptor(**field))

        self.fields = fields_instances

        indices = kwargs.pop("indices", [])
        indices_instances = []

        for index in indices:
            indices_instances.append(FieldIndex(**index))

        self.indices = indices_instances

    def add_field(self, field: Union[dict, PropertyDescriptor]):
        if isinstance(field, PropertyDescriptor):
            _field = field
        else:
            _field = PropertyDescriptor(**field)

        if _field is not None:
            self.fields.append(_field)

        return self

    def to_json(self, strip_none=True):
        data = {
            "container": self.container,
            "description": self.description,
            "domainId": self.domain_id,
            "domainURI": self.domain_uri,
            "name": self.name,
            "queryName": self.query_name,
            "schemaName": self.schema_name,
            "templateDescription": self.template_description,
        }

        json_fields = []
        for field in self.fields:
            json_fields.append(field.to_json())
        data["fields"] = json_fields

        json_indices = []
        for index in self.indices:
            json_indices.append(index.to_json())
        data["indices"] = json_indices

        return strip_none_values(data, strip_none)


# TODO: Determine if this can be used when initializing domain.create
class DomainDefinition:
    def __init__(self, **kwargs):
        self.create_domain = kwargs.pop("create_domain", None)
        self.domain_design = kwargs.pop("domain_design", None)
        self.domain_group = kwargs.pop("domain_group", None)
        self.domain_template = kwargs.pop("domain_template", None)
        self.import_data = kwargs.pop("import_data", None)
        self.kind = kwargs.pop("kind", None)
        self.module = kwargs.pop("module", None)
        self.options = kwargs.pop("options", None)


# modeled on org.labkey.api.gwt.client.model.GWTIndex
class FieldIndex:
    def __init__(self, **kwargs):
        self.column_names = kwargs.pop("column_names", kwargs.pop("columnNames", None))
        self.unique = kwargs.pop("unique", None)

    def to_json(self, strip_none=True):
        data = {"columnNames": self.column_names, "unique": self.unique}

        return strip_none_values(data, strip_none)


def conditional_format(
    query_filter: Union[str, QueryFilter, List[QueryFilter]],
    bold: bool = False,
    italic: bool = False,
    strike_through: bool = False,
    text_color: str = "",
    background_color: str = "",
) -> ConditionalFormat:
    """
    Creates a conditional format for use with an existing domain.
    Supports filter URL format as well as QueryFilter filter parameters.
    """
    filter_str = query_filter

    if isinstance(query_filter, QueryFilter):
        filter_str = encode_conditional_format_filter(query_filter)
    elif isinstance(query_filter, list):
        if len(query_filter) > 2:
            raise Exception("Too many QueryFilters given for one conditional format.")

        if not all([isinstance(qf, QueryFilter) for qf in query_filter]):
            raise Exception(
                "Please pass QueryFilter objects when updating a conditional format using a list of filters."
            )

        string_filters = [encode_conditional_format_filter(f) for f in query_filter]
        filter_str = (
            string_filters[0] + "&" + string_filters[1]
            if len(query_filter) == 2
            else string_filters[0]
        )

    return ConditionalFormat(
        background_color=background_color,
        bold=bold,
        filter=filter_str,
        italic=italic,
        strike_through=strike_through,
        text_color=text_color,
    )


def encode_conditional_format_filter(query_filter: QueryFilter) -> str:
    return f"format.column~{query_filter.filter_type}={query_filter.value}"


def __format_conditional_filters(field: dict) -> dict:
    """
    For every conditional format filter that is set as a QueryFilter, translates the given filter into LabKey
    filter URL format.
    """
    if "conditionalFormats" in field:
        for cf in field["conditionalFormats"]:
            if "filter" in cf and isinstance(
                cf["filter"], QueryFilter
            ):  # Supports one QueryFilter without list form
                cf["filter"] = encode_conditional_format_filter(cf["filter"])

            elif "filter" in cf and isinstance(cf["filter"], list):  # Supports list of QueryFilters
                filters = []
                for query_filter in cf["filter"]:
                    filters.append(encode_conditional_format_filter(query_filter))
                if len(filters) > 2:
                    raise Exception("Too many QueryFilters given for one conditional format.")
                cf["filter"] = filters[0] + "&" + filters[1] if len(filters) == 2 else filters[0]

    return field


def create(
    server_context: ServerContext, domain_definition: dict, container_path: str = None
) -> Domain:
    """
    Create a domain
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param domain_definition: A domain definition.
    :param container_path: labkey container path if not already set in context
    :return: Domain
    """
    url = server_context.build_url("property", "createDomain.api", container_path=container_path)
    domain = None

    # domainDesign is not required when creating a domain from a template
    if domain_definition.get("domainDesign", None) is not None:
        domain_fields = domain_definition["domainDesign"]["fields"]
        domain_definition["domainDesign"]["fields"] = list(
            map(__format_conditional_filters, domain_fields)
        )

    raw_domain = server_context.make_request(url, json=domain_definition)

    if raw_domain is not None:
        domain = Domain(**raw_domain)

    return domain


def drop(
    server_context: ServerContext, schema_name: str, query_name: str, container_path: str = None
) -> dict:
    """
    Delete a domain
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name of domain to drop
    :param container_path: labkey container path if not already set in context
    :return:
    """
    url = server_context.build_url("property", "deleteDomain.api", container_path=container_path)
    payload = {"schemaName": schema_name, "queryName": query_name}

    return server_context.make_request(url, json=payload)


def get(
    server_context: ServerContext, schema_name: str, query_name: str, container_path: str = None
) -> Domain:
    """
    Gets a domain design
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name of domain to get
    :param container_path: labkey container path if not already set in context
    :return: Domain
    """
    url = server_context.build_url("property", "getDomain.api", container_path=container_path)
    payload = {"schemaName": schema_name, "queryName": query_name}
    raw_domain = server_context.make_request(url, payload, method="GET")

    if raw_domain is not None:
        return Domain(**raw_domain)

    return None


def get_domain_details(
    server_context: ServerContext,
    schema_name: str = None,
    query_name: str = None,
    domain_id: int = None,
    domain_kind: str = None,
    container_path: str = None,
) -> Tuple[Domain, Dict]:
    """
    Gets a domain design and its associated options.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name of domain to get
    :param domain_id: id of domain to get
    :param domain_kind: domainKind of domain to get
    :param container_path: labkey container path if not already set in context
    :return: Domain, Dict
    """
    url = server_context.build_url(
        "property", "getDomainDetails.api", container_path=container_path
    )
    payload = {
        "schemaName": schema_name,
        "queryName": query_name,
        "domainId": domain_id,
        "domainKind": domain_kind,
    }
    response = server_context.make_request(url, payload, method="GET")
    raw_domain = response.get("domainDesign", None)
    domain = None
    options = response.get("options", None)

    if raw_domain is not None:
        domain = Domain(**raw_domain)

    return domain, options


def infer_fields(
    server_context: ServerContext, data_file: any, container_path: str = None
) -> List[PropertyDescriptor]:
    """
    Infer fields for a domain from a file
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param data_file: the data file from which to determine the fields shape
    :param container_path: labkey container path if not already set in context
    :return:
    """
    url = server_context.build_url("property", "inferDomain.api", container_path=container_path)
    raw_infer = server_context.make_request(url, file_payload={"inferfile": data_file})

    fields = None
    if "fields" in raw_infer:
        fields = []
        for f in raw_infer["fields"]:
            fields.append(PropertyDescriptor(**f))

    return fields


def save(
    server_context: ServerContext,
    schema_name: str,
    query_name: str,
    domain: Domain,
    container_path: str = None,
    options: Dict = None,
) -> any:
    """
    Saves the provided domain design
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of domain
    :param query_name: query name of domain
    :param domain: Domain to save
    :param container_path: labkey container path if not already set in context
    :param options: associated domain options to be saved
    :return:
    """
    url = server_context.build_url("property", "saveDomain.api", container_path=container_path)
    payload = {
        "domainDesign": domain.to_json(),
        "queryName": query_name,
        "schemaName": schema_name,
    }

    if options is not None:
        payload["options"] = options

    return server_context.make_request(url, json=payload)


class DomainWrapper:
    """
    Wrapper for all of the API methods exposed in the domain module. Used by the APIWrapper class.
    """

    def __init__(self, server_context: ServerContext):
        self.server_context = server_context

    @functools.wraps(create)
    def create(self, domain_definition: dict, container_path: str = None):
        return create(self.server_context, domain_definition, container_path)

    @functools.wraps(drop)
    def drop(self, schema_name: str, query_name: str, container_path: str = None):
        return drop(self.server_context, schema_name, query_name, container_path)

    @functools.wraps(get)
    def get(self, schema_name: str, query_name: str, container_path: str = None):
        return get(self.server_context, schema_name, query_name, container_path)

    @functools.wraps(get_domain_details)
    def get_domain_details(
        self,
        schema_name: str = None,
        query_name: str = None,
        domain_id: int = None,
        domain_kind: str = None,
        container_path: str = None,
    ):
        return get_domain_details(
            self.server_context, schema_name, query_name, domain_id, domain_kind, container_path
        )

    @functools.wraps(infer_fields)
    def infer_fields(self, data_file: any, container_path: str = None):
        return infer_fields(self.server_context, data_file, container_path)

    @functools.wraps(save)
    def save(
        self,
        schema_name: str,
        query_name: str,
        domain: Domain,
        container_path: str = None,
        options: Dict = None,
    ):
        return save(self.server_context, schema_name, query_name, domain, container_path, options)
