#
# Copyright (c) 2017 LabKey Corporation
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
import unittest

from labkey import utils
from labkey.unsupported import messageboard

from test_utils import MockLabKey, mock_server_context, success_test


class MockPostMessage(MockLabKey):
    api = 'insert.api'
    default_action = 'announcements'


class MockUpdateWiki(MockLabKey):
    api = 'editWiki.api'
    default_action = 'wiki'
    default_success_body = '<h1>Some wiki content</h1>'


class TestPostMessage(unittest.TestCase):

    def setUp(self):

        message_title = 'Test Insert Message'
        message_body = 'The body of the message'
        render_as = 'HTML'

        expected_content = {
            'body': message_body,
            'title': message_title,
            'rendererType': render_as
        }

        self.service = MockPostMessage()
        self.expected_kwargs = {
            'expected_args': [self.service.get_server_url()],
            'data': expected_content,
            'headers': None,
            'timeout': 300
        }

        self.args = [
            mock_server_context(self.service), message_title, message_body, render_as
        ]

    def test_success(self):
        success_test(self, self.service.get_successful_response(), messageboard.post_message, False,
                     *self.args, **self.expected_kwargs)


class TestUpdateWiki(unittest.TestCase):
    def setUp(self):

        wiki_name = 'WikiToUpdate'
        wiki_body = 'Updated wiki body'

        self.service = MockUpdateWiki()
        self.expected_kwargs = {
            'expected_args': [
                self.service.get_server_url(),
            ],
            'headers': {'Content-type': 'application/json'},
            'params': {
                'name': wiki_name
            }
        }

        self.args = [
            mock_server_context(self.service), wiki_name, wiki_body
        ]

    # TODO: Enable this test after update wiki is modified to only issue one request
    # def test_success(self):
    #     success_test_get(self, self.service.get_successful_response(), wiki.update_wiki, False,
    #                  *self.args, **self.expected_kwargs)


def suite():
    load_tests = unittest.TestLoader().loadTestsFromTestCase
    return unittest.TestSuite([
        load_tests(TestPostMessage),
        load_tests(TestUpdateWiki)
    ])


if __name__ == '__main__':
    utils.DISABLE_CSRF_CHECK = True
    unittest.main()
