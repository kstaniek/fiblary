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
import time

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

    rooms = dict((room.id, room.name) for room in hc2.rooms.list())

    def get_room_name_from_id(room_id):
        try:
            return rooms[room_id]
        except KeyError:
            return "Not assigned"

    start = time.time()
    open_doors = hc2.devices.list(
        type="door_sensor",  # type handled directly by RESTApi
        p_value="1",    # for properties prepend with p_
        p_disabled="0"
    )

    print("Open doors:")
    for device in open_doors:
        room_id = device.roomID
        room_name = get_room_name_from_id(room_id)
        print("  {}({}) in {}".format(device.name, device.id, room_name))

    stop = time.time()
    print("Command execution time: {0:.2f}s".format(stop - start))

    start = time.time()
    open_doors = hc2.devices.list(
        type="door_sensor",
        jsonpath="$[?(@.properties.value=='1'"
        " && @.properties.disabled=='0')]")

    print("\nOpen doors:")
    for device in open_doors:
        room_id = device.roomID
        room_name = get_room_name_from_id(room_id)
        print("  {}({}) in {}".format(device.name, device.id, room_name))

    stop = time.time()
    print("Command execution time: {0:.2f}s".format(stop - start))

    start = time.time()
    open_windows = hc2.devices.list(
        type="window_sensor",
        p_value="1",
        p_disabled="0"
    )

    print("\nOpen windows:")
    for device in open_windows:
        room_id = device.roomID
        room_name = get_room_name_from_id(room_id)
        print("  {}({}) in {}".format(device.name, device.id, room_name))

    stop = time.time()
    print("Command execution time: {0:.2f}s".format(stop - start))

    start = time.time()
    open_windows = hc2.devices.list(
        type="window_sensor",
        jsonpath="$[?(@.properties.value=='1'"
        " && @.properties.disabled=='0')]")

    print("\nOpen windows:")
    for device in open_windows:
        room_id = device.roomID
        room_name = get_room_name_from_id(room_id)
        print("  {}({}) in {}".format(device.name, device.id, room_name))

    stop = time.time()
    print("Command execution time: {0:.2f}s".format(stop - start))

    start = time.time()
    lights = hc2.devices.list(p_disabled="0", p_isLight="1")

    print("\nLights:")
    for device in lights:
        room_id = device.roomID
        room_name = get_room_name_from_id(room_id)
        state = "on" if device.properties['value'] == "1" else "off"
        print("  {}({}) in {} is {}".format(
            device.name,
            device.id,
            room_name,
            state))

    stop = time.time()
    print("Command execution time: {0:.2f}s".format(stop - start))

    start = time.time()
    lights = hc2.devices.list(
        jsonpath="$[?(@.properties.disabled=='0'"
        " && @.properties.isLight=='1')]")

    print("\nLights:")
    for device in lights:
        room_id = device.roomID
        room_name = get_room_name_from_id(room_id)
        state = "on" if device.properties['value'] == "1" else "off"
        print("  {}({}) in {} is {}".format(
            device.name,
            device.id,
            room_name,
            state))

    stop = time.time()
    print("Command execution time: {0:.2f}s".format(stop - start))

    start = time.time()
    try:
        device = hc2.devices.find(name=u'Blue lights')
        value = device.properties['value']
        if value == "1":
            device.turnOff()
            print("\nBlue lights turned off")
        else:
            device.turnOn()
            print("\nBlue lights turned on")

    except exceptions.NotFound:
        print("\nBlue Lights not found")
    stop = time.time()
    print("Command execution time: {0:.2f}s".format(stop - start))

    try:
        device = hc2.devices.find(type='binary_light')
    except exceptions.NoUniqueMatch:
        print("\nMore then one device matching the criteria")

if __name__ == '__main__':
    main()
