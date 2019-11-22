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
from threading import Timer

import pykka

from mopidy import core
from mopidy.audio import PlaybackState

logger = logging.getLogger(__name__)


class IdleWatchdog(pykka.ThreadingActor, core.CoreListener):
    """
    Watches the playback state of mopidy and starts/cancels a shutdown timer
    accordingly.
    """
    def __init__(self, idle_time, controls):
        super(IdleWatchdog, self).__init__()
        self.idle_time = idle_time
        self.controls = controls
        self.timer = None

    def cancel_timer(self):
        """
        Cancels the shutdown timer if present.
        """
        if self.timer is not None:
            logger.info("cancelling shutdown timer")
            self.timer.cancel()
            self.timer = None

    def start_timer(self):
        """
        Starts the shutdown timer.
        """
        if self.timer is not None:
            logger.warn("starting timer altough previous one exists "
                        + "- this shouldn't happen")
            self.cancel_timer()
        self.timer = Timer(self.idle_time * 60, self.shutdown)
        self.timer.start()

    def playback_state_changed(self, old_state, new_state):
        """
        Called by mopidy when the playback state has changed.
        If the state changes to PLAYING, the timer is cancelled. If the state
        changed to STOPPED or PAUSED and mopidy was playing previously, then
        the timer is started.
        """
        logger.debug("playback state changed from %s to %s",
                     old_state, new_state)
        if new_state == PlaybackState.PLAYING:
            self.cancel_timer()
        elif old_state == PlaybackState.PLAYING or old_state is None:
            logger.info("starting %s minute shutdown timer (state: %s)",
                        self.idle_time, new_state)
            self.start_timer()

    def shutdown(self):
        """
        Called when the timer has finished. Executes the shutdown.
        """
        self.controls.shutdown()

    def on_start(self):
        """
        Called when the idle watchdog is initialized.
        """
        core = self.controls.core
        self.playback_state_changed(None, core.playback.get_state().get())

    def on_stop(self):
        """
        Called when the idle watchdog is destroyed.
        """
        if self.timer is not None:
            self.timer.cancel()
