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
    fn_mapping = None

    def __init__(self, config, controls):
        self.config = config
        self.controls = controls
        self.gpios = [None] * 28

        self.fn_mapping = {
            "shutdown": self.controls.shutdown,
            "play_pause": self.controls.play_pause,
            "cdprev": self.controls.cd_previous,
            "prev": self.controls.previous,
            "next": self.controls.next,
            "vol_down": self.controls.volume_down,
            "vol_up": self.controls.volume_up
        }
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
        for gpio in range(28):
            for action in "when_pressed", "when_released", "when_held":
                try:
                    self.configure_button(gpio, action)
                except ValueError as e:
                    self.logger.error(str(e))

    def configure_button(self, gpio, action):
        """
        Configures a single button function.

        :param gpio: the gpio number
        :param action: the action to configure (when_pressed or when_held)
        """

        key = "gpio{:d}.{}".format(gpio, action)
        try:
            fn_type = self.config[key]
        except KeyError:
            fn_type = None

        if fn_type is None:
            return

        try:
            fn = self.fn_mapping[fn_type.strip()]
        except KeyError:
            raise ValueError(
                    "cannot assign gpio{:d}.{}: unknown fn type '{}'".format(
                        gpio, action, fn_type))

        btn = self.gpios[gpio]
        if btn is None:
            raise ValueError(("cannot configure {:d}.{}"
                              + " - gpio{:d} not configured").format(
                                  gpio, action, gpio))

        if action == 'when_pressed':
            if btn.when_pressed is not None:
                raise ValueError(("cannot assign {} to gpio{:d}.when_pressed:"
                                  + " already assigned").format(
                                      fn_type, gpio))
            btn.when_pressed = lambda: fn()
        elif action == 'when_released':
            if btn.when_released is not None:
                raise ValueError(("cannot assign {} to gpio{:d}.when_released:"
                                  + " already assigned").format(
                                      fn_type, gpio))
            btn.when_released = lambda: fn()
        elif action == 'when_held':
            if btn.when_held is not None:
                raise ValueError(("cannot assign {} to gpio{:d}.when_held:"
                                  + " already assigned").format(
                                      fn_type, gpio))
            btn.when_held = lambda: fn()

        self.logger.info("{} assigned to gpio{:d}.{}".format(
            fn_type, gpio, action))
