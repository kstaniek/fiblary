# Copyright 2013 Nebula Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

"""Test rest module"""

import operator

from fiblary.common import event
from fiblary.common import exceptions
from fiblary.tests import utils


event_name = "event_1"


def fake_handler():
    pass


class TestEventHook(utils.TestCase):

    def setUp(self):
        super(TestEventHook, self).setUp()

        self.event_hook = event.EventHook(event_name)

    def test_init(self):
        """Test constructor"""

        self.assertEqual(repr(self.event_hook), event_name)

    def test_add_remove_event(self):
        """Test adding the new event handler"""

        self.assertEqual(
            self.event_hook.get_handler_count(),
            0,
            "Incorrect initial number of handlers")

        self.assertEqual(
            self.event_hook.event_queue,
            None,
            "Event queue should not initialized")

        self.event_hook += fake_handler
        self.assertEqual(
            self.event_hook.get_handler_count(),
            1,
            "Incorect number of handlers")

        self.assertEqual(
            type(self.event_hook.event_queue),
            event.EventQueue,
            "Queue should be initialized with EventQueue")

        self.event_hook -= fake_handler
        self.assertEqual(
            self.event_hook.get_handler_count(),
            0,
            "Incorrect number of event handlers after subtraction")

        self.assertRaises(
            exceptions.HandlerNotFound,
            operator.isub,
            self.event_hook,
            fake_handler)
