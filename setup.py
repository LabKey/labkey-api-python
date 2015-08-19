#
# Copyright (c) 2011-2015 LabKey Corporation
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
Setup script for Python client API for LabKey Server.

Also installs included versions of third party libraries, if those libraries
are not already installed.
"""
from __future__ import print_function

import sys

if sys.version_info < (2, 6):
  print('labkey-api-python requires python version >= 2.6.',
        file=sys.stderr)
  sys.exit(1)

from setuptools import setup

packages = [
  'labkeyapi'
]

install_requires = []

long_desc = "Python client API for LabKey Server. Supports for query, wiki, and messageboard APIs."

setup(
  name='labkey',
  version='0.24',
  description='Python client API for LabKey Server',
  long_description=long_desc,
  license="Apache License 2.0",
  author='Elizabeth Nelson',
  author_email='eknelson@labkey.com',
  maintainer='Brian Connolly',
  maintainer_email='brian@labkey.com',
  url='https://www.labkey.org/wiki/home/Documentation/page.view?name=python',
  install_requires=install_requires,
  packages=packages,
  package_data={},
  keywords="labkey api client",
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: MacOS',
    'Operating System :: Microsoft',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2',
    'Topic :: Scientific/Engineering'
  ]
)
