#
# Copyright (c) 2017-2018 LabKey Corporation
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
from datetime import date, datetime
import unittest

try:
    import mock
except ImportError:
    import unittest.mock as mock

from labkey import utils


class TestJsonDumps(unittest.TestCase):

    def test_encoder(self):
        # test date and datetime encoding
        payload = {
            'my_date': date(1985, 9, 11),
            'my_date_time': datetime(2018, 9, 18, 5, 25)
        }

        utils.json_dumps(payload)

    def test_encoder_override(self):
        payload = {
            'testdate': datetime(2018, 9, 11, 6, 45)
        }

        try:
            # disable the "cls" override by passing None
            utils.json_dumps(payload, cls=None)
        except TypeError as e:
            if "is not JSON serializable" not in str(e):
                print("Did not see expected exception")
                raise e


def suite():
    load_tests = unittest.TestLoader().loadTestsFromTestCase
    return unittest.TestSuite([
        load_tests(TestJsonDumps)
    ])


if __name__ == '__main__':
    utils.DISABLE_CSRF_CHECK = True
    unittest.main()
