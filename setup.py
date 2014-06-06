#!/usr/bin/env python
#  Copyright 2014 Klaudiusz Staniek
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import sys

import fiblary

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'fiblary',
    'fiblary.client',
    'fiblary.client.v3',
    'fiblary.common',
    'fiblary.external',
]

with open('requirements.txt') as f:
    requires = f.readlines()

with open('README.rst') as f:
    readme = f.read()

setup(
    name='fiblary',
    version=fiblary.__version__,
    description='Home Center 2 API Python Library',
    long_description=readme,
    author='Klaudiusz Staniek',
    author_email='klaudiusz@staniek.name',
    url='https://github.com/kstaniek/fiblary',
    packages=packages,
    package_data={'': ['LICENSE', ], },
    package_dir={'fiblary': 'fiblary'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
