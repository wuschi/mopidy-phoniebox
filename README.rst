****************************
Mopidy-Phoniebox
****************************

A phoniebox / jukebox4kids extension for mopidy.

If you have no idea what a phoniebox is, please have a look at the `project resources <#projectresources>`__.

Currently the following features are implemented:

- an idle watchdog which shuts down the machine when not playing for a defined amount of minutes
- support for playback controls via GPIO buttons

Installation
============

Install by running::

        pip install Mopidy-Phoniebox

Configuration
=============

The phoniebox mopidy extension is configured in the ``mopidy.conf`` config file.

Example Configuration
---------------------
::

        [phoniebox]
        enabled = true

        # shut down phoniebox after not playing for 10 minutes
        idle_time_before_shutdown = 10

        # configure GPIO 26 as pulled high with 50 ms debounce time
        gpio26 = pull_up,50
        
        # when GPIO 26 is pressed, trigger the play_pause function
        play_pause = gpio26,when_pressed

Configuration Options
---------------------

``enabled=[true|false]``
    ``true`` when this extension should be enabled, ``false`` otherwise.

``idle_time_before_shutdown=<int>``
    The time in minutes that mopidy needs to be paused or stopped before the phoniebox is shut down. Use value ``0`` or omit this config option to disable the idle timer. 

    The command ``sudo /sbin/poweroff`` will be executed for shutdown, so make sure that the user running mopidy has permission to execute the poweroff command with sudo permissions.

``gpio<N>=<pull_type>,<bounce_time>,<hold_time>,<hold_repeat>``
    Configures the GPIO pin number ``<N>``. Use broadcom (BCM) numbering for GPIO pins. Optional arguments can be omitted from the config value from right to left.

    ``pull_type=[pull_up|pull_down|none|none_invert]``
        **Mandatory**. Configure the GPIO pin as pulled high (``pull_up``) or low (``pull_down``) by default, or leave it floating with regular (``none``) or reversed (``none_invert``) input polarity.

    ``bounce_time=<int>|none``
        **Optional**. Configure software debounce time in milliseconds, or disable debounce compensation if ``none`` (the default).

    ``hold_time=<float>``
        **Optional**. Configure hold time in seconds (default: 1.0 seconds).

    ``hold_repeat=[true|false]``
        **Optional**. If ``true``, then the ``when_held`` function assigned to the GPIO is triggered every ``hold_time`` seconds while held. If ``false`` (the default) the ``when_held`` function will only be triggered once per hold.

``play_pause=gpio<N>,<action>``
    Configure the GPIO button function for toggling play/resume in mopidy.

    ``gpio<N>``
        **Mandatory**. The GPIO pin the button is connected to. The GPIO also has to be configured within the extension (see above).

    ``action=[when_pressed|when_held]``
        **Mandatory**. Whether to trigger the function when the button is pressed (``when_pressed``) or held (``when_held``).


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

.. _projectresources:

Project resources
=================

- `Phoniebox information <http://phoniebox.de>`__
- `jukebox4kids discussion forum <https://forum-raspberrypi.de/forum/thread/13144-projekt-jukebox4kids-jukebox-fuer-kinder/>`__
- `Source Code <https://github.com/wuschi/mopidy-phoniebox>`__
- `Issue tracker <https://github.com/wuschi/mopidy-phoniebox/issues>`__
 

Credits
=======

- Original author: `Thomas Wunschel <https://github.com/wuschi>`__
- Current maintainer: `Thomas Wunschel <https://github.com/wuschi>`__


