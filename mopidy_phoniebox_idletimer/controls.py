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


class PhonieboxControls:
    """
    Phoniebox control functions.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, core):
        self.core = core

    def save_playback_state(self):
        """
        Saves the current playback state. Not implemented yet.
        """
        pass

    def shutdown(self):
        """
        Executes the phoniebox shutdown
        """
        self.logger.info("executing phoniebox shutdown")
        self.save_playback_state()
        return_code = subprocess.call(["sudo", "/sbin/poweroff"])
        if return_code > 0:
            self.logger.error("error shutting down phoniebox: %s", return_code)
