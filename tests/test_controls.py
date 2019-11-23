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

from mopidy_phoniebox.controls import PhonieboxControls


class PhonieboxControlsTest(unittest.TestCase):

    def test_init(self):
        core = mock.Mock()

        ctrls = PhonieboxControls(core)
        self.assertIs(core, ctrls.core)

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
