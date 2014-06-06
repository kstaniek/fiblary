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

import time


logging.basicConfig(
    format='%(asctime)-15s %(levelname)s: %(module)s:%(funcName)s'
    ':%(lineno)d: %(message)s',
    level=logging.CRITICAL)


SCENE = """--[[
%% properties
%% globals
--]]
while true do
    fibaro:debug("test")
    fibaro:sleep(600)
    fibaro:debug("test2")
end"""


def print_table(scenes):
    table = pt.PrettyTable([
        "ID",
        "Name",
        "Enabled",
        "Running Instances",
        "Autostart",
        "Killable"])

    for scene in scenes:
        table.add_row([
            scene.id,
            scene.name,
            scene.enabled,
            scene.runningInstances,
            scene.autostart,
            scene.killable])

    print(table)


def main():

    hc2 = Client(
        'v3',
        'http://192.168.1.230/api/',
        'admin',
        'admin'
    )

    scenes = hc2.scenes.findall()
    print_table(scenes)

    for scene_id in [scene.id for scene in hc2.scenes.findall()]:

        scene = hc2.scenes.get(scene_id)
        if scene.isLua:
            print(u"LUA Scene: {}".format(scene.name))
        else:
            print(u"Block Scene: {}".format(scene.name))

    print("Provisioning new scene")
    scene = hc2.scenes.create(name="fiblary_test_scene")
    scene.isLua = True
    scene.lua = SCENE
    scene.html = ""

    scene_id = scene.id
    scene = hc2.scenes.update(scene)

    print("Scene code:\n{}".format(scene.lua))

    scene.start()
    print("Scene {} running for 1 minute".format(scene_id))

    scenes = hc2.scenes.list(name="fiblary_test_scene")
    print_table(scenes)

    time.sleep(60)

    print("Scene {} stopping".format(scene_id))
    scene.stop()
    scenes = hc2.scenes.list(name="fiblary_test_scene")
    print_table(scenes)

    print("Deleting test scenes")
    for scene in hc2.scenes.list(name="fiblary_test_scene"):
        hc2.scenes.delete(scene.id)

    scenes = hc2.scenes.findall(name="fiblary_test_scene")
    print_table(scenes)

    exit()


if __name__ == '__main__':
    main()
