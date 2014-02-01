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

"""
 fiblary.common.utils
 ~~~~~~~~~~~~~~~~~~~~

 Common Utilities Implementation
"""


import sys


def import_module(import_str):
    """Import a module."""
    __import__(import_str)
    return sys.modules[import_str]


def import_versioned_module(module, version, submodule=None):
    module = 'fiblary.%s.%s' % (module, version)
    if submodule:
        module = '.'.join((module, submodule))
    return import_module(module)


def quote_if_string(value):
    if type(value) in [str, unicode]:
        return "'{0}'".format(value)
    else:
        return value
