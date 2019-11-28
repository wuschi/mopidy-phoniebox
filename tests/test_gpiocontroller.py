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

import time
import unittest

from gpiozero import Button, Device
from gpiozero.pins.mock import MockFactory

import mock

from mopidy_phoniebox import ButtonConfig, GpioConfig
from mopidy_phoniebox.gpiocontroller import GpioController


class GpioControllerTest(unittest.TestCase):

    Device.pin_factory = MockFactory()

    def test_init(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)
        for gpio in range(28):
            self.assertIsNone(controller.gpios[gpio])

        Device.pin_factory.reset()
        controls.reset_mock()
        config = {}
        for gpio in range(28):
            config['gpio{:d}'.format(gpio)] = None
        controller = GpioController(config, controls)
        for gpio in range(28):
            self.assertIsNone(controller.gpios[gpio])

        Device.pin_factory.reset()
        controls.reset_mock()
        config = {'gpio27': GpioConfig().deserialize("pull_up"),
                  'play_pause': ButtonConfig().deserialize(
                      'gpio27,when_pressed')}
        controller = GpioController(config, controls)
        for gpio in range(27):
            self.assertIsNone(controller.gpios[gpio])
        self.assertIsNotNone(controller.gpios[27])
        self.assertTrue(controller.gpios[27].pull_up)
        self.assertEqual(1, controller.gpios[27].hold_time)
        self.assertFalse(controller.gpios[27].hold_repeat)
        self.assertIsNotNone(controller.gpios[27].when_pressed)
        self.assertIsNone(controller.gpios[27].when_held)

        btn_pin = Device.pin_factory.pin(27)
        btn_pin.drive_low()
        time.sleep(0.1)
        btn_pin.drive_high()
        controls.play_pause.assert_called_once()

        Device.pin_factory.reset()
        controls.reset_mock()
        config = {'gpio27': GpioConfig().deserialize("pull_up"),
                  'play_pause': ButtonConfig().deserialize('gpio27,when_held')}
        controller = GpioController(config, controls)
        for gpio in range(27):
            self.assertIsNone(controller.gpios[gpio])
        self.assertIsNotNone(controller.gpios[27])
        self.assertTrue(controller.gpios[27].pull_up)
        self.assertEqual(1, controller.gpios[27].hold_time)
        self.assertFalse(controller.gpios[27].hold_repeat)
        self.assertIsNone(controller.gpios[27].when_pressed)
        self.assertIsNotNone(controller.gpios[27].when_held)

        btn_pin = Device.pin_factory.pin(27)
        btn_pin.drive_low()
        time.sleep(0.1)
        btn_pin.drive_high()
        time.sleep(0.2)
        controls.play_pause.assert_not_called()

        btn_pin.drive_low()
        time.sleep(1.2)
        btn_pin.drive_high()
        time.sleep(0.2)
        controls.play_pause.assert_called_once()

        Device.pin_factory.reset()
        controls.reset_mock()
        config = {'gpio27': GpioConfig().deserialize(''),
                  'play_pause': ButtonConfig().deserialize('gpio27,when_held')}
        controller = GpioController(config, controls)
        for gpio in range(27):
            self.assertIsNone(controller.gpios[gpio])
        self.assertIsNone(controller.gpios[27])

    def test_configure_gpios(self):
        Device.pin_factory.reset()
        controls = mock.Mock()
        config = {}
        controller = GpioController(config, controls)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'gpio27': GpioConfig().deserialize("pull_up,150")}
        controller.configure_gpios()
        for gpio in range(27):
            self.assertIsNone(controller.gpios[gpio])
        self.assertIsNotNone(controller.gpios[27])
        self.assertTrue(controller.gpios[27].pull_up)
        self.assertEqual(1, controller.gpios[27].hold_time)
        self.assertFalse(controller.gpios[27].hold_repeat)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'gpio27': GpioConfig().deserialize("pull_down")}
        controller.configure_gpios()
        for gpio in range(27):
            self.assertIsNone(controller.gpios[gpio])
        self.assertIsNotNone(controller.gpios[27])
        self.assertFalse(controller.gpios[27].pull_up)
        self.assertEqual(1, controller.gpios[27].hold_time)
        self.assertFalse(controller.gpios[27].hold_repeat)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'gpio27': GpioConfig().deserialize("none")}
        controller.configure_gpios()
        for gpio in range(27):
            self.assertIsNone(controller.gpios[gpio])
        self.assertIsNotNone(controller.gpios[27])
        self.assertIsNone(controller.gpios[27].pull_up)
        self.assertEqual(1, controller.gpios[27].hold_time)
        self.assertFalse(controller.gpios[27].hold_repeat)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'gpio27': GpioConfig().deserialize("none_invert")}
        controller.configure_gpios()
        for gpio in range(27):
            self.assertIsNone(controller.gpios[gpio])
        self.assertIsNotNone(controller.gpios[27])
        self.assertIsNone(controller.gpios[27].pull_up)
        self.assertEqual(1, controller.gpios[27].hold_time)
        self.assertFalse(controller.gpios[27].hold_repeat)

    def test_configure_buttons(self):
        controls = mock.Mock()
        config = {}
        controller = GpioController(config, controls)

        controller.configure_button = mock.Mock()
        controller.configure_buttons()
        controller.configure_button.assert_has_calls(
            [
                mock.call('play_pause', controls.play_pause),
                mock.call('cdprev', controls.cd_previous),
                mock.call('prev', controls.previous),
                mock.call('next', controls.next)
            ]
        )

        # assert all configure_button() are called even when ValueErrors raised
        controller.configure_button = mock.Mock()
        controller.configure_button.side_effect = ValueError
        controller.configure_buttons()
        controller.configure_button.assert_has_calls(
            [
                mock.call('play_pause', controls.play_pause),
                mock.call('cdprev', controls.cd_previous),
                mock.call('prev', controls.previous),
                mock.call('next', controls.next)
            ]
        )

    def test_configure_button(self):
        controls = mock.Mock()
        config = {}
        controller = GpioController(config, controls)

        # no config set, should pass without changes
        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {}
        controller.configure_button('play_pause', controls.play_pause)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'play_pause': ButtonConfig().deserialize('')}
        controller.configure_button('play_pause', controls.play_pause)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'play_pause': ButtonConfig().deserialize(
            'gpio0,when_pressed')}
        with self.assertRaises(ValueError):
            controller.configure_button('play_pause', controls.play_pause)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.config = {'play_pause': ButtonConfig().deserialize(
            'gpio0,when_pressed')}
        controller.configure_button('play_pause', controls.play_pause)
        self.assertIsNotNone(controller.gpios[0].when_pressed)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.gpios[0].when_pressed = lambda x: x
        controller.config = {'play_pause': ButtonConfig().deserialize(
            'gpio0,when_pressed')}
        with self.assertRaises(ValueError):
            controller.configure_button('play_pause', controls.play_pause)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.config = {'play_pause': ButtonConfig().deserialize(
            'gpio0,when_held')}
        controller.configure_button('play_pause', controls.play_pause)
        self.assertIsNotNone(controller.gpios[0].when_held)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.gpios[0].when_held = lambda x: x
        controller.config = {'play_pause': ButtonConfig().deserialize(
            'gpio0,when_held')}
        with self.assertRaises(ValueError):
            controller.configure_button('play_pause', controls.play_pause)
