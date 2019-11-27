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

import subprocess
import unittest

import mock

from mopidy.audio import PlaybackState

from mopidy_phoniebox.controls import PhonieboxControls


class PhonieboxControlsTest(unittest.TestCase):

    def test_init(self):
        core = mock.Mock()

        ctrls = PhonieboxControls(core)
        self.assertIs(core, ctrls.core)

    def test_play_pause(self):
        core = mock.Mock()
        future = mock.Mock()
        core.playback.get_state.return_value = future

        ctrls = PhonieboxControls(core)
        future.get.return_value = PlaybackState.PLAYING
        ctrls.play_pause()
        core.playback.pause.assert_called_once()
        core.playback.resume.assert_not_called()
        core.playback.play.assert_not_called()

        core.reset_mock()
        ctrls = PhonieboxControls(core)
        future.get.return_value = PlaybackState.PAUSED
        ctrls.play_pause()
        core.playback.pause.assert_not_called()
        core.playback.resume.assert_called_once()
        core.playback.play.assert_not_called()

        core.reset_mock()
        ctrls = PhonieboxControls(core)
        future.get.return_value = PlaybackState.STOPPED
        ctrls.play_pause()
        core.playback.pause.assert_not_called()
        core.playback.resume.assert_not_called()
        core.playback.play.assert_called_once()

    def test_shutdown(self):
        core = mock.Mock()
        ctrls = PhonieboxControls(core)

        subprocess.call = self.return_ok
        rc = ctrls.shutdown()
        self.assertEqual(0, rc)

        subprocess.call = self.return_notok
        rc = ctrls.shutdown()
        self.assertEqual(1, rc)

    def return_ok(self, *args):
        return 0

    def return_notok(self, *args):
        return 1
