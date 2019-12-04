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
from __future__ import unicode_literals

import unittest

from mopidy_phoniebox import FunctionConfig


class FunctionConfigTest(unittest.TestCase):

    def test_deserialize(self):

        fn_conf = FunctionConfig().deserialize("some_fn")
        self.assertIsInstance(fn_conf, FunctionConfig.tuple_functionconfig)
        self.assertEqual("some_fn", fn_conf.fn_type)
        self.assertEqual(0, len(fn_conf.fn_args))

        fn_conf = FunctionConfig().deserialize("some_fn,a=0")
        self.assertIsInstance(fn_conf, FunctionConfig.tuple_functionconfig)
        self.assertEqual("some_fn", fn_conf.fn_type)
        self.assertEqual(1, len(fn_conf.fn_args))
        self.assertEqual(0, fn_conf.fn_args['a'])

        fn_conf = FunctionConfig().deserialize("some_fn,a=0,b = '1',c = 'bla'")
        self.assertIsInstance(fn_conf, FunctionConfig.tuple_functionconfig)
        self.assertEqual("some_fn", fn_conf.fn_type)
        self.assertEqual(3, len(fn_conf.fn_args))
        self.assertEqual(0, fn_conf.fn_args['a'])
        self.assertEqual('1', fn_conf.fn_args['b'])
        self.assertEqual('bla', fn_conf.fn_args['c'])

        fn_conf = FunctionConfig().deserialize(None)
        self.assertIsNone(fn_conf)

        fn_conf = FunctionConfig().deserialize("")
        self.assertIsNone(fn_conf)

        with self.assertRaises(ValueError):
            FunctionConfig().deserialize(",")

        with self.assertRaises(ValueError):
            FunctionConfig().deserialize(",a=0")

        with self.assertRaises(ValueError):
            FunctionConfig().deserialize("some_fn,")

        with self.assertRaises(ValueError):
            FunctionConfig().deserialize("some_fn,a=0,")

        with self.assertRaises(ValueError):
            FunctionConfig().deserialize("some_fn,a=bla")

    def test_serialize(self):
        fn_conf = FunctionConfig.tuple_functionconfig("some_fn", None)
        val = FunctionConfig().serialize(fn_conf)
        self.assertEqual("some_fn", val)

        fn_conf = FunctionConfig.tuple_functionconfig("some_fn", {})
        val = FunctionConfig().serialize(fn_conf)
        self.assertEqual("some_fn", val)

        fn_conf = FunctionConfig.tuple_functionconfig("some_fn", {'a': 0})
        val = FunctionConfig().serialize(fn_conf)
        self.assertEqual("some_fn,a=0", val)

        fn_conf = FunctionConfig.tuple_functionconfig(
                "some_fn", {'a': 0, 'b': 'blub'})
        val = FunctionConfig().serialize(fn_conf)
        self.assertTrue(
            "some_fn,a=0,b='blub'" == val or "some_fn,b='blub',a=0" == val)

        val = FunctionConfig().serialize(None)
        self.assertEqual("", val)
