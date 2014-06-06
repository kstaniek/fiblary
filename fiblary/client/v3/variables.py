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
 fiblary.variables
 ~~~~~~~~~~~~~~

 Home Center Variable Manager Implementation
"""


import logging

from fiblary.client.v3 import base
from fiblary.common import exceptions

# TODO(kstaniek): Handle predefined variables

_logger = logging.getLogger(__name__)


class Controller(base.CommonController):
    RESOURCE = 'globalVariables'

    def get(self, item_id):
        url = '{0}?name={1}'.format(self.RESOURCE, item_id)
        item = self.http_client.get(url).json()
        return self.model(**item)

    def delete(self, item_id):
        url = '{0}?name={1}'.format(self.RESOURCE, item_id)
        self.http_client.delete(url)
        return

    def set(self, name, value):
        data = {
            'name': name,
            'value': value
        }
        try:
            item = self.update(data)
            _logger.info('Variable set: {0}="{1}"'.format(name, value))
        except exceptions.HTTPNotFound:
            _logger.info('Variable created: {0}="{1}"'.format(name, value))
            item = self.create(**data)

        return self.model(**item)
