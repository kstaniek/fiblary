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
 fiblary.schemas
 ~~~~~~~~~~~~~~~~~

 Home Center Schema Manager Class Implementation

"""

import copy
import json
import jsonpatch
import logging
import os
import requests
import warlock.model as warlock

_logger = logging.getLogger(__name__)


class SchemaBasedModel(warlock.Model):
    """Home Center specific subclass of the warlock Model

    This implementation alters the function of the patch property
    to take into account the schema's core properties. With this version
    undefined properties which are core will generated 'replace'
    operations rather than 'add'.
    """
    @warlock.Model.patch.getter
    def patch(self):
        """Return a jsonpatch object representing the delta."""
        original = copy.deepcopy(self.__dict__['__original__'])
        new = dict(self)
        if self.__dict__['schema']:
            for prop in self.schema['properties']:
                if prop not in original and prop in new:
                    original[prop] = None

        return jsonpatch.make_patch(original, dict(self)).to_string()


class ActionSchemaModel(SchemaBasedModel):
    """Home Center specific subclass for the schemas with actions

    This implementation alters the setting items and makes callables
    (actions) and controller properties stored outside of the schema properties
    """

    def __setitem__(self, key, value):
        if not callable(value) and key != "controller":
            super(ActionSchemaModel, self).__setitem__(key, value)
        else:
            # actions are callable so added only to the local dict
            self.__dict__[key] = value


class SceneSchemaModel(ActionSchemaModel):
    """Home Center specific subclass for the Scene with actions"""
    def start(self):
        return self.controller.start(self.id)

    def stop(self):
        return self.controller.stop(self.id)

    def enable(self):
        return self.controller.enable(self.id)

    def disable(self):
        return self.controller.disable(self.id)


class Schema(object):
    """Home Center specific subclass for the Schema.

    It implements the ``name`` attribute
    """
    def __init__(self, raw_schema):
        self._raw_schema = raw_schema
        self.name = raw_schema['name']

    def raw(self):
        return copy.deepcopy(self._raw_schema)


class Controller(object):
    """Controller class to handle the schemas"""

    def __init__(self):
        self.schemas = {}

    def get(self, schema_name):

        if schema_name in self.schemas:
            _logger.debug("Get schema from memory cache: {}".format(
                schema_name))
            return self.schemas[schema_name]
        else:
            # try from local directory
            filename = "./.cache/{}.json".format(schema_name)

            if os.path.exists(filename):
                with open(filename) as f:
                    schema = json.load(f)
                    self.schemas[schema_name] = Schema(schema)
                    _logger.debug("Schema retrieved from local cache:"
                                  " {}".format(schema_name))
                    return self.schemas[schema_name]

            else:
                dirname = os.path.dirname(filename)
                try:
                    os.stat(dirname)
                except Exception:
                    os.mkdir(dirname)

                url = "https://raw.github.com/kstaniek/hcschema/master/json/"\
                    "{}.json".format(schema_name)
                response = requests.get(url)
                if response.status_code == 200:
                    schema = response.json()
                    self.schemas[schema_name] = Schema(schema)
                    _logger.info("Schema retrieved from repository: {}".format(
                        schema_name))
                    with open(filename, "w+") as f:
                        f.write(json.dumps(schema))
                    return self.schemas[schema_name]
                else:
                    self.schemas[schema_name] = None
                    _logger.info("Schema not found: {}".format(schema_name))
                    return None
