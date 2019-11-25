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


class GpioConfig(config.ConfigValue):
    """
    For serialization / deserialization of gpio config values
    """
    tuple_gpioconfig = namedtuple("GpioConfig", ("pull_up_down",
                                                 "bounce_time",
                                                 "hold_time",
                                                 "hold_repeat"))

    valid_pull_up_downs = "pull_up", "pull_down", "none", "none_invert"

    def __init__(self):
        pass

    def deserialize(self, val):
        """
        Deserializes a config value to the corresponding GpioConfig tuple.
        """
        if val is None:
            return None

        val = config.decode(val).strip()
        if val == "":
            return None

        val = val.split(',')
        if len(val) < 1 or len(val) > 4:
            raise ValueError("invalid config string for gpio config: {}"
                             .format(val))

        bounce_time = None
        hold_time = 1
        hold_repeat = False

        pull_up_down = val[0].strip()
        if pull_up_down not in self.valid_pull_up_downs:
            raise ValueError(("invalid pull_up_down for gpio config {}"
                             + " - one of {} required").format(
                             pull_up_down, ", ".join(self.valid_pull_up_downs)
                             ))

        if len(val) > 1:
            bounce_time = val[1].strip()
            if bounce_time.lower() == "none":
                bounce_time = None
            else:
                try:
                    bounce_time = int(bounce_time)
                except ValueError:
                    raise ValueError("invalid bounce_time for gpio config: {}"
                                     .format(bounce_time))
                if bounce_time <= 0:
                    raise ValueError("bounce_time must not be zero or"
                                     + " negative: {}".format(bounce_time))

        if len(val) > 2:
            hold_time = val[2].strip()
            try:
                hold_time = float(hold_time)
            except ValueError:
                raise ValueError("invalid hold_time value for gpio config: {}"
                                 .format(hold_time))
            if hold_time <= 0:
                raise ValueError("hold_time must notbe zero or negative: {}"
                                 .format(hold_time))

        if len(val) > 3:
            hold_repeat = val[3].strip()
            if hold_repeat.lower() == "true":
                hold_repeat = True
            elif hold_repeat.lower() == "false":
                hold_repeat = False
            else:
                raise ValueError("invalid hold_repeat value for gpio config:"
                                 + " {}".format(hold_repeat))

        return self.tuple_gpioconfig(pull_up_down, bounce_time,
                                     hold_time, hold_repeat)

    def serialize(self, value, display=False):
        """
        Serializes a GpioConfig tuple to the corresponding string value.
        """
        if value is None:
            return ""

        value = "{:s},{},{},{}".format(value.pull_up_down, value.bounce_time,
                                       value.hold_time, value.hold_repeat)

        return config.encode(value)
