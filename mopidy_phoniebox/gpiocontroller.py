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
import logging

from gpiozero import Button


class GpioController:
    """
    Sets up gpios and button functions
    """
    config = None
    controls = None
    gpios = None
    logger = logging.getLogger(__name__)

    def __init__(self, config, controls):
        self.config = config
        self.controls = controls
        self.gpios = [None] * 28

        self.configure_gpios()
        self.configure_buttons()

    def configure_gpios(self):
        """
        Configures the gpios.
        """
        for gpio in range(28):
            key = "gpio{:d}".format(gpio)
            try:
                gpioconfig = self.config[key]
            except KeyError:
                continue
            if gpioconfig is None:
                continue

            if gpioconfig.pull_up_down == "pull_up":
                pull_up = True
                active_state = None
            elif gpioconfig.pull_up_down == "pull_down":
                pull_up = False
                active_state = None
            elif gpioconfig.pull_up_down == "none_invert":
                pull_up = None
                active_state = False
            else:  # none
                pull_up = None
                active_state = True

            bounce_time = gpioconfig.bounce_time
            if bounce_time is not None:
                bounce_time = float(bounce_time) / 1000
            hold_time = gpioconfig.hold_time
            hold_repeat = gpioconfig.hold_repeat

            self.gpios[gpio] = Button(gpio, pull_up, active_state,
                                      bounce_time, hold_time, hold_repeat)

    def configure_buttons(self):
        """
        Configures all button functions.
        """
        try:
            self.configure_button("shutdown", self.controls.shutdown)
        except ValueError as e:
            self.logger.error(str(e))

        try:
            self.configure_button("play_pause", self.controls.play_pause)
        except ValueError as e:
            self.logger.error(str(e))

        try:
            self.configure_button("cdprev", self.controls.cd_previous)
        except ValueError as e:
            self.logger.error(str(e))

        try:
            self.configure_button("prev", self.controls.previous)
        except ValueError as e:
            self.logger.error(str(e))

        try:
            self.configure_button("next", self.controls.next)
        except ValueError as e:
            self.logger.error(str(e))

        try:
            self.configure_button("vol_down", self.controls.volume_down)
        except ValueError as e:
            self.logger.error(str(e))

        try:
            self.configure_button("vol_up", self.controls.volume_up)
        except ValueError as e:
            self.logger.error(str(e))

    def configure_button(self, fn_type, fn):
        """
        Configures a single button function.

        :param fn_type: the button function type
        :param fn: the function to execute when the button is pressed
        """
        try:
            btn_conf = self.config[fn_type]
        except KeyError:
            btn_conf = None

        if btn_conf is None:
            return

        btn = self.gpios[btn_conf.gpio]
        if btn is None:
            raise ValueError(("cannot configure {} button"
                              + " - gpio {:d} not configured").format(
                                  fn_type, btn_conf.gpio))
        if btn_conf.action == 'when_pressed':
            if btn.when_pressed is not None:
                raise ValueError(("cannot assign action when_pressed for {}: "
                                  + "gpio {:d} already assigned").format(
                                      fn_type, btn_conf.gpio))
            btn.when_pressed = lambda: fn()
        elif btn_conf.action == 'when_held':
            if btn.when_held is not None:
                raise ValueError(("cannot assign action when_held for {}: "
                                  + "gpio {:d} already assigned").format(
                                      fn_type, btn_conf.gpio))
            btn.when_held = lambda: fn()
        self.logger.info("{} assigned to gpio {} ({})".format(
            fn_type, btn_conf.gpio, btn_conf.action))
