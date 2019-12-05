****************************
Mopidy-Phoniebox
****************************

A phoniebox / jukebox4kids extension for mopidy.

If you have no idea what a phoniebox is, please have a look at the `external resources <#external-resources>`__.

Currently the following features are implemented:

- an idle watchdog which shuts down the machine when not playing for a defined amount of minutes
- support for playback and volume controls via GPIO buttons

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

        # configure GPIO 13 as pulled high with 50 ms debounce time, 0.5 seconds hold time. repeat when_held every 0.5s while held
        gpio13 = pull_up,50,0.5,true
        # when GPIO 13 is held, decrease the volume by 7
        gpio13.when_held = vol_down,vol_step=7
        # when GPIO 13 is released (and was not held), decrease the volume by 10
        gpio13.when_released = vol_down,vol_step=10
        # configure GPIO 19 as pulled high with 50 ms debounce time, 0.5 seconds hold time. repeat when_held every 0.5s while held
        gpio19 = pull_up,50,0.5,true
        # when GPIO 19 is held, increase the volume by 7
        gpio19.when_held = vol_up,vol_step=7
        # when GPIO 19 is released (and was not held), increase the volume by 10
        gpio19.when_released = vol_up,vol_step=10
        # configure GPIO 20 as pulled high with 50 ms debounce time
        gpio20 = pull_up,50
        # when GPIO 20 is pressed, jump to previous track (CD-player style)
        gpio20.when_pressed = cdprev
        # configure GPIO 21 as pulled high with 50 ms debounce time
        gpio21 = pull_up,50
        # when GPIO 21 is pressed, jump to next track
        gpio21.when_pressed = next
        # configure GPIO 26 as pulled high with no debounce time, 0.5 seconds hold time and no repeat on hold
        gpio26 = pull_up,none,0.5,false
        # when GPIO 26 is pressed, trigger the play_pause function
        gpio26.when_pressed = play_pause

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

``gpio<N>.when_pressed=<function_type>[,param=value...]`` / ``gpio<N>.when_released=<function_type>[,param=value...]`` / ``gpio<N>.when_held=<function_type>[,param=value...]``
    Configure the GPIO pin number ``<N>`` function type when the button is pressed / released / held. The ``when_released`` function is only executed when there is no ``when_held`` function assigned to the same button or when the button was not held before being released.
    Some ``<function_type>`` take optional ``param=value`` pairs, separated by comma.
    Valid values for ``<function_type>`` are:

    ``shutdown``
        Shutdown the phoniebox.

    ``play_pause``
        Toggle pause / resume in mopidy.

    ``prev``
        Jump to previous track.

    ``cdprev``
        Jump to previous track in Compact Disc player style: When current track is playing for more than 3 seconds then jump to beginning of current track. Jump to previous track when current track is playing for less than 3 seconds.

    ``next``
        Jump to next track.

    ``seek_bwd``
        Seek backward. The number of seconds to seek by can be passed in the argument ``seconds`` (default is ``5``).

    ``seek_fwd``
        Seek forward. The number of seconds to seek by can be passed in the argument ``seconds`` (default is ``5``).

    ``vol_down``
        Decrease playback volume. The percentage the volume should be decreased with a single call can be passed in the argument ``vol_step`` (default is ``5``).

    ``vol_up``
        Increase playback volume. The percentage the volume should be increased with a single call can be passed in the argument ``vol_step`` (default is ``5``).

    ``mute``
        Mute/unmute playback volume.

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

- `Source Code <https://github.com/wuschi/mopidy-phoniebox>`__
- `Issue tracker <https://github.com/wuschi/mopidy-phoniebox/issues>`__
 
External resources
==================

- `Phoniebox information <http://phoniebox.de>`__
- `jukebox4kids discussion forum <https://forum-raspberrypi.de/forum/thread/13144-projekt-jukebox4kids-jukebox-fuer-kinder/>`__

Credits
=======

- Original author: `Thomas Wunschel <https://github.com/wuschi>`__
- Current maintainer: `Thomas Wunschel <https://github.com/wuschi>`__


