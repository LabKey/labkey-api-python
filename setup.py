#!/usr/bin/env python

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

from distutils.core import setup
setup(name='LabKey',
      version='0.24',
      description='Python client API for LabKey Server',
      long_description = open('README.txt').read() + open('NEWS.txt').read(),
      license="Apache License 2.0",
      author='Elizabeth Nelson',
      author_email='eknelson@labkey.com',
      maintainer='Brian Connolly',
      maintainer_email='brian@labkey.com',
      url='https://www.labkey.org/wiki/home/Documentation/page.view?name=python',
      download_url='http://www.labkey.com/download-labkey-server',
      packages=['labkey'],
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
