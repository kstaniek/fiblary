#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

import logging

from fiblary.client import Client

logging.basicConfig(
    format='%(asctime)-15s %(levelname)s: %(module)s:%(funcName)s'
    ':%(lineno)d: %(message)s',
    level=logging.CRITICAL)


def main():
    hc2 = Client(
        'v3',
        'http://192.168.1.230/api/',
        'admin',
        'admin'
    )

    info = hc2.info.get()
    print info

    weather = hc2.weather.get()
    print weather

    login = hc2.login.get()
    print login

    devices = hc2.devices.get(1)
    print devices

    devices = hc2.devices.list(name='Ceiling Lamp')
    print devices
    print type(devices)

    for device in devices:
        print device.name

    devices = hc2.devices.list(id=1)
    for device in devices:
        print device.name

if __name__ == '__main__':
    main()
