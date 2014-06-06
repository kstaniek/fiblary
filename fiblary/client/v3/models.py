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
 fiblary.models
 ~~~~~~~~~~~~~~~~~

 Home Center Model Class Implementations

"""

import functools
import jsonpatch
import logging
import six

_logger = logging.getLogger(__name__)


_type_ignore = ["HC_user", "VOIP_user", "weather", 'iOS_device', '']


def factory(controller, item):
    # try as item could be anything
    try:
        if item['type'] in _type_ignore:
            return None
    except Exception:
        pass

    model = None
    if isinstance(item, dict):
        if controller.RESOURCE == 'devices':
            model = DeviceModel(controller, item)
        elif controller.RESOURCE == 'scenes':
            model = SceneModel(controller, item)
        else:
            model = GenericModel(controller, item)
    elif isinstance(item, list):
        model = RecursiveList(item)
    else:
        assert 0, "Unknown model"
    return model


class RecursiveList(list):

    def __init__(self, value):
        if value is None:
            pass
        elif isinstance(value, list):
            for index, data in enumerate(value):
                self.append(data)
                self.__setitem__(index, data)
        else:
            raise TypeError, 'Expected list'

        self.__dict__['__original__'] = value

    def __getitem__(self, key):
        return list.__getitem__(self, key)

    def __setitem__(self, key, value):
        if isinstance(value, str):
            value = unicode(value)
        if isinstance(value, list) and not isinstance(value, RecursiveList):
            value = RecursiveList(value)

        if isinstance(value, dict) and not isinstance(value, RecursiveDict):
            value = RecursiveDict(value)

        list.__setitem__(self, key, value)

    __setattr__ = __setitem__
    __getattr__ = __getitem__


class RecursiveDict(dict):
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError, 'Expected dict'
        self.__dict__['__original__'] = value

    def changes(self):
        original = self.__dict__['__original__']
        return jsonpatch.make_patch(original, dict(self)).to_string()

    def __setitem__(self, key, value):
        if isinstance(value, str):
            value = unicode(value)
        if isinstance(value, dict) and not isinstance(value, RecursiveDict):
            value = RecursiveDict(value)

        if isinstance(value, list) and not isinstance(value, RecursiveList):
            value = RecursiveList(value)

        if not callable(value):
            dict.__setitem__(self, key, value)
        else:
            # actions are callable so added only to the local dict
            self.__dict__[key] = value

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    __setattr__ = __setitem__
    __getattr__ = __getitem__


class GenericModel(RecursiveDict):
    def __init__(self, controller, item):
        self.__dict__['controller'] = controller
        super(GenericModel, self).__init__(item)


class DeviceModel(GenericModel):
    def __init__(self, controller, item):
        super(DeviceModel, self).__init__(controller, item)

        if 'actions' in self:
            def action(action_name, argn, *args, **kwargs):
                _logger.info("{0}({1})->{2}{3}".format(
                    self.name, self.id, action_name, args)
                )
                if len(args) != argn:
                    # hack due to http://bugzilla.fibaro.com/view.php?id=1125
                    if action_name != 'setTargetLevel':
                        raise TypeError(
                            "%s() takes exactly %d argument(s) (%d given)" % (
                                action_name, argn, len(args))
                        )
                return self.controller.action(self.id, action_name, *args)

            for action_name, argn in six.iteritems(self['actions']):
                _logger.debug("{0}({1})<-{2}({3})".format(
                    self.name,
                    self.id,
                    action_name,
                    argn))

                self.__dict__[str(action_name)] = functools.partial(
                    action, action_name, argn)


class SceneModel(GenericModel):
    def __init__(self, controller, item):
        super(SceneModel, self).__init__(controller, item)
    """Home Center specific subclass for the Scene with actions"""

    def start(self):
        return self.controller.start(self.id)

    def stop(self):
        return self.controller.stop(self.id)

    def enable(self):
        return self.controller.enable(self.id)

    def disable(self):
        return self.controller.disable(self.id)
