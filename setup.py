#
# Copyright (c) 2015-2017 LabKey Corporation
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
import re
from setuptools import setup

packages = ["labkey"]

with open("labkey/__init__.py", "r") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

long_desc = "Python client API for LabKey Server. Supports query and experiment APIs."

tests_require = ["pytest", "requests", "mock", "pytest-cov"]

setup(
    name="labkey",
    version=version,
    description="Python client API for LabKey Server",
    long_description=long_desc,
    license="Apache License 2.0",
    author="LabKey",
    author_email="alanv@labkey.com",
    maintainer="Alan Vezina",
    maintainer_email="alanv@labkey.com",
    url="https://github.com/LabKey/labkey-api-python",
    packages=packages,
    package_data={},
    install_requires=["requests"],
    tests_require=tests_require,
    setup_requires=["pytest-runner"],
    extras_require={"test": tests_require},
    keywords="labkey api client",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
)
