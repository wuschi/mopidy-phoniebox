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
    Button.was_held = False
    config = None
    controls = None
    gpios = None
    logger = logging.getLogger(__name__)
    fn_mapping = None

    def __init__(self, config, controls):
        self.config = config
        self.controls = GpioControls(controls)
        self.gpios = [None] * 28

        self.fn_mapping = {
            "shutdown": self.controls.shutdown,
            "play_pause": self.controls.play_pause,
            "cdprev": self.controls.cd_previous,
            "prev": self.controls.previous,
            "next": self.controls.next,
            "seek_bwd": self.controls.seek_bwd,
            "seek_fwd": self.controls.seek_fwd,
            "vol_down": self.controls.volume_down,
            "vol_up": self.controls.volume_up,
            "mute": self.controls.mute_unmute
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
            fn_conf = self.config[key]
        except KeyError:
            fn_conf = None

        if fn_conf is None:
            return

        try:
            fn = self.fn_mapping[fn_conf.fn_type.strip()]
        except KeyError:
            raise ValueError(
                    "cannot assign gpio{:d}.{}: unknown fn type '{}'".format(
                        gpio, action, fn_conf.fn_type))

        btn = self.gpios[gpio]
        fn_type = fn_conf.fn_type
        fn_args = fn_conf.fn_args
        if btn is None:
            raise ValueError(("cannot configure {:d}.{}"
                              + " - gpio{:d} not configured").format(
                                  gpio, action, gpio))

        if action == 'when_pressed':
            if btn.when_pressed is not None:
                raise ValueError(("cannot assign {} to gpio{:d}.when_pressed:"
                                  + " already assigned").format(
                                      fn_type, gpio))
            btn.when_pressed = lambda: fn(**fn_args)
        elif action == 'when_released':
            if btn.when_released is not None:
                raise ValueError(("cannot assign {} to gpio{:d}.when_released:"
                                  + " already assigned").format(
                                      fn_type, gpio))
            btn.when_released = lambda bt: self.on_released(bt, fn, **fn_args)
        elif action == 'when_held':
            if btn.when_held is not None:
                raise ValueError(("cannot assign {} to gpio{:d}.when_held:"
                                  + " already assigned").format(
                                      fn_type, gpio))
            btn.when_held = lambda bt: self.on_held(bt, fn, **fn_args)

        self.logger.info("{} assigned to gpio{:d}.{}".format(
            fn_type, gpio, action))

    def on_held(self, btn, fn, **fn_args):
        """
        Wrapper around a buttons when_held fn.

        :param btn: the button that was held
        :param fn: the function to wrap
        """
        btn.was_held = True
        self.logger.debug("{} is held".format(btn))
        fn(**fn_args)

    def on_released(self, btn, fn, **fn_args):
        """
        Wrapper around a buttons when_released fn. Only executes the wrapped
        function when the button does not have a when_held function or the
        button was not held previously.

        :param btn: the button that was released
        :param fn: the function to wrap
        """
        if btn.was_held:
            btn.was_held = False
            self.logger.debug("{} is released but was held".format(btn))
        else:
            self.logger.debug("{} is released and was not held".format(btn))
            fn(**fn_args)


class GpioControls():
    """
    Wrapper around the `PhonieboxControls` which accepts `**kwargs` in it's
    methods for passing optional parameters.
    """

    controls = None

    def __init__(self, controls):
        self.controls = controls

    def shutdown(self, **kwargs):
        """
        Wraps `PhonieboxControls.shutdown()`. No optional parameters accepted.
        """
        self.controls.shutdown()

    def play_pause(self, **kwargs):
        """
        Wraps `PhonieboxControls.play_pause()`. No optional parameters
        accepted.
        """
        self.controls.play_pause()

    def cd_previous(self, **kwargs):
        """
        Wraps `PhonieboxControls.cd_previous()`. No optional parameters
        accepted.
        """
        self.controls.cd_previous()

    def previous(self, **kwargs):
        """
        Wraps `PhonieControls.previous()`. No optional parameters accepted.
        """
        self.controls.previous()

    def next(self, **kwargs):
        """
        Wraps `PhonieControls.next()`. No optional parameters accepted.
        """
        self.controls.next()

    def seek_bwd(self, **kwargs):
        """
        Wraps `PhonieboxControls.seek_bwd()`. Uses the following optional
        parameters:

        - `seconds`: The number of seconds to seek backwards
        """
        try:
            seconds = kwargs['seconds']
            self.controls.seek_bwd(seconds)
        except KeyError:
            self.controls.seek_bwd()

    def seek_fwd(self, **kwargs):
        """
        Wraps `PhonieboxControls.seek_fwd()`. Uses the following optional
        parameters:

        - `seconds`: The number of seconds to seek forwards
        """
        try:
            seconds = kwargs['seconds']
            self.controls.seek_fwd(seconds)
        except KeyError:
            self.controls.seek_fwd()

    def volume_down(self, **kwargs):
        """
        Wraps `PhonieboxControls.volume_down()`. Uses the following optional
        parameters:

        - `vol_step`: The percentage to decrease the volume by.
        """
        try:
            vol_step = kwargs['vol_step']
            self.controls.volume_down(vol_step)
        except KeyError:
            self.controls.volume_down()

    def volume_up(self, **kwargs):
        """
        Wraps `PhonieboxControls.volume_up()`. Uses the following optional
        parameters:

        - `vol_step`: The percentage to increase the volume by.
        """
        try:
            vol_step = kwargs['vol_step']
            self.controls.volume_up(vol_step)
        except KeyError:
            self.controls.volume_up()

    def mute_unmute(self, **kwargs):
        """
        Wraps `PhonieboxControls.mute_unmute()`. No optional parameters
        accepted.
        """
        self.controls.mute_unmute()
