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


def create(server_context):
    pass


def drop(server_context, schema_name, query_name, container_path=None):
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

    return server_context.make_request(url, payload, headers=headers)


def get(server_context, schema_name, query_name, container_path=None):
    """
    Gets a domain design
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param schema_name: schema of table
    :param query_name: table name of domain to drop
    :param container_path: labkey container path if not already set in context
    :return:
    """
    url = server_context.build_url('property', 'getDomain.api', container_path=container_path)

    payload = {
        'schemaName': schema_name,
        'queryName': query_name
    }

    domain_design = None

    json_body = server_context.make_request(url, payload, method='GET')
    if json_body is not None:
        domain_design = Domain.from_data(json_body)

    return domain_design


def save(server_context):
    pass


class Domain(object):
    def __init__(self, **kwargs):
        self.container = kwargs.pop('container', None)
        self.description = kwargs.pop('description', None)
        self.domain_id = kwargs.pop('domain_id', kwargs.pop('domainId', -1))
        self.domain_uri = kwargs.pop('domain_uri', kwargs.pop('domainURI', None))
        # self.fields
        # self.indices
        self.name = kwargs.pop('name', None)
        self.query_name = kwargs.pop('query_name', kwargs.pop('queryName', None))
        self.schema_name = kwargs.pop('schema_name', kwargs.pop('schemaName', None))
        self.template_description = kwargs.pop('template_description', kwargs.pop('templateDescription', None))

        fields = kwargs.pop('fields', [])
        fields_instances = []

        for field in fields:
            fields_instances.append(PropertyDescriptor.from_data(field))

        self.fields = fields_instances

    @staticmethod
    def from_data(data):
        return Domain(**data)


class PropertyDescriptor(object):
    def __init__(self, **kwargs):
        self.concept_uri = kwargs.pop('concept_uri', kwargs.pop('conceptURI', None))
        # self.conditional_formats
        self.container = kwargs.pop('container', None)
        self.default_display_value = kwargs.pop('default_display_value', kwargs.pop('defaultDisplayValue', None))
        self.default_scale = kwargs.pop('default_scale', kwargs.pop('defaultScale', None))
        self.default_value = kwargs.pop('default_value', kwargs.pop('defaultValue', None))
        self.default_value_type = kwargs.pop('default_value_type', kwargs.pop('defaultValueType', None))
        self.description = kwargs.pop('description', None)
        self.dimension = kwargs.pop('dimension', False)
        self.disable_editing = kwargs.pop('disable_editing', kwargs.pop('disableEditing', False))
        self.exclude_from_shifting = kwargs.pop('exclude_from_shifting', kwargs.pop('excludeFromShifting', False))
        self.faceting_behavior_type = kwargs.pop('faceting_behavior_type', kwargs.pop('facetingBehaviorType', None))
        self.format = kwargs.pop('format', None)
        self.hidden = kwargs.pop('hidden', False)
        self.import_aliases = kwargs.pop('import_aliases', kwargs.pop('importAliases', None))
        self.label = kwargs.pop('label', None)
        self.lookup_container = kwargs.pop('lookup_container', kwargs.pop('lookupContainer', None))
        self.lookup_description = kwargs.pop('lookup_description', kwargs.pop('lookupDescription', None))
        self.lookup_query = kwargs.pop('lookup_query', kwargs.pop('lookupQuery', None))
        self.lookup_schema = kwargs.pop('lookup_schema', kwargs.pop('lookupSchema', None))
        self.measure = kwargs.pop('measure', False)
        self.mv_enabled = kwargs.pop('mv_enabled', kwargs.pop('mvEnabled', False))
        self.name = kwargs.pop('name', None)
        self.ontology_uri = kwargs.pop('ontology_uri', kwargs.pop('ontologyURI', None))
        self.phi = kwargs.pop('phi', None)
        self.prevent_reordering = kwargs.pop('prevent_reordering', kwargs.pop('preventReordering', False))
        self.property_id = kwargs.pop('property_id', kwargs.pop('propertyId', None))
        self.property_uri = kwargs.pop('property_uri', kwargs.pop('propertyURI', None))
        # self.property_validators
        self.range_uri = kwargs.pop('range_uri', kwargs.pop('rangeURI', None))
        self.recommended_variable = kwargs.pop('recommended_variable', kwargs.pop('recommendedVariable', False))
        self.redacted_text = kwargs.pop('redacted_text', kwargs.pop('redactedText', None))
        self.required = kwargs.pop('required', False)
        self.scale = kwargs.pop('scale', None)
        self.search_terms = kwargs.pop('search_terms', kwargs.pop('searchTerms', None))
        self.semantic_type = kwargs.pop('semantic_type', kwargs.pop('semanticType', None))
        self.set_dimension = kwargs.pop('set_dimension', kwargs.pop('setDimension', False))
        self.set_exclude_from_shifting = kwargs.pop('set_exclude_from_shifting', kwargs.pop('setExcludeFromShifting', False))
        self.set_measure = kwargs.pop('set_measure', kwargs.pop('setMeasure', False))
        self.shown_in_details_view = kwargs.pop('shown_in_details_view', kwargs.pop('shownInDetailsView', False))
        self.shown_in_insert_view = kwargs.pop('shown_in_insert_view', kwargs.pop('shownInInsertView', False))
        self.shown_in_update_view = kwargs.pop('shown_in_update_view', kwargs.pop('shownInUpdateView', False))
        self.type_editable = kwargs.pop('type_editable', kwargs.pop('typeEditable', False))
        self.url = kwargs.pop('url', None)

    @staticmethod
    def from_data(data):
        return PropertyDescriptor(**data)
