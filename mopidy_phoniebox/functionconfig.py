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
from ast import literal_eval
from collections import namedtuple

from mopidy import config


class FunctionConfig(config.ConfigValue):
    """
    For serialization / deserialization of gpio function config values
    """
    tuple_functionconfig = namedtuple("FunctionConfig", ("fn_type", "fn_args"))

    def __init__(self):
        pass

    def deserialize(self, val):
        """
        Deserializes a config value to the corresponding FunctionConfig tuple.
        """
        if val is None:
            return None

        val = config.decode(val).strip()
        if val == "":
            return None

        arr = val.split(',')
        fn_type = arr[0].strip()
        if fn_type == '':
            raise ValueError(("empty fn_type for function config '{}' not"
                             + " allowed").format(val))
        del arr[0]
        fn_args = None
        if len(arr) > 0:
            try:
                fn_args = dict((k.strip(), literal_eval(v.strip())) for k, v in
                               (pair.split('=') for pair in arr))
            except ValueError:
                raise ValueError(("malformed function arguments for function"
                                 + " config '{}'").format(val))
        else:
            fn_args = dict()

        return self.tuple_functionconfig(fn_type, fn_args)

    def serialize(self, value, display=False):
        """
        Serializes a FunctionConfig tuple to the corresponding string value.
        """
        if value is None:
            return ""

        if value.fn_args is None or len(value.fn_args) == 0:
            return config.encode(value.fn_type)

        arr = [value.fn_type]
        for key in value.fn_args:
            val = value.fn_args[key]
            if isinstance(val, str) or isinstance(val, unicode):
                pair = "{}='{}'".format(key, val)
            else:
                pair = "{}={}".format(key, val)
            arr = arr + [pair]

        return config.encode(",".join(arr))
