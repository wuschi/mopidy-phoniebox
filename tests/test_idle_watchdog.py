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

import mock

from mopidy.audio import PlaybackState

from mopidy_phoniebox.idle_watchdog import IdleWatchdog


class IdleWatchdogTest(unittest.TestCase):

    def test_init(self):
        controls = mock.Mock()

        iw = IdleWatchdog(0, controls)

        self.assertTrue(iw.idle_time == 0)

        iw = IdleWatchdog(1, controls)
        self.assertTrue(iw.idle_time == 1)

    def test_shutdown(self):
        controls = mock.Mock()

        iw = IdleWatchdog(1, controls)
        iw.shutdown()

        controls.shutdown.assert_called_once()

    def test_start_timer(self):
        controls = mock.Mock()

        iw = IdleWatchdog(1, controls)
        self.assertIsNone(iw.timer)

        iw.start_timer()
        self.assertIsNotNone(iw.timer)

        iw.cancel_timer()
        self.assertIsNone(iw.timer)

        iw.start_timer()
        self.assertIsNotNone(iw.timer)
        iw.start_timer()
        self.assertIsNotNone(iw.timer)
        iw.cancel_timer()
        self.assertIsNone(iw.timer)

    def test_playback_state_changed(self):
        controls = mock.Mock()

        iw = IdleWatchdog(1, controls)
        self.assertIsNone(iw.timer)

        iw.playback_state_changed(None, PlaybackState.STOPPED)
        self.assertIsNotNone(iw.timer)

        iw.playback_state_changed(PlaybackState.STOPPED, PlaybackState.PLAYING)
        self.assertIsNone(iw.timer)

        iw.playback_state_changed(PlaybackState.PLAYING, PlaybackState.PAUSED)
        self.assertIsNotNone(iw.timer)

        iw.playback_state_changed(PlaybackState.PAUSED, PlaybackState.PLAYING)
        self.assertIsNone(iw.timer)

    def test_on_start(self):
        controls = mock.Mock()
        future = mock.Mock()

        controls.core.playback.get_state.return_value = future

        iw = IdleWatchdog(1, controls)
        future.get.return_value = PlaybackState.STOPPED
        iw.on_start()
        controls.core.playback.get_state.assert_called_once()
        future.get.assert_called_once()
        self.assertIsNotNone(iw.timer)
        iw.cancel_timer()

        future.reset_mock()
        iw = IdleWatchdog(1, controls)
        future.get.return_value = PlaybackState.PLAYING
        iw.on_start()
        future.get.assert_called_once()
        self.assertIsNone(iw.timer)
        iw.cancel_timer()

    def test_on_stop(self):
        controls = mock.Mock()

        iw = IdleWatchdog(1, controls)
        iw.start_timer()
        self.assertIsNotNone(iw.timer)
        iw.on_stop()
        self.assertIsNone(iw.timer)
