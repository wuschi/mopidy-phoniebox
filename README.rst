****************************
Mopidy-Phoniebox
****************************

This mopidy extension shuts down the machine when mopidy is not playing anything for the configured time in minutes.

Installation
============

Install by running::

        pip install Mopidy-Phoniebox

Configuration
=============

The idle time after which the shutdown will be executed is configured in the ``mopidy.conf`` config file::

        [phoniebox]
        enabled = true

        # idle time in minutes before shutdown is executed
        idle_time_before_shutdown = 0

Usage
=====

This extension will shutdown the machine when mopidy is not playing anything for ``idle_time_before_shutdown``
minutes.
The command ``sudo /sbin/poweroff`` will be executed for shutdown, so make sure that the user running mopidy has
permission to execute the poweroff command with sudo permissions.

License
=============
::

  Copyright 2019 Thomas Wunschel (https://github.com/wuschi)

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

Project resources
=================

- `Source Code <https://github.com/wuschi/mopidy-phoniebox>`__
- `Issue tracker <https://github.com/wuschi/mopidy-phoniebox/issues>`__
 

Credits
=======

- Original author: `Thomas Wunschel <https://github.com/wuschi>`__
- Current maintainer: `Thomas Wunschel <https://github.com/wuschi>`__
