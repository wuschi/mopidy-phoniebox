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
from __future__ import absolute_import, unicode_literals

import logging
import os

from mopidy import config, ext

from .gpioconfig import GpioConfig


__version__ = '0.1.0-dev'


class Extension(ext.Extension):
    """
    The phoniebox extension for mopidy.
    """

    dist_name = 'Mopidy-Phoniebox'
    ext_name = 'phoniebox'
    version = __version__
    logger = logging.getLogger(__name__)

    def get_default_config(self):
        """
        Loads the default configuration.
        """
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        """
        Returns the configuration schema of this extension.
        """
        schema = super(Extension, self).get_config_schema()
        schema['idle_time_before_shutdown'] = config.Integer()
        for gpio in range(28):
            schema['gpio{:d}'.format(gpio)] = GpioConfig()
        return schema

    def setup(self, registry):
        """
        Registers this extension in mopidy.
        """
        from .frontend import PhonieboxFrontend
        registry.add('frontend', PhonieboxFrontend)

        # Or nothing to register e.g. command extension
        self.logger.info("Initialized %s version %s",
                         self.dist_name, self.version)
