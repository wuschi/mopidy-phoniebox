#
#  Copyright 2019 Thomas Wunschel (https://github.com/wuschi)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from collections import namedtuple

from mopidy import config


class ButtonConfig(config.ConfigValue):
    """
    For serialization / deserialization of button config values
    """
    tuple_buttonconfig = namedtuple("ButtonConfig", ("gpio", "action"))

    valid_actions = "when_pressed", "when_held"

    def __init__(self):
        pass

    def deserialize(self, val):
        """
        Deserializes a config value to the corresponding ButtonConfig tuple.

        :param val: the value to deserialize
        :type val: :class:`string` or :class:`None`
        """
        if val is None:
            return None

        val = config.decode(val).strip()
        if val == "":
            return None

        val = val.split(',')
        if len(val) != 2:
            raise ValueError("invalid config string for button config: {}"
                             .format(val))

        gpio = val[0].strip().replace("gpio", "")
        try:
            gpio = int(gpio)
        except ValueError:
            raise ValueError("invalid gpio for button config: {}".format(val))
        if gpio < 0 or gpio > 27:
            raise ValueError("invalid range for gpio in button config {}"
                             + " - must be between 0 and 27".format(val))

        action = val[1].strip()
        if action not in self.valid_actions:
            raise ValueError(("invalid action for button config {}"
                             + " - one of {} required").format(
                                 val, ','.join(self.valid_actions)))

        return self.tuple_buttonconfig(gpio, action)

    def serialize(self, value, display=False):
        """
        Serializes a ButtonConfig tuple to the corresponding string value.

        :param value: the :class:`ButtonConfig` to serialize
        :param display: for masking out passwords etc. (not used here)
        """
        if value is None:
            return ""

        value = "gpio{:d},{:s}".format(value.gpio, value.action)

        return config.encode(value)
