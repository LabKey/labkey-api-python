from labkey.security import who_am_i
import pytest
from labkey.api_wrapper import APIWrapper

# copy from:
# JavaClientApiTest.testImpersonateUser()
# JavaClientApiTest.testImpersonationConnection()

pytestmark = pytest.mark.integration  # Mark all tests in this module as integration tests
TEST_EMAIL = "test_user@test.test"
TEST_DISPLAY_NAME = "test user"


@pytest.fixture(scope="session")
def test_user(api: APIWrapper, project):
    url = api.server_context.build_url("security", "createNewUser.api")
    resp = api.server_context.make_request(url, {"email": TEST_EMAIL, "sendEmail": False})
    user_id = resp["userId"]
    yield {"id": user_id, "email": TEST_EMAIL, "display_name": TEST_DISPLAY_NAME}
    url = api.server_context.build_url("security", "deleteUser.api", container_path="/")
    resp = api.server_context.make_request(url, {"id": user_id})


def test_impersonation(api: APIWrapper, test_user):
    # test impersonation via email
    api.security.impersonate_user(email=TEST_EMAIL)
    who = who_am_i(api.server_context)
    assert who.display_name == test_user["display_name"]
    assert who.email == test_user["email"]
    assert who.id == test_user["id"]

    # test stop impersonating
    api.security.stop_impersonating()
    who = who_am_i(api.server_context)
    assert who.display_name != test_user["display_name"]
    assert who.email != test_user["email"]
    assert who.id != test_user["id"]

    # test impersonation via user id
    api.security.impersonate_user(user_id=test_user["id"])
    who = who_am_i(api.server_context)
    assert who.display_name == test_user["display_name"]
    assert who.email == test_user["email"]
    assert who.id == test_user["id"]

    # We need to stop impersonating a user before leaving so we don't mess up other tests.
    api.security.stop_impersonating()
