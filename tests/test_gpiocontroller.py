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

from mopidy_phoniebox import FunctionConfig, GpioConfig
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
        config = {
            'gpio27': GpioConfig().deserialize("pull_up"),
            'gpio27.when_pressed': FunctionConfig().deserialize('play_pause')
        }
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
        config = {
            'gpio27': GpioConfig().deserialize("pull_up"),
            'gpio27.when_held': FunctionConfig().deserialize('play_pause')
        }
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
        config = {
            'gpio27': GpioConfig().deserialize(''),
            'gpio27.when_held': FunctionConfig().deserialize('play_pause')
        }
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
                mock.call(0, 'when_pressed'),
                mock.call(0, 'when_released'),
                mock.call(0, 'when_held'),
                mock.call(1, 'when_pressed'),
                mock.call(1, 'when_released'),
                mock.call(1, 'when_held'),
                mock.call(2, 'when_pressed'),
                mock.call(2, 'when_released'),
                mock.call(2, 'when_held'),
                mock.call(3, 'when_pressed'),
                mock.call(3, 'when_released'),
                mock.call(3, 'when_held'),
                mock.call(4, 'when_pressed'),
                mock.call(4, 'when_released'),
                mock.call(4, 'when_held'),
                mock.call(5, 'when_pressed'),
                mock.call(5, 'when_released'),
                mock.call(5, 'when_held'),
                mock.call(6, 'when_pressed'),
                mock.call(6, 'when_released'),
                mock.call(6, 'when_held'),
                mock.call(7, 'when_pressed'),
                mock.call(7, 'when_released'),
                mock.call(7, 'when_held'),
                mock.call(8, 'when_pressed'),
                mock.call(8, 'when_released'),
                mock.call(8, 'when_held'),
                mock.call(9, 'when_pressed'),
                mock.call(9, 'when_released'),
                mock.call(9, 'when_held'),
                mock.call(10, 'when_pressed'),
                mock.call(10, 'when_released'),
                mock.call(10, 'when_held'),
                mock.call(11, 'when_pressed'),
                mock.call(11, 'when_released'),
                mock.call(11, 'when_held'),
                mock.call(12, 'when_pressed'),
                mock.call(12, 'when_released'),
                mock.call(12, 'when_held'),
                mock.call(13, 'when_pressed'),
                mock.call(13, 'when_released'),
                mock.call(13, 'when_held'),
                mock.call(14, 'when_pressed'),
                mock.call(14, 'when_released'),
                mock.call(14, 'when_held'),
                mock.call(15, 'when_pressed'),
                mock.call(15, 'when_released'),
                mock.call(15, 'when_held'),
                mock.call(16, 'when_pressed'),
                mock.call(16, 'when_released'),
                mock.call(16, 'when_held'),
                mock.call(17, 'when_pressed'),
                mock.call(17, 'when_released'),
                mock.call(17, 'when_held'),
                mock.call(18, 'when_pressed'),
                mock.call(18, 'when_released'),
                mock.call(18, 'when_held'),
                mock.call(19, 'when_pressed'),
                mock.call(19, 'when_released'),
                mock.call(19, 'when_held'),
                mock.call(20, 'when_pressed'),
                mock.call(20, 'when_released'),
                mock.call(20, 'when_held'),
                mock.call(21, 'when_pressed'),
                mock.call(21, 'when_released'),
                mock.call(21, 'when_held'),
                mock.call(22, 'when_pressed'),
                mock.call(22, 'when_released'),
                mock.call(22, 'when_held'),
                mock.call(23, 'when_pressed'),
                mock.call(23, 'when_released'),
                mock.call(23, 'when_held'),
                mock.call(24, 'when_pressed'),
                mock.call(24, 'when_released'),
                mock.call(24, 'when_held'),
                mock.call(25, 'when_pressed'),
                mock.call(25, 'when_released'),
                mock.call(25, 'when_held'),
                mock.call(26, 'when_pressed'),
                mock.call(26, 'when_released'),
                mock.call(26, 'when_held'),
                mock.call(27, 'when_pressed'),
                mock.call(27, 'when_released'),
                mock.call(27, 'when_held')
            ]
        )

        # assert all configure_button() are called even when ValueErrors raised
        controller.configure_button = mock.Mock()
        controller.configure_button.side_effect = ValueError
        controller.configure_buttons()
        controller.configure_button.assert_has_calls(
            [
                mock.call(0, 'when_pressed'),
                mock.call(0, 'when_released'),
                mock.call(0, 'when_held'),
                mock.call(1, 'when_pressed'),
                mock.call(1, 'when_released'),
                mock.call(1, 'when_held'),
                mock.call(2, 'when_pressed'),
                mock.call(2, 'when_released'),
                mock.call(2, 'when_held'),
                mock.call(3, 'when_pressed'),
                mock.call(3, 'when_released'),
                mock.call(3, 'when_held'),
                mock.call(4, 'when_pressed'),
                mock.call(4, 'when_released'),
                mock.call(4, 'when_held'),
                mock.call(5, 'when_pressed'),
                mock.call(5, 'when_released'),
                mock.call(5, 'when_held'),
                mock.call(6, 'when_pressed'),
                mock.call(6, 'when_released'),
                mock.call(6, 'when_held'),
                mock.call(7, 'when_pressed'),
                mock.call(7, 'when_released'),
                mock.call(7, 'when_held'),
                mock.call(8, 'when_pressed'),
                mock.call(8, 'when_released'),
                mock.call(8, 'when_held'),
                mock.call(9, 'when_pressed'),
                mock.call(9, 'when_released'),
                mock.call(9, 'when_held'),
                mock.call(10, 'when_pressed'),
                mock.call(10, 'when_released'),
                mock.call(10, 'when_held'),
                mock.call(11, 'when_pressed'),
                mock.call(11, 'when_released'),
                mock.call(11, 'when_held'),
                mock.call(12, 'when_pressed'),
                mock.call(12, 'when_released'),
                mock.call(12, 'when_held'),
                mock.call(13, 'when_pressed'),
                mock.call(13, 'when_released'),
                mock.call(13, 'when_held'),
                mock.call(14, 'when_pressed'),
                mock.call(14, 'when_released'),
                mock.call(14, 'when_held'),
                mock.call(15, 'when_pressed'),
                mock.call(15, 'when_released'),
                mock.call(15, 'when_held'),
                mock.call(16, 'when_pressed'),
                mock.call(16, 'when_released'),
                mock.call(16, 'when_held'),
                mock.call(17, 'when_pressed'),
                mock.call(17, 'when_released'),
                mock.call(17, 'when_held'),
                mock.call(18, 'when_pressed'),
                mock.call(18, 'when_released'),
                mock.call(18, 'when_held'),
                mock.call(19, 'when_pressed'),
                mock.call(19, 'when_released'),
                mock.call(19, 'when_held'),
                mock.call(20, 'when_pressed'),
                mock.call(20, 'when_released'),
                mock.call(20, 'when_held'),
                mock.call(21, 'when_pressed'),
                mock.call(21, 'when_released'),
                mock.call(21, 'when_held'),
                mock.call(22, 'when_pressed'),
                mock.call(22, 'when_released'),
                mock.call(22, 'when_held'),
                mock.call(23, 'when_pressed'),
                mock.call(23, 'when_released'),
                mock.call(23, 'when_held'),
                mock.call(24, 'when_pressed'),
                mock.call(24, 'when_released'),
                mock.call(24, 'when_held'),
                mock.call(25, 'when_pressed'),
                mock.call(25, 'when_released'),
                mock.call(25, 'when_held'),
                mock.call(26, 'when_pressed'),
                mock.call(26, 'when_released'),
                mock.call(26, 'when_held'),
                mock.call(27, 'when_pressed'),
                mock.call(27, 'when_released'),
                mock.call(27, 'when_held')
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
        controller.configure_button(27, 'when_held')
        controller.configure_button(27, 'when_released')

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'gpio27': None}
        controller.configure_button(27, 'when_released')
        controller.configure_button(27, 'when_held')

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {'gpio27': ''}
        controller.configure_button(27, 'when_released')
        controller.configure_button(27, 'when_held')

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.config = {
            'gpio27.when_pressed': FunctionConfig().deserialize('play_pause')
        }
        controller.configure_button(27, 'when_held')
        with self.assertRaises(ValueError):
            controller.configure_button(27, 'when_pressed')

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.config = {
            'gpio0.when_pressed': FunctionConfig().deserialize('unknown_fn')
        }
        with self.assertRaises(ValueError):
            controller.configure_button(0, 'when_pressed')

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.config = {
            'gpio0.when_pressed': FunctionConfig().deserialize('play_pause')
        }
        controller.configure_button(0, 'when_pressed')
        self.assertIsNotNone(controller.gpios[0].when_pressed)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.gpios[0].when_pressed = lambda x: x
        controller.config = {
            'gpio0.when_pressed': FunctionConfig().deserialize('play_pause')
        }
        with self.assertRaises(ValueError):
            controller.configure_button(0, 'when_pressed')

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.config = {
            'gpio0.when_held': FunctionConfig().deserialize(' play_pause ')
        }
        controller.configure_button(0, 'when_held')
        self.assertIsNotNone(controller.gpios[0].when_held)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.gpios[0].when_held = lambda x: x
        controller.config = {
            'gpio0.when_held': FunctionConfig().deserialize('play_pause')
        }
        with self.assertRaises(ValueError):
            controller.configure_button(0, 'when_held')

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.config = {
            'gpio0.when_released': FunctionConfig().deserialize(' play_pause ')
        }
        controller.configure_button(0, 'when_released')
        self.assertIsNotNone(controller.gpios[0].when_released)

        Device.pin_factory.reset()
        controller.gpios = [None] * 28
        controller.gpios[0] = Button(0)
        controller.gpios[0].when_released = lambda x: x
        controller.config = {
            'gpio0.when_released': FunctionConfig().deserialize('play_pause')
        }
        with self.assertRaises(ValueError):
            controller.configure_button(0, 'when_released')

    def test_on_held(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        Device.pin_factory.reset()
        btn = Button(0)
        controller.on_held(btn, controls.some_fn)
        self.assertTrue(btn.was_held)
        controls.some_fn.assert_called_once()

    def test_on_released(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        Device.pin_factory.reset()
        btn = Button(0)
        self.assertFalse(btn.was_held)
        controller.on_released(btn, controls.some_fn)
        self.assertFalse(btn.was_held)
        controls.some_fn.assert_called_once()

        controls.reset_mock()
        Device.pin_factory.reset()
        btn.was_held = True
        controller.on_released(btn, controls.some_fn)
        self.assertFalse(btn.was_held)
        controls.some_fn.assert_not_called()

    def test_gpiocontrols_volume_up(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.volume_up(**args)
        controls.volume_up.assert_called_once()

        args = {'vol_step': 3}
        controller.controls.volume_up(**args)
        controls.volume_up.assert_called_with(3)

    def test_gpiocontrols_volume_down(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.volume_down(**args)
        controls.volume_down.assert_called_once()

        args = {'vol_step': 3}
        controller.controls.volume_down(**args)
        controls.volume_down.assert_called_with(3)

    def test_gpiocontrols_mute_unmute(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.mute_unmute(**args)
        controls.mute_unmute.assert_called_once()

    def test_gpiocontrols_shutdown(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.shutdown(**args)
        controls.shutdown.assert_called_once()

    def test_gpiocontrols_play_pause(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.play_pause(**args)
        controls.play_pause.assert_called_once()

    def test_gpiocontrols_cd_previous(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.cd_previous(**args)
        controls.cd_previous.assert_called_once()

    def test_gpiocontrols_previous(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.previous(**args)
        controls.previous.assert_called_once()

    def test_gpiocontrols_next(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.next(**args)
        controls.next.assert_called_once()

    def test_gpiocontrols_seek_bwd(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.seek_bwd(**args)
        controls.seek_bwd.assert_called_once()

        args = {'seconds': 3}
        controller.controls.seek_bwd(**args)
        controls.seek_bwd.assert_called_with(3)

    def test_gpiocontrols_seek_fwd(self):
        config = {}
        controls = mock.Mock()
        controller = GpioController(config, controls)

        args = {}
        controller.controls.seek_fwd(**args)
        controls.seek_fwd.assert_called_once()

        args = {'seconds': 3}
        controller.controls.seek_fwd(**args)
        controls.seek_fwd.assert_called_with(3)
