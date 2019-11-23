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

from mopidy_phoniebox.frontend import PhonieboxFrontend


class PhonieboxControlsTest(unittest.TestCase):

    def test_init(self):
        core = mock.Mock()
        config = {'phoniebox': {'idle_time_before_shutdown': 0}}

        f = PhonieboxFrontend(config, core)
        self.assertIs(core, f.core)
        self.assertIs(config['phoniebox'], f.config)
        self.assertIsNotNone(f.controls)
        self.assertIsNone(f.idle_watchdog)

    def test_on_start(self):
        core = mock.Mock()
        config = {'phoniebox': {'idle_time_before_shutdown': 0}}

        f = PhonieboxFrontend(config, core)
        f.on_start()
        self.assertIsNone(f.idle_watchdog)

        config = {'phoniebox': {'idle_time_before_shutdown': 100}}
        f = PhonieboxFrontend(config, core)
        f.on_start()
        self.assertIsNotNone(f.idle_watchdog)
        f.idle_watchdog.stop()

    def test_on_stop(self):
        core = mock.Mock()
        config = {'phoniebox': {'idle_time_before_shutdown': 100}}
        iw = mock.Mock()

        f = PhonieboxFrontend(config, core)
        f.idle_watchdog = iw
        f.on_stop()
        iw.stop.assert_called_once()
