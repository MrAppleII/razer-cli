# razer-cli
Command line interface for controlling Razer devices on Linux

## About
With this command line interface you can configure your Razer peripherals, such
as keyboard and mouse, set their colors and effects, etc.

The most simple use case (for which this tool was originally developed) is to
use it in symbiosis with [`pywal`](https://github.com/dylanaraps/pywal). Then
this tool will set your Razer colors to Pywal's colors. See below for more
information.

## Installation
```bash
pip install razer-cli
```

## Usage
```bash
$ razer-cli -h
usage: razer-cli [-h] [-e EFFECT] [-v] [-c COLOR [COLOR ...]] [-l] [-ll] [-a]
                 [-d DEVICE [DEVICE ...]] [--dpi DPI]

optional arguments:
  -h, --help            show this help message and exit
  -e EFFECT, --effect EFFECT
                        set effect
  -v, --verbose         increase output verbosity
  -c COLOR [COLOR ...], --color COLOR [COLOR ...]
                        choose color (default: X color1), use one argument for
                        hex, or three for base10 rgb
  -l, --list_devices    list available devices and their supported effects
  -ll, --list_devices_long
                        list available devices and all their capabilities
  -a, --automatic       try to find colors and set them to all devices without
                        user arguments, uses X or pywal colors
  -d DEVICE [DEVICE ...], --device DEVICE [DEVICE ...]
                        only affect these devices, same name as output of -l
  --dpi DPI             set DPI of device
```
<sup>This might be out of date, just run it with `-h` yourself to see the newest
options.</sup>  

### Example usage with Pywal
To get your mouse and keyboard to use Pywal's colors, simply start `razer-cli`
with the `-a` flag, after having executed `wal`: `razer-cli -a`  
Example in action 
[here](https://github.com/LoLei/dotfiles/blob/master/exec-wal.sh).

#### Other examples
`$ razer-cli -e ripple -c ff0000`  
`$ razer-cli -e static -c ffffff`  

You can also leave out the color or the effect:  
`$ razer-cli -e breath_single`  
`$ razer-cli -c 55ff99`

Currently this will imply the `-a` flag being used for the missing setting. I
plan on also having the option to reuse the current color/effect, if the
argument is missing, in the future.

#### Other symbiosis tools
* [`wpgtk`](https://github.com/deviantfero/wpgtk)
* [`Chameleon`](https://github.com/GideonWolfe/Chameleon)

## Dependencies
* [`openrazer`](https://github.com/openrazer/openrazer)
  * :warning: Do not install `openrazer` from [pip](https://pypi.org/project/openrazer/), which is something else.
  * Instead install it from one of the various package managers of your distribution.
* [`xrdb`](https://www.archlinux.org/packages/extra/x86_64/xorg-xrdb/)
  * Also available on most distros.

## Disclaimer
Not all devices have been tested, but basic effects should work everywhere. Some guesswork is being done as to what capabilities are supported on specific devices. If you need more advanced configuration, consider using the GUIs [Polychromatic](https://github.com/polychromatic/polychromatic/), [RazerGenie](https://github.com/z3ntu/RazerGenie) or [RazerCommander](https://gitlab.com/gabmus/razerCommander) which have specific implementations for most devices.
  
Feel free to open feature request issues or PRs.
