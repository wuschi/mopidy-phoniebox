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
from mopidy.models import TlTrack

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

    def test_cd_previous(self):
        core = mock.Mock()
        future = mock.Mock()
        core.playback.get_time_position.return_value = future
        future_tl_track = mock.Mock()
        core.playback.get_current_tl_track.return_value = future_tl_track
        future_tl = mock.Mock()
        core.tracklist.get_length.return_value = future_tl
        future_tl.get.return_value = 3

        ctrls = PhonieboxControls(core)
        future.get.return_value = 1000
        future_tl_track.get.return_value = TlTrack(2, None)
        ctrls.cd_previous()
        core.playback.previous.assert_called_once()
        core.playback.seek.assert_not_called()
        core.playback.play.assert_not_called()

        core.reset_mock()
        ctrls = PhonieboxControls(core)
        future.get.return_value = 1000
        future_tl_track.get.return_value = TlTrack(1, None)
        ctrls.cd_previous()
        core.playback.previous.assert_not_called()
        core.playback.seek.assert_not_called()
        core.playback.play.assert_called_with(tlid=3)

        core.reset_mock()
        future.get.return_value = 4000
        future_tl_track.get.return_value = TlTrack(2, None)
        ctrls.cd_previous()
        core.playback.previous.assert_not_called()
        core.playback.seek.assert_called_with(0)
        core.playback.play.assert_not_called()

        future_tl.get.return_value = 0
        core.reset_mock()
        future.get.return_value = 4000
        future_tl_track.get.return_value = None
        ctrls.cd_previous()
        core.playback.previous.assert_not_called()
        core.playback.seek.assert_not_called()
        core.playback.play.assert_not_called()

        future_tl.get.return_value = 0
        core.reset_mock()
        future.get.return_value = 4000
        future_tl_track.get.return_value = TlTrack(1, None)
        ctrls.cd_previous()
        core.playback.previous.assert_not_called()
        core.playback.seek.assert_not_called()
        core.playback.play.assert_not_called()

        future_tl.get.return_value = 3
        core.reset_mock()
        future.get.return_value = 4000
        future_tl_track.get.return_value = None
        ctrls.cd_previous()
        core.playback.previous.assert_not_called()
        core.playback.seek.assert_not_called()
        core.playback.play.assert_called_with(tlid=3)

    def test_previous(self):
        core = mock.Mock()
        future_tl_track = mock.Mock()
        core.playback.get_current_tl_track.return_value = future_tl_track
        future_tl = mock.Mock()
        core.tracklist.get_length.return_value = future_tl
        future_tl.get.return_value = 3

        ctrls = PhonieboxControls(core)
        future_tl_track.get.return_value = TlTrack(2, None)
        ctrls.previous()
        core.playback.previous.assert_called_once()
        core.playback.seek.assert_not_called()

        core.reset_mock()
        future_tl_track.get.return_value = TlTrack(1, None)
        ctrls.previous()
        core.playback.previous.assert_not_called()
        core.playback.play.assert_called_with(tlid=3)

        future_tl.get.return_value = 0
        core.reset_mock()
        future_tl_track.get.return_value = None
        ctrls.previous()
        core.playback.previous.assert_not_called()
        core.playback.play.assert_not_called()

        future_tl.get.return_value = 0
        core.reset_mock()
        future_tl_track.get.return_value = TlTrack(1, None)
        ctrls.previous()
        core.playback.previous.assert_not_called()
        core.playback.play.assert_not_called()

        future_tl.get.return_value = 3
        core.reset_mock()
        future_tl_track.get.return_value = None
        ctrls.previous()
        core.playback.previous.assert_not_called()
        core.playback.play.assert_called_with(tlid=3)

    def test_next(self):
        core = mock.Mock()
        future_tl_track = mock.Mock()
        future_tl = mock.Mock()
        core.playback.get_current_tl_track.return_value = future_tl_track
        core.tracklist.get_length.return_value = future_tl
        future_tl.get.return_value = 3

        ctrls = PhonieboxControls(core)
        future_tl_track.get.return_value = TlTrack(2, None)
        ctrls.next()
        core.playback.next.assert_called_once()
        core.playback.play.assert_not_called()

        core.reset_mock()
        future_tl_track.get.return_value = TlTrack(3, None)
        ctrls.next()
        core.playback.next.assert_not_called()
        core.playback.play.assert_called_with(tlid=1)

        future_tl.get.return_value = 1
        core.reset_mock()
        future_tl_track.get.return_value = None
        ctrls.next()
        core.playback.next.assert_not_called()
        core.playback.play.assert_called_with(tlid=1)

        future_tl.get.return_value = 0
        core.reset_mock()
        future_tl_track.get.return_value = None
        ctrls.next()
        core.playback.next.assert_not_called()
        core.playback.play.assert_not_called()

        future_tl.get.return_value = 0
        core.reset_mock()
        future_tl_track.get.return_value = TlTrack(1, None)
        ctrls.next()
        core.playback.next.assert_not_called()
        core.playback.play.assert_not_called()

    def test_seek_bwd(self):
        core = mock.Mock()
        future_pos = mock.Mock()
        core.playback.get_time_position.return_value = future_pos

        ctrls = PhonieboxControls(core)
        future_pos.get.return_value = 6000
        ctrls.seek_bwd()
        core.playback.seek.assert_called_with(1000)

        core.reset_mock()
        future_pos.get.return_value = 1000
        ctrls.seek_bwd()
        core.playback.seek.assert_called_with(0)

        core.reset_mock()
        future_pos.get.return_value = 10000
        ctrls.seek_bwd(seconds=3)
        core.playback.seek.assert_called_with(7000)

    def test_seek_fwd(self):
        core = mock.Mock()
        future_pos = mock.Mock()
        core.playback.get_time_position.return_value = future_pos

        ctrls = PhonieboxControls(core)
        future_pos.get.return_value = 6000
        ctrls.seek_fwd()
        core.playback.seek.assert_called_with(11000)

        core.reset_mock()
        future_pos.get.return_value = 0
        ctrls.seek_fwd()
        core.playback.seek.assert_called_with(5000)

        core.reset_mock()
        future_pos.get.return_value = 10000
        ctrls.seek_fwd(seconds=3)
        core.playback.seek.assert_called_with(13000)

    def test_volume_up(self):
        core = mock.Mock()
        future_vol = mock.Mock()
        core.mixer.get_volume.return_value = future_vol

        ctrls = PhonieboxControls(core)
        future_vol.get.return_value = None
        ctrls.volume_up()
        core.mixer.set_volume.asert_called_with(55)

        core.reset_mock()
        future_vol.get.return_value = 80
        ctrls.volume_up()
        core.mixer.set_volume.assert_called_with(85)

        core.reset_mock()
        future_vol.get.return_value = 80
        ctrls.volume_up(vol_step=3)
        core.mixer.set_volume.assert_called_with(83)

        core.reset_mock()
        future_vol.get.return_value = 100
        ctrls.volume_up()
        core.mixer.set_volume.assert_called_with(100)

    def test_volume_down(self):
        core = mock.Mock()
        future_vol = mock.Mock()
        core.mixer.get_volume.return_value = future_vol

        ctrls = PhonieboxControls(core)
        future_vol.get.return_value = None
        ctrls.volume_down()
        core.mixer.set_volume.asert_called_with(45)

        core.reset_mock()
        future_vol.get.return_value = 80
        ctrls.volume_down()
        core.mixer.set_volume.assert_called_with(75)

        core.reset_mock()
        future_vol.get.return_value = 80
        ctrls.volume_down(vol_step=1)
        core.mixer.set_volume.assert_called_with(79)

        core.reset_mock()
        future_vol.get.return_value = 0
        ctrls.volume_down()
        core.mixer.set_volume.assert_called_with(0)

    def test_mute_unmute(self):
        core = mock.Mock()
        future_muted = mock.Mock()
        core.mixer.get_mute.return_value = future_muted

        ctrls = PhonieboxControls(core)
        future_muted.get.return_value = None
        ctrls.mute_unmute()
        core.mixer.set_mute.assert_called_with(False)

        core.reset_mock()
        future_muted.get.return_value = False
        ctrls.mute_unmute()
        core.mixer.set_mute.assert_called_with(True)

        core.reset_mock()
        future_muted.get.return_value = True
        ctrls.mute_unmute()
        core.mixer.set_mute.assert_called_with(False)

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
