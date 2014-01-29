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
import prettytable as pt

from fiblary.client import Client

from fiblary.common.timestamp import datetime_to_epoch
from fiblary.common.timestamp import timestamp_to_iso

import datetime as dt


logging.basicConfig(
    format='%(asctime)-15s %(levelname)s: %(module)s:%(funcName)s'
    ':%(lineno)d: %(message)s',
    level=logging.CRITICAL)


def print_table(events, devices, rooms):
    table = pt.PrettyTable([
        "id",
        "timestamp",
        "deviceName",
        "roomName",
        "deviceType",
        "propertyName",
        "oldValue",
        "newValue"])

    table.align["deviceName"] = 'l'

    for event in events:
        device_name, roomID = devices[event.deviceID]
        try:
            room_name = rooms[roomID]
        except KeyError:
            room_name = "Unassigned"

        table.add_row([
            event.id,
            timestamp_to_iso(event.timestamp),
            "{}({})".format(room_name, roomID),
            "{}({})".format(device_name, event.deviceID),
            event.deviceType,
            event.propertyName,
            event.oldValue,
            event.newValue])

    print(table)


def main():

    hc2 = Client(
        'v3',
        'http://192.168.1.230/api',
        'admin',
        'admin'
    )

    rooms = dict((room.id, room.name) for room in hc2.rooms.list())
    devices = dict(
        (device.id, (device.name, device.roomID))
        for device in hc2.devices.list()
    )

    print("List of last 100 events")
    events = hc2.events.list(last='100', type='id')
    print_table(events, devices, rooms)

    print("List of last 10 events for device id=114")
    events = hc2.events.list(last='10', type='id', deviceID='114')
    print_table(events, devices, rooms)

    print(
        "List of all events for specific datetime 2014-01-28 9:00:00"
        " - 2014-01-28 12:00:00")
    start_datetime = datetime_to_epoch(dt.datetime(2014, 1, 28, 9, 0))
    stop_datetime = datetime_to_epoch(dt.datetime(2014, 1, 28, 12, 0))

    """" File "./events.py", line 102
    events = hc2.events.list(from=start_datetime, to=stop_datetime)
                                ^
    SyntaxError: invalid syntax

    Can someone tell me why I can't use from as a parameter name?
    """

    args = {
        'from': start_datetime,
        'to': stop_datetime,
        'type': 'time'
    }

    events = hc2.events.list(**args)
    print_table(events, devices, rooms)

    print(
        "List of all events for specific datetime 2014-01-28 9:00:00"
        " - 2014-01-28 12:00:00 for device ID=169")

    args = {
        'from': start_datetime,
        'to': stop_datetime,
        'type': 'time',
        'deviceID': 169
    }

    events = hc2.events.list(**args)
    print_table(events, devices, rooms)

    exit()

if __name__ == '__main__':
    main()
