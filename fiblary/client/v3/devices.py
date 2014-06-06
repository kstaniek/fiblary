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
 fiblary.devices
 ~~~~~~~~~~~~~~

 Home Center Device Manager Implementation
"""

from fiblary.client.v3 import base
from fiblary.common import exceptions

import logging


_logger = logging.getLogger(__name__)


# TODO(kstaniek):
# http://hc2/api/devices?type=satel_partition
# http://hc2/api/callAction?deviceID=312&name=removeFailedNodeId
# http://hc2/api/callAction?deviceID=38&name=wakeUpDeadDevice


class Controller(base.CommonController):
    RESOURCE = 'devices'
    API_PARAMS = ('id', 'type', 'roomID')

    def action(self, device_id, action, *args):
        cmd = "callAction?deviceID={0}&name={1}".format(device_id, action)
        for i, arg in enumerate(args, 1):
            cmd = '{0}&arg{1}={2}'.format(cmd, i, arg)

        resp = self.http_client.get(cmd)
        if resp.status_code != 200 and resp.status_code != 202:
            exceptions.from_response(resp)

    def update(self, data):
        try:
            """
            HC2 does not like those properties to be PUT
            """
            data.properties.pop("associationView")
            data.properties.pop("associationSet")

        except Exception:
            pass

        return super(Controller, self).update(data)
