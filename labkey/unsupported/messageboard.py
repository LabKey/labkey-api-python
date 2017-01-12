#
# Copyright (c) 2015-2016 LabKey Corporation
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
"""
unsupported.messageboard
~~~~~~~~~~~~~~~~
WARNING: This module is not officially supported! Use at your own risk.

This module provides functions for interacting with Message Boards on the
LabKey Server.
"""
from __future__ import unicode_literals
from requests.exceptions import SSLError
from labkey.utils import build_url


def post_message(server_context, message_title, message_body, render_as, container_path=None):
    """
    Post a message to a message board on a LabKey instance.
    :param server_context: A LabKey server context. See utils.create_server_context.
    :param message_title: The title of the message.
    :param message_body: The content of the message.
    :param render_as: The content of the message.
    :param container_path: Optional container path that can be used to override the server_context container path
    :return: Returns 1 if successful, 0 is post failed.
    """
    # Build the URL for querying LabKey Server
    message_url = build_url(server_context, 'announcements', 'insert.api', container_path=container_path)

    message_data = {
        'title': message_title,
        'body': message_body,
        'rendererType': render_as
    }

    session = server_context['session']

    try:
        message_response = session.post(message_url, message_data)
    except SSLError as e:
        print("There was problem while attempting to submit the message to " + str(e.geturl()) + ". The HTTP response code was " + str(e.getcode()))
        print("The HTTP client error was: " + format(e))
        return 0
        
    return 1
