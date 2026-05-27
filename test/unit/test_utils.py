#
# Copyright (c) 2017-2026 LabKey Corporation
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
from labkey.utils import btoa, encode_uri_component, waf_encode, snake_to_camel, transform_options


def test_btoa():
    assert btoa(None) is None
    assert btoa("") == ""
    assert btoa("DELETE TABLE some.table;") == "REVMRVRFIFRBQkxFIHNvbWUudGFibGU7"


def test_encode_uri_component():
    assert (
        encode_uri_component("SELECT * FROM x.y WHERE y = 5 & 2 AND y IS NOT NULL;")
        == "SELECT%20*%20FROM%20x.y%20WHERE%20y%20%3D%205%20%26%202%20AND%20y%20IS%20NOT%20NULL%3B"
    )
    assert (
        encode_uri_component("><&/%' \"1äöüÅ") == "%3E%3C%26%2F%25'%20%221%C3%A4%C3%B6%C3%BC%C3%85"
    )


def test_waf_encode():
    prefix = "/*{{base64/x-www-form-urlencoded/wafText}}*/"
    assert waf_encode(None) is None
    assert waf_encode("") == ""
    assert waf_encode("hello") == prefix + "aGVsbG8="
    assert (
        waf_encode("DELETE TABLE some.table;")
        == prefix + "REVMRVRFJTIwVEFCTEUlMjBzb21lLnRhYmxlJTNC"
    )
    assert (
        waf_encode("><&/%' \"1äöüÅ")
        == prefix + "JTNFJTNDJTI2JTJGJTI1JyUyMCUyMjElQzMlQTQlQzMlQjYlQzMlQkMlQzMlODU="
    )


def test_snake_to_camel():
    assert snake_to_camel("snake_case") == "snakeCase"
    assert snake_to_camel("multiple_word_snake_case") == "multipleWordSnakeCase"
    assert snake_to_camel("alreadyCamelCase") == "alreadyCamelCase"
    assert snake_to_camel("single") == "single"
    assert snake_to_camel("UPPER_SNAKE_CASE") == "upperSnakeCase"
    assert snake_to_camel("_leading_underscore") == "leadingUnderscore"
    assert snake_to_camel("trailing_underscore_") == "trailingUnderscore"
    assert snake_to_camel("multiple__underscores") == "multipleUnderscores"
    assert snake_to_camel("") == ""


def test_transform_options():
    options = {
        "include_columns": True,
        "include_system_queries": False,
        "include_title": False,
        "include_user_queries": False,
        "include_view_data_url": True,
        "query_detail_columns": False,
    }
    expected_keys = [
        "include_columns",
        "include_system_queries",
        "include_user_queries",
        "include_view_data_url",
    ]
    transformed_options = transform_options(options, expected_keys)
    assert transformed_options == {
        "includeColumns": True,
        "includeSystemQueries": False,
        "includeUserQueries": False,
        "includeViewDataUrl": True,
    }
    assert transformed_options["includeColumns"] is True

    # Empty options
    assert transform_options({}, ["any_key"]) == {}

    # Empty expected_keys
    assert transform_options({"any_key": 1}, []) == {}

    # Filtering behavior: only keys in expected_keys are kept and transformed
    options = {"keep_me": 1, "ignore_me": 2}
    expected = ["keep_me"]
    result = transform_options(options, expected)
    assert result == {"keepMe": 1}

    # Keys in expected_keys but not in options are ignored
    options = {"present_key": "I am present!"}
    expected = ["present_key", "absent_key"]
    result = transform_options(options, expected)
    assert result == {"presentKey": "I am present!"}

    # Non-snake_case keys that are in expected_keys
    options = {"alreadyCamel": 1, "simple": 2, "UPPER_SNAKE": 3}
    expected = ["alreadyCamel", "simple", "UPPER_SNAKE"]
    result = transform_options(options, expected)
    assert result == {"alreadyCamel": 1, "simple": 2, "upperSnake": 3}
