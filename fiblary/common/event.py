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
 fiblary.common.event
 ~~~~~~~~~~~~~~~~~~~~

 Event Implementation
"""
import logging
import threading

from fiblary.common import exceptions

try:
    import Queue as queue
except Exception:
    import queue

import inspect

_logger = logging.getLogger(__name__)


class EventQueue(threading.Thread):

    def __init__(self, name=None):
        super(EventQueue, self).__init__(name=name or self.__class__.__name__)
        self.queue = queue.Queue()
        self._stop = threading.Event("EventQueue Stop Event")

        self.n = 0
        self.serving = None
        self.daemon = True  # stop unconditionally on exit

        _logger.info("Starting the event queue for {}".format(self.name))
        self.start()

    def error(self, error, function, a=(), kw=None):
        """Called when function raises error.
        """
        _logger.exception(
            "EventQueue event raised exception ({}, {}, {}):{}".format(
                function, a, kw or {}, error)
        )

    def put(self, event, function=None, a=(), kw=None):
        """Queue the call to function, return the number of the call.
        """
        self.queue.put((event, function, a, kw or {}))
        return self.n + self.queue.qsize()

    def stop(self):
        _logger.info("Stopping the event queue for {}".format(self.name))
        self._stop.set()
        self.put("EXIT")

    def run(self):
        """A blocking loop which continually calls functions as specified
        in self.queue.
        """
        while not self.stopped():
            try:
                event, function, a, kw = self.queue.get(True, 120)
            except queue.Empty:
                _logger.warning("Event queue timeout: {}".format(self.name))
                continue

            if event == "EXIT":
                break

            _logger.debug("Calling on {} changed handlers".format(event))
            self.serving = (function, a, kw)
            try:
                function(*a, **kw)
            except Exception as e:
                self.error(e, function, a, kw)
            self.n += 1

    def stopped(self):
        return self._stop.isSet()


def queue_event(f):
    """Decorator which queues method/function calls in
    self.eventqueue and self.name [if f is a method whose
    first argument is 'self'],
    otherwise f.eventqueue.
    """
    args = inspect.getargspec(f)[0]
    if args and (args[0] == 'self'):
        def decorated(self, *a, **kw):
            if self.event_queue:
                self.event_queue.put(self.__repr__(), f, (self,) + a, kw)
    else:
        f.event_queue = EventQueue()

        def decorated(*a, **kw):
            f.event_queue.put(f.__name__, f, a, kw)
    decorated.__name__ = f.__name__
    decorated.__doc__ = f.__doc__
    return decorated


class EventHook(object):
    """EventHook as suggested from Michael Foord in his Event Pattern:
    http://www.voidspace.org.uk/python/weblog/arch_d7_2007_02_03.shtml#e616

    Extended with queue event
    """

    def __init__(self, name=""):
        self.__handlers = []
        self.name = name
        self.event_queue = None

    def get_handler_count(self):
        return len(self.__handlers)

    def __iadd__(self, handler):
        if not self.event_queue:
            self.event_queue = EventQueue(self.name)
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        try:
            self.__handlers.remove(handler)
        except ValueError:
            raise exceptions.HandlerNotFound

        if self.get_handler_count() == 0:
            self.event_queue.stop()
            self.event_queue.join()
            del self.event_queue
            self.event_queue = None
        return self

    def __repr__(self):
        return self.name

    @queue_event
    def __fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    __call__ = __fire
