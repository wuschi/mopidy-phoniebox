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
import subprocess

from mopidy.audio import PlaybackState


class PhonieboxControls:
    """
    Phoniebox control functions.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, core):
        self.core = core

    def shutdown(self):
        """
        Executes the phoniebox shutdown
        """
        self.logger.info("PhonieboxControls.shutdown()")
        return_code = subprocess.call(["sudo", "/sbin/poweroff"])
        if return_code > 0:
            self.logger.error("error shutting down phoniebox: %s", return_code)
        return return_code

    def play_pause(self):
        """
        Toggle play/pause.
        """
        state = self.core.playback.get_state().get()
        self.logger.info(
                "PhonieboxControls.play_pause() - state {}".format(state))
        if state == PlaybackState.PLAYING:
            self.core.playback.pause()
        elif state == PlaybackState.PAUSED:
            self.core.playback.resume()
        else:
            self.core.playback.play()

    def cd_previous(self):
        """
        Change to previous track Compact-Disc player style:
        When current song is playing for > 3 secs, change to beginning of
        current track, otherwise change to previous track.

        If no track or the first track is played, jump to the last track of
        the tracklist.
        """
        tl_len = self.core.tracklist.get_length().get()
        track = self.core.playback.get_current_tl_track().get()
        pos = self.core.playback.get_time_position().get()
        if track is None:
            tlid = 0
        else:
            tlid = track.tlid
        self.logger.info(
            ("PhonieboxControls.cd_previous() "
             + "- track {} of {}, position {}").format(tlid, tl_len, pos))
        if tl_len == 0:
            return
        if tlid == 0 or (tlid == 1 and pos < 3000):
            self.core.playback.play(tlid=tl_len)
        elif tlid > 1 and pos < 3000:
            self.core.playback.previous()
        else:
            self.core.playback.seek(0)

    def previous(self):
        """
        Change to previous track.

        If no track or the first track is played, jump to the last track of
        the tracklist.
        """
        tl_len = self.core.tracklist.get_length().get()
        track = self.core.playback.get_current_tl_track().get()
        if track is None:
            tlid = 0
        else:
            tlid = track.tlid
        self.logger.info(
            "PhonieboxControls.previous() - track {} of {}".format(
                tlid, tl_len))
        if tl_len == 0:
            return
        if tlid > 1:
            self.core.playback.previous()
        else:
            self.core.playback.play(tlid=tl_len)

    def next(self):
        """
        Change to next track.

        If no track or the last track is played, jump to the first track of
        the tracklist.
        """
        tl_len = self.core.tracklist.get_length().get()
        track = self.core.playback.get_current_tl_track().get()
        if track is None:
            tlid = 0
        else:
            tlid = track.tlid
        self.logger.info(
            "PhonieboxControls.next() - track {} of {}".format(tlid, tl_len))
        if tl_len == 0:
            return
        if tlid == 0 or tlid >= tl_len:
            self.core.playback.play(tlid=1)
        else:
            self.core.playback.next()

    def volume_up(self):
        """
        Increase the volume by 5.
        """
        volume = self.core.mixer.get_volume().get()
        self.logger.info(
            "PhonieboxControls.volume_up() - current vol {}".format(volume))
        if volume is None:
            volume = 50

        volume += 5
        volume = min(volume, 100)
        self.core.mixer.set_volume(volume)

    def volume_down(self):
        """
        Decrease the volume by 5.
        """
        volume = self.core.mixer.get_volume().get()
        self.logger.info(
            "PhonieboxControls.volume_down() - current vol {}".format(volume))
        if volume is None:
            volume = 50

        volume -= 5
        volume = max(volume, 0)
        self.core.mixer.set_volume(volume)
