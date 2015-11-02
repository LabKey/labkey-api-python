from __future__ import unicode_literals
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey.utils import create_server_context
from labkey.query import delete_rows, update_rows, insert_rows, select_rows, execute_sql
from labkey.exceptions import RequestError, QueryNotFoundError, ServerNotFoundError, RequestAuthorizationError
from mock_server_responses import MockDeleteRows, MockUpdateRows, MockInsertRows, MockSelectRows, MockExecuteSQL


def success_test(test, expected_response, api_method, *args, **expected_kwargs):
    with mock.patch('labkey.utils.requests.Session.post') as mock_post:
        mock_post.return_value = expected_response
        resp = api_method(*args)

        # validate response is as expected
        test.assertEquals(resp, expected_response.text)

        # validate call is made as expected
        expected_args = expected_kwargs.pop('expected_args')
        mock_post.assert_called_once_with(*expected_args, **expected_kwargs)


def throws_error_test(test, expected_error, expected_response, api_method, *args, **expected_kwargs):
    with mock.patch('labkey.utils.requests.Session.post') as mock_post:
        with test.assertRaises(expected_error):
            mock_post.return_value = expected_response
            api_method(*args)

        # validate call is made as expected
        expected_args = expected_kwargs.pop('expected_args')
        mock_post.assert_called_once_with(*expected_args, **expected_kwargs)


configs = {
    'protocol': 'https://'
    , 'server': 'my_testServer:8080'
    , 'context_path': 'testPath'
    , 'project_path': 'testProject/subfolder'
}

schema = 'testSchema'
query = 'testQuery'
server_context = create_server_context(configs['server'], configs['project_path'], configs['context_path'])


class TestDeleteRows(unittest.TestCase):

    def setUp(self):
        self.configs = configs.copy()
        self.service = MockDeleteRows(**self.configs)
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"queryName": "' + query + '", "rows": "{id:1234}", "schemaName": "' + schema + '"}'
            , 'headers': {u'Content-Type': u'application/json'}
            , 'timeout': 30
        }

        rows = '{id:1234}'
        self.args = [
            server_context, schema, query, rows
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), delete_rows, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , delete_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , delete_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , delete_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , delete_rows, *self.args, **self.expected_kwargs)


class TestUpdateRows(unittest.TestCase):

    def setUp(self):
        self.configs = configs.copy()
        self.service = MockUpdateRows(**self.configs)
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"queryName": "' + query + '", "rows": "{id:1234}", "schemaName": "' + schema + '"}'
            , 'headers': {u'Content-Type': u'application/json'}
            , 'timeout': 30
        }

        rows = '{id:1234}'
        self.args = [
            server_context, schema, query, rows
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), update_rows, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , update_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , update_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , update_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , update_rows, *self.args, **self.expected_kwargs)


class TestInsertRows(unittest.TestCase):

    def setUp(self):
        self.configs = configs.copy()
        self.service = MockInsertRows(**self.configs)
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': '{"queryName": "' + query + '", "rows": "{id:1234}", "schemaName": "' + schema + '"}'
            , 'headers': {u'Content-Type': u'application/json'}
            , 'timeout': 30
        }

        rows = '{id:1234}'
        self.args = [
            server_context, schema, query, rows
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), insert_rows, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , insert_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , insert_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , insert_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , insert_rows, *self.args, **self.expected_kwargs)


class TestExecuteSQL(unittest.TestCase):

    def setUp(self):
        self.configs = configs.copy()
        self.service = MockExecuteSQL(**self.configs)
        sql = 'select * from ' + schema + '.' + query
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': {'sql': sql, "schemaName": schema}
            , 'headers': None
            , 'timeout': 30
        }

        self.args = [
            server_context, schema, sql
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), execute_sql, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , execute_sql, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , execute_sql, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , execute_sql, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , execute_sql, *self.args, **self.expected_kwargs)


class TestSelectRows(unittest.TestCase):

    def setUp(self):
        self.configs = configs.copy()
        self.service = MockSelectRows(**self.configs)
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()]
            , 'data': {"schemaName": schema, "query.queryName": query}
            , 'headers': None
            , 'timeout': 30
        }

        self.args = [
            server_context, schema, query
        ]

    def test_success(self):
        test = self
        success_test(test, self.service.get_successful_response(), select_rows, *self.args, **self.expected_kwargs)

    def test_unauthorized(self):
        test = self
        throws_error_test(test, RequestAuthorizationError, self.service.get_unauthorized_response()
                          , select_rows, *self.args, **self.expected_kwargs)

    def test_query_not_found(self):
        test = self
        throws_error_test(test, QueryNotFoundError,  self.service.get_query_not_found_response()
                          , select_rows, *self.args, **self.expected_kwargs)

    def test_server_not_found(self):
        test = self
        throws_error_test(test, ServerNotFoundError, self.service.get_server_not_found_response()
                          , select_rows, *self.args, **self.expected_kwargs)

    def test_general_error(self):
        test = self
        throws_error_test(test, RequestError, self.service.get_general_error_response()
                          , select_rows, *self.args, **self.expected_kwargs)


if __name__ == '__main__':
    unittest.main()
