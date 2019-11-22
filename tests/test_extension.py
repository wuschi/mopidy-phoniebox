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

from mopidy_phoniebox_idletimer import Extension
from mopidy_phoniebox_idletimer import frontend as frontend_lib


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()
        config = ext.get_default_config()

        self.assertIn('[phoniebox-idletimer]', config)
        self.assertIn('enabled = true', config)
        self.assertIn('idle_time_before_shutdown = 0', config)

    def test_get_config_schema(self):
        ext = Extension()
        schema = ext.get_config_schema()

        self.assertIn('enabled', schema)
        self.assertIn('idle_time_before_shutdown', schema)

    def test_setup(self):
        registry = mock.Mock()

        ext = Extension()
        ext.setup(registry)

        registry.add.assert_called_once_with(
                'frontend',
                frontend_lib.PhonieboxIdleTimerFrontend)
