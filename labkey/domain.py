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
from __future__ import unicode_literals
import json

from labkey.utils import ServerContext


def strip_none_values(data, do_strip=True):
    # type: (dict, bool) -> dict
    if do_strip:
        for k in list(data.keys()):
            if data[k] is None:
                del data[k]
    return data


class ConditionalFormat(object):
    def __init__(self, **kwargs):
        self.background_color = kwargs.pop('background_color', kwargs.pop('backgroundColor', None))
        self.bold = kwargs.pop('bold', None)
        self.filter = kwargs.pop('filter', None)
        self.italic = kwargs.pop('italic', None)
        self.strike_through = kwargs.pop('strike_through', kwargs.pop('strikethrough', None))
        self.text_color = kwargs.pop('text_color', kwargs.pop('textColor', None))

    @staticmethod
    def from_data(data):
        return ConditionalFormat(**data)

    def to_json(self):
        data = {
            'backgroundColor': self.background_color,
            'bold': self.bold,
            'filter': self.filter,
            'italic': self.italic,
            'strikethrough': self.strike_through,
            'textColor': self.text_color
        }

        return data


# modeled on org.labkey.api.gwt.client.model.GWTDomain
class Domain(object):
    def __init__(self, **kwargs):
        self.container = kwargs.pop('container', None)
        self.description = kwargs.pop('description', None)
        self.domain_id = kwargs.pop('domain_id', kwargs.pop('domainId', None))
        self.domain_uri = kwargs.pop('domain_uri', kwargs.pop('domainURI', None))
        self.name = kwargs.pop('name', None)
        self.query_name = kwargs.pop('query_name', kwargs.pop('queryName', None))
        self.schema_name = kwargs.pop('schema_name', kwargs.pop('schemaName', None))
        self.template_description = kwargs.pop('template_description', kwargs.pop('templateDescription', None))

        fields = kwargs.pop('fields', [])
        fields_instances = []

        for field in fields:
            fields_instances.append(PropertyDescriptor.from_data(field))

        self.fields = fields_instances

        indices = kwargs.pop('indices', [])
        indices_instances = []

        for index in indices:
            indices_instances.append(FieldIndex.from_data(index))

        self.indices = indices_instances

    @staticmethod
    def from_data(data):
        return Domain(**data)

    def add_field(self, field):
        # type: (self, Union[dict, PropertyDescriptor]) -> Domain
        if isinstance(field, PropertyDescriptor):
            _field = field
        else:
            _field = PropertyDescriptor(**field)

        if _field is not None:
            self.fields.append(_field)

        return self

    def to_json(self, strip_none=True):
        data = {
            'container': self.container,
            'description': self.description,
            'domainId': self.domain_id,
            'domainURI': self.domain_uri,
            'name': self.name,
            'queryName': self.query_name,
            'schemaName': self.schema_name,
            'templateDescription': self.template_description
        }

        json_fields = []
        for field in self.fields:
            json_fields.append(field.to_json())
        data['fields'] = json_fields

        json_indices = []
        for index in self.indices:
            json_indices.append(index.to_json())
        data['indices'] = json_indices

        return strip_none_values(data, strip_none)


# TODO: Determine if this can be used when initializing domain.create
class DomainDefinition(object):
    def __init__(self, **kwargs):
        self.create_domain = kwargs.pop('create_domain', None)
        self.domain_design = kwargs.pop('domain_design', None)
        self.domain_group = kwargs.pop('domain_group', None)
        self.domain_template = kwargs.pop('domain_template', None)
        self.import_data = kwargs.pop('import_data', None)
        self.kind = kwargs.pop('kind', None)
        self.module = kwargs.pop('module', None)
        self.options = kwargs.pop('options', None)


# modeled on org.labkey.api.gwt.client.model.GWTIndex
class FieldIndex(object):
    def __init__(self, **kwargs):
        self.column_names = kwargs.pop('column_names', kwargs.pop('columnNames', None))
        self.unique = kwargs.pop('unique', None)

    @staticmethod
    def from_data(data):
        return FieldIndex(**data)

    def to_json(self, strip_none=True):
        data = {
            'columnNames': self.column_names,
            'unique': self.unique
        }

        return strip_none_values(data, strip_none)


# modeled on org.labkey.api.gwt.client.model.GWTPropertyDescriptor
class PropertyDescriptor(object):
    def __init__(self, **kwargs):
        self.concept_uri = kwargs.pop('concept_uri', kwargs.pop('conceptURI', None))

        formats = kwargs.pop('conditional_formats', kwargs.pop('conditionalFormats', []))
        format_instances = []
        for f in formats:
            format_instances.append(ConditionalFormat.from_data(f))
        self.conditional_formats = format_instances

        self.container = kwargs.pop('container', None)
        self.default_display_value = kwargs.pop('default_display_value', kwargs.pop('defaultDisplayValue', None))
        self.default_scale = kwargs.pop('default_scale', kwargs.pop('defaultScale', None))
        self.default_value = kwargs.pop('default_value', kwargs.pop('defaultValue', None))
        self.default_value_type = kwargs.pop('default_value_type', kwargs.pop('defaultValueType', None))
        self.description = kwargs.pop('description', None)
        self.dimension = kwargs.pop('dimension', None)
        self.disable_editing = kwargs.pop('disable_editing', kwargs.pop('disableEditing', None))
        self.exclude_from_shifting = kwargs.pop('exclude_from_shifting', kwargs.pop('excludeFromShifting', None))
        self.faceting_behavior_type = kwargs.pop('faceting_behavior_type', kwargs.pop('facetingBehaviorType', None))
        self.format = kwargs.pop('format', None)
        self.hidden = kwargs.pop('hidden', None)
        self.import_aliases = kwargs.pop('import_aliases', kwargs.pop('importAliases', None))
        self.label = kwargs.pop('label', None)
        self.lookup_container = kwargs.pop('lookup_container', kwargs.pop('lookupContainer', None))
        self.lookup_description = kwargs.pop('lookup_description', kwargs.pop('lookupDescription', None))
        self.lookup_query = kwargs.pop('lookup_query', kwargs.pop('lookupQuery', None))
        self.lookup_schema = kwargs.pop('lookup_schema', kwargs.pop('lookupSchema', None))
        self.measure = kwargs.pop('measure', None)
        self.mv_enabled = kwargs.pop('mv_enabled', kwargs.pop('mvEnabled', None))
        self.name = kwargs.pop('name', None)
        self.ontology_uri = kwargs.pop('ontology_uri', kwargs.pop('ontologyURI', None))
        self.phi = kwargs.pop('phi', None)
        self.prevent_reordering = kwargs.pop('prevent_reordering', kwargs.pop('preventReordering', None))
        self.property_id = kwargs.pop('property_id', kwargs.pop('propertyId', None))
        self.property_uri = kwargs.pop('property_uri', kwargs.pop('propertyURI', None))

        validators = kwargs.pop('property_validators', kwargs.pop('propertyValidators', []))
        validator_instances = []
        for v in validators:
            validator_instances.append(PropertyValidator.from_data(v))
        self.property_validators = validator_instances

        self.range_uri = kwargs.pop('range_uri', kwargs.pop('rangeURI', None))
        self.recommended_variable = kwargs.pop('recommended_variable', kwargs.pop('recommendedVariable', None))
        self.redacted_text = kwargs.pop('redacted_text', kwargs.pop('redactedText', None))
        self.required = kwargs.pop('required', None)
        self.scale = kwargs.pop('scale', None)
        self.search_terms = kwargs.pop('search_terms', kwargs.pop('searchTerms', None))
        self.semantic_type = kwargs.pop('semantic_type', kwargs.pop('semanticType', None))
        self.set_dimension = kwargs.pop('set_dimension', kwargs.pop('setDimension', None))
        self.set_exclude_from_shifting = kwargs.pop('set_exclude_from_shifting', kwargs.pop('setExcludeFromShifting', None))
        self.set_measure = kwargs.pop('set_measure', kwargs.pop('setMeasure', None))
        self.shown_in_details_view = kwargs.pop('shown_in_details_view', kwargs.pop('shownInDetailsView', None))
        self.shown_in_insert_view = kwargs.pop('shown_in_insert_view', kwargs.pop('shownInInsertView', None))
        self.shown_in_update_view = kwargs.pop('shown_in_update_view', kwargs.pop('shownInUpdateView', None))
        self.type_editable = kwargs.pop('type_editable', kwargs.pop('typeEditable', None))
        self.url = kwargs.pop('url', None)

    @staticmethod
    def from_data(data):
        return PropertyDescriptor(**data)

    def to_json(self, strip_none=True):
        # TODO: Likely only want to include those that are not None
        data = {
            'conceptURI': self.concept_uri,
            'container': self.container,
            'defaultDisplayValue': self.default_display_value,
            'defaultScale': self.default_scale,
            'defaultValue': self.default_value,
            'defaultValueType': self.default_value_type,
            'description': self.description,
            'dimension': self.dimension,
            'disableEditing': self.disable_editing,
            'excludeFromShifting': self.exclude_from_shifting,
            'facetingBehaviorType': self.faceting_behavior_type,
            'format': self.format,
            'hidden': self.hidden,
            'importAliases': self.import_aliases,
            'label': self.label,
            'lookupContainer': self.lookup_container,
            'lookupDescription': self.lookup_description,
            'lookupQuery': self.lookup_query,
            'lookupSchema': self.lookup_schema,
            'measure': self.measure,
            'mvEnabled': self.mv_enabled,
            'name': self.name,
            'ontologyURI': self.ontology_uri,
            'phi': self.phi,
            'preventReordering': self.prevent_reordering,
            'propertyId': self.property_id,
            'propertyURI': self.property_uri,
            'rangeURI': self.range_uri,
            'recommendedVariable': self.recommended_variable,
            'redactedText': self.redacted_text,
            'required': self.required,
            'scale': self.scale,
            'searchTerms': self.search_terms,
            'semanticType': self.semantic_type,
            'setDimension': self.set_dimension,
            'setExcludeFromShifting': self.set_exclude_from_shifting,
            'setMeasure': self.set_measure,
            'shownInDetailsView': self.shown_in_details_view,
            'shownInInsertView': self.shown_in_insert_view,
            'shownInUpdateView': self.shown_in_update_view,
            'typeEditable': self.type_editable,
            'url': self.url
        }

        json_formats = []
        for f in self.conditional_formats:
            json_formats.append(f.to_json())
        data['conditionalFormats'] = json_formats

        json_validators = []
        for p in self.property_validators:
            json_validators.append(p.to_json())
        data['propertyValidators'] = json_validators

        return strip_none_values(data, strip_none)


class PropertyValidator(object):
    def __init__(self, **kwargs):
        self.description = kwargs.pop('description', None)
        self.error_message = kwargs.pop('error_message', kwargs.pop('errorMessage', None))
        self.expression = kwargs.pop('expression', None)
        self.name = kwargs.pop('name', None)
        self.new = kwargs.pop('new', None)
        self.properties = kwargs.pop('properties', None)
        self.row_id = kwargs.pop('row_id', kwargs.pop('rowId', None))
        self.type = kwargs.pop('type', None)

    @staticmethod
    def from_data(data):
        return PropertyValidator(**data)

    def to_json(self, strip_none=True):
        data = {
            'description': self.description,
            'errorMessage': self.error_message,
            'expression': self.expression,
            'name': self.name,
            'new': self.new,
            'properties': self.properties,
            'rowId': self.row_id,
            'type': self.type
        }

        return strip_none_values(data, strip_none)


def create(server_context, domain_definition, container_path=None):
    # type: (ServerContext, dict, str) -> Domain
    """
    Create a domain
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param domain_definition: A domain definition.
    :param container_path: labkey container path if not already set in context
    :return: Domain
    """
    url = server_context.build_url('property', 'createDomain.api', container_path=container_path)

    headers = {
        'Content-Type': 'application/json'
    }

    domain = None

    raw_domain = server_context.make_request(url, json.dumps(domain_definition), headers=headers)

    if raw_domain is not None:
        domain = Domain.from_data(raw_domain)

    return domain


def drop(server_context, schema_name, query_name, container_path=None):
    # type: (ServerContext, str, str, str) -> dict
    """
    Delete a domain
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name of domain to drop
    :param container_path: labkey container path if not already set in context
    :return:
    """
    url = server_context.build_url('property', 'deleteDomain.api', container_path=container_path)

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'schemaName': schema_name,
        'queryName': query_name
    }

    return server_context.make_request(url, json.dumps(payload), headers=headers)


def get(server_context, schema_name, query_name, container_path=None):
    # type: (ServerContext, str, str, str) -> Domain
    """
    Gets a domain design
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name of domain to get
    :param container_path: labkey container path if not already set in context
    :return: Domain
    """
    url = server_context.build_url('property', 'getDomain.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name
    }

    domain = None

    raw_domain = server_context.make_request(url, payload, method='GET')
    if raw_domain is not None:
        domain = Domain.from_data(raw_domain)

    return domain


def infer_fields(server_context, data_file, container_path=None):
    # type: (ServerContext, any) -> List[PropertyDescriptor]
    """
    Infer fields for a domain from a file
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param data_file: the data file from which to determine the fields shape
    :param container_path: labkey container path if not already set in context
    :return:
    """
    url = server_context.build_url('property', 'inferDomain.api', container_path=container_path)

    raw_infer = server_context.make_request(url, None, file_payload={
        'inferfile': data_file
    })

    fields = None
    if 'fields' in raw_infer:
        fields = []
        for f in raw_infer['fields']:
            fields.append(PropertyDescriptor.from_data(f))

    return fields


def save(server_context, schema_name, query_name, domain, container_path=None):
    # type: (ServerContext, str, str, Domain, str) -> None
    """
    Saves the provided domain design
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of domain
    :param query_name: query name of domain
    :param domain: Domain to save
    :param container_path: labkey container path if not already set in context
    :return:
    """
    url = server_context.build_url('property', 'saveDomain.api', container_path=container_path)

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'domainDesign': domain.to_json(),
        'queryName': query_name,
        'schemaName': schema_name
    }

    return server_context.make_request(url, json.dumps(payload), headers=headers)
