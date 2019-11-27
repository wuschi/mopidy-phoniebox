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

from mopidy_phoniebox import ButtonConfig


class ButtonConfigTest(unittest.TestCase):

    def test_deserialize(self):
        btn_conf = ButtonConfig().deserialize("gpio0,when_pressed")
        self.assertIsInstance(btn_conf, ButtonConfig.tuple_buttonconfig)
        self.assertEqual(0, btn_conf.gpio)
        self.assertEqual("when_pressed", btn_conf.action)

        btn_conf = ButtonConfig().deserialize("gpio0,when_held")
        self.assertIsInstance(btn_conf, ButtonConfig.tuple_buttonconfig)
        self.assertEqual(0, btn_conf.gpio)
        self.assertEqual("when_held", btn_conf.action)

        btn_conf = ButtonConfig().deserialize(None)
        self.assertIsNone(btn_conf)

        btn_conf = ButtonConfig().deserialize("  ")
        self.assertIsNone(btn_conf)

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize("gpio0,when_pressed,")

    def test_deserialize_gpio(self):
        btn_conf = ButtonConfig().deserialize("gpio10,when_pressed")
        self.assertEqual(10, btn_conf.gpio)

        btn_conf = ButtonConfig().deserialize("  gpio10,when_pressed")
        self.assertEqual(10, btn_conf.gpio)

        btn_conf = ButtonConfig().deserialize("gpio10   ,when_pressed")
        self.assertEqual(10, btn_conf.gpio)

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize(",when_pressed")

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize("gio10,when_pressed")

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize("gpio28,when_pressed")

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize("gpio-1,when_pressed")

    def test_deserialize_action(self):
        btn_conf = ButtonConfig().deserialize("gpio0,  when_pressed")
        self.assertEqual("when_pressed", btn_conf.action)

        btn_conf = ButtonConfig().deserialize("gpio0,when_pressed  ")
        self.assertEqual("when_pressed", btn_conf.action)

        btn_conf = ButtonConfig().deserialize("gpio0,when_held")
        self.assertEqual("when_held", btn_conf.action)

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize("gpio0,when_released")

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize("gpio0,wen_pressed")

        with self.assertRaises(ValueError):
            ButtonConfig().deserialize("gpio0")

    def test_serialize(self):
        btn_conf = ButtonConfig.tuple_buttonconfig(0, "when_pressed")
        str = ButtonConfig().serialize(btn_conf)
        self.assertEqual("gpio0,when_pressed", str)

        str = ButtonConfig().serialize(None)
        self.assertEqual("", str)
