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
Exceptions
"""

import sys


class CommandError(Exception):
    pass


class BaseException(Exception):
    """An error occurred."""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message or self.__class__.__doc__


class ConnectionError(BaseException):
    """Connection Error"""
    pass


class NoUniqueMatch(BaseException):
    """No uniqueue item match"""
    pass


class NotFound(BaseException):
    """Item not found"""
    pass


class HandlerNotFound(BaseException):
    """Handler not found"""
    pass


class WrongArgumentsNumber(Exception):
    def __init__(self, action, expected_num_arg, num_arg):
            self.action = action
            self.num_arg = num_arg
            self.expected_num_arg = expected_num_arg

    def __str__(self):
        return "{0} takes exactly {1} arguments ({2} given)".format(
            repr(self.action),
            self.expected_num_arg,
            self.num_arg)


class HTTPException(Exception):
    """Base exception for all HTTP-derived exceptions."""
    code = 'N/A'

    def __init__(self, details=None):
        self.details = details or self.__class__.__doc__

    def __str__(self):
        return "%s (HTTP %s)" % (self.details, self.code)


class HTTPNotFound(HTTPException):
    """Not Found"""
    code = 404


class HTTPInternalServerError(HTTPException):
    """Internal Server Error"""
    code = 500


class HTTPMultipleChoices(HTTPException):
    """Multiple Choices"""
    code = 300


class HTTPBadRequest(HTTPException):
    """Bad Request"""
    code = 400

_code_map = {}
for obj_name in dir(sys.modules[__name__]):
    if obj_name.startswith('HTTP'):
        obj = getattr(sys.modules[__name__], obj_name)
        _code_map[obj.code] = obj


def from_response(response, details=True):
    """Return an instance of an HTTPException based on requests response."""
    cls = _code_map.get(response.status_code, HTTPException)
    if details:
        details = response.reason
        return cls(details=details)

    return cls()
