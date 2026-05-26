#
# Copyright (c) 2021-2026 LabKey Corporation
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
import pytest
from labkey.api_wrapper import APIWrapper

# copy from:
# JavaClientApiTest.testImpersonateUser()
# JavaClientApiTest.testImpersonationConnection()

pytestmark = pytest.mark.integration  # Mark all tests in this module as integration tests
TEST_EMAIL = "test_user@example.com"
TEST_DISPLAY_NAME = "test user"
DEACTIVATED_EMAIL = "deactivated_user@example.com"
DEACTIVATED_DISPLAY_NAME = "deactivated user"


@pytest.fixture(scope="session")
def test_user(api: APIWrapper, project):
    url = api.server_context.build_url("security", "createNewUser.api")
    resp = api.server_context.make_request(url, {"email": TEST_EMAIL, "sendEmail": False})
    user_id = resp["userId"]
    yield {"id": user_id, "email": TEST_EMAIL, "display_name": TEST_DISPLAY_NAME}
    url = api.server_context.build_url("security", "deleteUser.api", container_path="/")
    api.server_context.make_request(url, {"id": user_id})


def test_impersonation(api: APIWrapper, test_user):
    # test impersonation via email
    api.security.impersonate_user(email=TEST_EMAIL)
    who = api.security.who_am_i()
    assert who.display_name == test_user["display_name"]
    assert who.email == test_user["email"]
    assert who.id == test_user["id"]

    # test stop impersonating
    api.security.stop_impersonating()
    who = api.security.who_am_i()
    assert who.display_name != test_user["display_name"]
    assert who.email != test_user["email"]
    assert who.id != test_user["id"]

    # test impersonation via user id
    api.security.impersonate_user(user_id=test_user["id"])
    who = api.security.who_am_i()
    assert who.display_name == test_user["display_name"]
    assert who.email == test_user["email"]
    assert who.id == test_user["id"]

    # We need to stop impersonating a user before leaving so we don't mess up other tests.
    api.security.stop_impersonating()


@pytest.fixture(scope="module")
def deactivated_user(api: APIWrapper, project):
    url = api.server_context.build_url("security", "createNewUser.api")
    resp = api.server_context.make_request(url, {"email": DEACTIVATED_EMAIL, "sendEmail": False})
    user_id = resp["userId"]
    yield {"id": user_id, "email": DEACTIVATED_EMAIL, "display_name": DEACTIVATED_DISPLAY_NAME}
    url = api.server_context.build_url("security", "deleteUser.api", container_path="/")
    api.server_context.make_request(url, {"id": user_id})


def test_issue_52904(api: APIWrapper, deactivated_user):
    resp = api.security.deactivate_users(target_ids=[deactivated_user["id"]])
    assert resp["success"] is True

    # Deactivating again shouldn't issue a redirect
    resp = api.security.deactivate_users(target_ids=[deactivated_user["id"]])
    assert resp["success"] is True
