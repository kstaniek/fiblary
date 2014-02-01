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


logging.basicConfig(
    format='%(asctime)-15s %(levelname)s: %(module)s:%(funcName)s'
    ':%(lineno)d: %(message)s',
    level=logging.CRITICAL)


def print_section_table(sections):
    table = pt.PrettyTable([
        "id",
        "name",
        "sortOrder"])

    for section in sections:
        table.add_row([
            section.id,
            section.name,
            section.sortOrder])

    print(table)


def print_room_table(rooms):
    table = pt.PrettyTable([
        "id",
        "name",
        "sectionID",
        "icon",
        "temperature",
        "humidity",
        "light",
        "thermostat"])

    for room in rooms:
        table.add_row([
            room.id,
            room.name,
            room.sectionID,
            room.icon,
            room.defaultSensors['temperature'],
            room.defaultSensors['humidity'],
            room.defaultSensors['light'],
            room.defaultThermostat])

    print(table)


def main():

    hc2 = Client(
        'v3',
        'http://192.168.1.230/api',
        'admin',
        'admin'
    )

    sections = hc2.sections.list()
    print_section_table(sections)
    print("Adding new section")
    section = hc2.sections.create(name="fiblaro_test_section")

    sections = hc2.sections.list()
    print_section_table(sections)

    rooms = hc2.rooms.list()
    print_room_table(rooms)

    print("Adding new room")
    room = hc2.rooms.create(name="fiblaro_test_room", sectionID=section.id)
    rooms = hc2.rooms.list()
    print_room_table(rooms)

    print("Changing the room name")
    room.name = "fiblaro_test_room_1"
    room = hc2.rooms.update(room)
    print("Changing the room name to: {}".format(room.name))

    rooms = hc2.rooms.list(name="fiblaro_test_room_1")
    print_room_table(rooms)

    print("Deleting rooms")
    for room in hc2.rooms.list(name="fiblaro_test_room_1"):
        hc2.rooms.delete(room.id)

    rooms = hc2.rooms.list(name="fiblaro_test_room_1")
    print_room_table(rooms)

    sections = hc2.sections.list(name="fiblaro_test_section")
    print_section_table(sections)

    print("Deleting sections")
    for section in hc2.sections.list(name="fiblaro_test_section"):
        hc2.sections.delete(section.id)

    sections = hc2.sections.list(name="fiblaro_test_section")
    print_section_table(sections)

    exit()


if __name__ == '__main__':
    main()
