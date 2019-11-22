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

from mopidy import core

import pykka

from .controls import PhonieboxControls


class PhonieboxIdleTimerFrontend(pykka.ThreadingActor, core.CoreListener):
    """
    Idle-Timer frontend.
    Creates an IdleWatchdog if idle_time_before_shutdown > 0.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, config, core):
        super(PhonieboxIdleTimerFrontend, self).__init__()
        self.core = core
        self.config = config['phoniebox-idletimer']
        self.controls = PhonieboxControls(core)
        self.idle_watchdog = None

    def on_start(self):
        """
        If idle_time_before_shutdown > 0, an IdleWatchdog will be created with
        the specified idle time.
        """
        idle_time = self.config['idle_time_before_shutdown']
        if idle_time > 0:
            from .idle_watchdog import IdleWatchdog
            self.idle_watchdog = IdleWatchdog.start(idle_time, self.controls)
            self.logger.info("idle timer enabled")
        else:
            self.idle_watchdog = None
            self.logger.info("idle timer disabled")

    def on_stop(self):
        """
        Stops the IdleWatchdog if it has been started previously
        """
        if self.idle_watchdog is not None:
            self.idle_watchdog.stop()
