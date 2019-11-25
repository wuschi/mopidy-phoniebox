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

from mopidy_phoniebox import GpioConfig


class GpioConfigTest(unittest.TestCase):

    def test_deserialize(self):

        gpio_conf = GpioConfig().deserialize("pull_up,150,2,False")
        self.assertIsInstance(gpio_conf, GpioConfig.tuple_gpioconfig)
        self.assertEqual("pull_up", gpio_conf.pull_up_down)
        self.assertEqual(150, gpio_conf.bounce_time)
        self.assertEqual(2, gpio_conf.hold_time)
        self.assertEqual(False, gpio_conf.hold_repeat)

        gpio_conf = GpioConfig().deserialize("pull_down,150,2.5,True")
        self.assertIsInstance(gpio_conf, GpioConfig.tuple_gpioconfig)
        self.assertEqual("pull_down", gpio_conf.pull_up_down)
        self.assertEqual(150, gpio_conf.bounce_time)
        self.assertEqual(2.5, gpio_conf.hold_time)
        self.assertEqual(True, gpio_conf.hold_repeat)

        gpio_conf = GpioConfig().deserialize(None)
        self.assertIsNone(gpio_conf)

        gpio_conf = GpioConfig().deserialize("")
        self.assertIsNone(gpio_conf)

        gpio_conf = GpioConfig().deserialize("pull_up,150,2")
        self.assertEqual("pull_up", gpio_conf.pull_up_down)
        self.assertEqual(150, gpio_conf.bounce_time)
        self.assertEqual(2, gpio_conf.hold_time)
        self.assertEqual(False, gpio_conf.hold_repeat)

        gpio_conf = GpioConfig().deserialize("pull_up,150")
        self.assertEqual("pull_up", gpio_conf.pull_up_down)
        self.assertEqual(150, gpio_conf.bounce_time)
        self.assertEqual(1, gpio_conf.hold_time)
        self.assertEqual(False, gpio_conf.hold_repeat)

        gpio_conf = GpioConfig().deserialize("pull_up")
        self.assertEqual("pull_up", gpio_conf.pull_up_down)
        self.assertEqual(None, gpio_conf.bounce_time)
        self.assertEqual(1, gpio_conf.hold_time)
        self.assertEqual(False, gpio_conf.hold_repeat)

        with self.assertRaises(ValueError):
            GpioConfig().deserialize("pull_up,150,2,False,")

    def test_deserialize_pull_up_down(self):
        gpio_conf = GpioConfig().deserialize("   pull_up,150,2,False")
        self.assertEqual("pull_up", gpio_conf.pull_up_down)

        gpio_conf = GpioConfig().deserialize("pull_down   ,150,2,False")
        self.assertEqual("pull_down", gpio_conf.pull_up_down)

        gpio_conf = GpioConfig().deserialize("none,150,2,False")
        self.assertEqual("none", gpio_conf.pull_up_down)

        gpio_conf = GpioConfig().deserialize("none_invert,150,2,False")
        self.assertEqual("none_invert", gpio_conf.pull_up_down)

        with self.assertRaises(ValueError):
            GpioConfig().deserialize(",150,2,False")

        with self.assertRaises(ValueError):
            GpioConfig().deserialize("pull,150,2,False")

    def test_deserialize_bounce_time(self):
        gpio_conf = GpioConfig().deserialize("pull_up,  150  ,2,False")
        self.assertEqual(150, gpio_conf.bounce_time)

        gpio_conf = GpioConfig().deserialize("pull_up,None,2,False")
        self.assertEqual(None, gpio_conf.bounce_time)

        gpio_conf = GpioConfig().deserialize("pull_up")
        self.assertEqual(None, gpio_conf.bounce_time)

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150.0,2,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,ten,2,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,-100,2,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,0,2,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,,2,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,")

    def test_deserialize_hold_time(self):
        gpio_conf = GpioConfig().deserialize("pull_up,150, 2  ,False")
        self.assertEqual(2, gpio_conf.hold_time)

        gpio_conf = GpioConfig().deserialize("pull_up,150, 2.50  ,False")
        self.assertEqual(2.5, gpio_conf.hold_time)

        gpio_conf = GpioConfig().deserialize("pull_up,150")
        self.assertEqual(1, gpio_conf.hold_time)

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150,ten,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150,None,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150,-2,False")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150,,")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150,")

    def test_deserialize_hold_repeat(self):
        gpio_conf = GpioConfig().deserialize("pull_up,150,2,False")
        self.assertEqual(False, gpio_conf.hold_repeat)

        gpio_conf = GpioConfig().deserialize("pull_up,150,2,false")
        self.assertEqual(False, gpio_conf.hold_repeat)

        gpio_conf = GpioConfig().deserialize("pull_up,150,2,True")
        self.assertEqual(True, gpio_conf.hold_repeat)

        gpio_conf = GpioConfig().deserialize("pull_up,150,2,true")
        self.assertEqual(True, gpio_conf.hold_repeat)

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150,2,")

        with self.assertRaises(ValueError):
            gpio_conf = GpioConfig().deserialize("pull_up,150,2,None")

    def test_serialize(self):
        gpio_conf = GpioConfig.tuple_gpioconfig("pull_up", 150, 2, False)
        str = GpioConfig().serialize(gpio_conf)
        self.assertEqual("pull_up,150,2,False", str)

        gpio_conf = GpioConfig.tuple_gpioconfig("pull_down", 150, 2.50, True)
        str = GpioConfig().serialize(gpio_conf)
        self.assertEqual("pull_down,150,2.5,True", str)

        gpio_conf = GpioConfig.tuple_gpioconfig("pull_down", None, 2.50, True)
        str = GpioConfig().serialize(gpio_conf)
        self.assertEqual("pull_down,None,2.5,True", str)

        str = GpioConfig().serialize(None)
        self.assertEqual("", str)
