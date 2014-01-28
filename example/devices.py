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
from fiblary.common import exceptions


logging.basicConfig(
    format='%(asctime)-15s %(levelname)s: %(module)s:%(funcName)s'
    ':%(lineno)d: %(message)s',
    level=logging.CRITICAL)


def main():
    hc2 = Client(
        'v3',
        'http://192.168.1.230/api',
        'admin',
        'admin'
    )

    rooms = dict((room.id, room) for room in hc2.rooms.list())

    open_doors = hc2.devices.findall(
        type="door_sensor",
        value="1",
        disabled="0"
    )

    print("Currently open doors:")
    for device in open_doors:
        room_id = device.roomID
        room_name = rooms[room_id].name
        print("  {}({}) in {}".format(device.name, device.id, room_name))

    open_windows = hc2.devices.findall(
        type="window_sensor",
        value="1",
        disabled="0"
    )

    print("Currently open windows:")
    for device in open_windows:
        room_id = device.roomID
        room_name = rooms[room_id].name
        print("  {}({}) in {}".format(device.name, device.id, room_name))

    lights = hc2.devices.findall(isLight="1", disabled="0")

    print("Lights:")
    for device in lights:
        room_id = device.roomID
        room_name = rooms[room_id].name
        state = "on" if device.properties['value'] == "1" else "off"
        print("  {}({}) in {} is {}".format(
            device.name,
            device.id,
            room_name,
            state))

    try:
        device = hc2.devices.find(name="Blue lights")
        value = device.properties['value']
        if value == "1":
            device.turnOff()
        else:
            device.turnOn()

    except exceptions.NotFound:
        print("Device not found")


if __name__ == '__main__':
    main()
