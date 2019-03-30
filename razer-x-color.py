#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Lorenz Leitner"
__version__ = "0.1.0"
__license__ = "MIT" # TODO: Change

import subprocess, sys
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import argparse
import json

def hex_to_decimal(hex_color):
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return r, g, b

def parse_color_argument(color):
    # Hex: Just one input argument
    rgb = color[0]
    r, g, b = hex_to_decimal(rgb)

    # RGB: Three base10 input arguments
    # TODO

    return r, g, b

def get_x_color():
    # Get current primary color used by pywal, which is color1 in Xresources
    # Colors could also be read from ~/.cache/wal/colors.json, but this way it
    # doesn't depend on pywal, in case the X colors are set from a different origin
    output = subprocess.check_output(
            "xrdb -query | grep \"*color1:\" | awk -F '#' '{print $2}'", 
            shell=True)
    rgb = output.decode()
    r, g, b = hex_to_decimal(rgb)

    return r, g, b

def set_color(color):
    """ Set the color either from the input argument or use a fallback color """

    r = 0
    g = 0
    b = 0

    if(color):
        # Set colors from input argument
        r, g, b = parse_color_argument(color)

    else:
        # Use X colors as fallback if no color argument is set
        # TODO: Maybe also add argument to pull colors from
        # ~/.cache/wal.colors.jason
        r, g, b = get_x_color()

    if args.verbose:
        print("RBG: ")
        sys.stdout.write(str(r) + " ")
        sys.stdout.write(str(g) + " ")
        sys.stdout.write(str(b) + "\n\n")

    rgb = []
    rgb.append(r)
    rgb.append(g)
    rgb.append(b)

    return rgb

def get_effects_of_device(device):
    # All relevant effects
    effects = [
        'breath_random',
        'breath_single',
        'breath_dual',
        'breath_triple',
        'pulsate',
        'reactive',
        'ripple',
        'ripple_random',
        'spectrum',
        'static',
        'startlight_single',
        'starlight_dual',
        'starlight_random',
        'wave',
    ]

    return [effect for effect in effects if device.fx.has(effect)]

def list_devices(device_manager):
    """
    List all connected Razer devices
    https://github.com/openrazer/openrazer/blob/master/examples/list_devices.py
    """

    print("Found {} Razer devices".format(len(device_manager.devices)))

    # Iterate over each device and pretty out some standard information about each
    for device in device_manager.devices:
        print("{}:".format(device.name))
        print("   type: {}".format(device.type))
        print("   serial: {}".format(device.serial))
        print("   firmware version: {}".format(device.firmware_version))
        print("   driver version: {}".format(device.driver_version))

        device_effects = get_effects_of_device(device)
        print("   effects: {}".format(device_effects))

        if (args.list_devices_long):
            print("   capabilities: {}".format(device.capabilities))
    print()

def set_effect_to_device(device_manager, device, effect, color):
    r = color[0]
    g = color[1]
    b = color[2]

    if (effect == "static"):
        # Set the effect to static, requires colors in 0-255 range
        device.fx.static(r, g, b)

    elif (effect == "breath_single"):
        # TODO: Maybe add 'breath_dual' with primary and secondary color
        device.fx.breath_single(r, g, b)

    elif (effect == "reactive"):
        times = [razer_constants.REACTIVE_500MS, razer_constants.REACTIVE_1000MS,
        razer_constants.REACTIVE_1500MS, razer_constants.REACTIVE_2000MS]
        # TODO: Add choice for time maybe
        device.fx.reactive(r, g, b, times[3])

    elif (effect == "ripple"):
        device.fx.ripple(r, g, b, razer_constants.RIPPLE_REFRESH_RATE)

    else:
        print("Effect is supported by device but not yet implemented.\n"
                "Consider opening a PR:\n"
                "https://github.com/LoLei/razer-x-color/pulls")
        return

    print("Setting device: {} to effect {}".format(device.name,
        effect))


def set_effect_to_all_devices(device_manager, input_effect, color):
    """ Set one effect to all connected devices, if they support that effect """

    # Iterate over each device and set the effect
    for device in device_manager.devices:
        if not input_effect:
            effect_to_use = "static"
        else:
            effect_to_use = input_effect

        if not device.fx.has(effect_to_use):
            effect_to_use = "static"
            if args.verbose:
                print("Device does not support chosen effect. Using static"
                        " as fallback...")

        set_effect_to_device(device_manager, device, effect_to_use, color)

def main():
    """ Main entry point of the app """

    # -------------------------------------------------------------------------
    # COLORS
    color = set_color(args.color)

    # -------------------------------------------------------------------------
    # DEVICES
    # Create a DeviceManager. This is used to get specific devices
    device_manager = DeviceManager()

    if (args.list_devices or args.list_devices_long):
        list_devices(device_manager)

    # Disable daemon effect syncing.
    # Without this, the daemon will try to set the lighting effect to every device.
    device_manager.sync_effects = False

    # Do below only if dry run is not specified
    if args.automatic or args.effect or args.color:
        set_effect_to_all_devices(device_manager, args.effect, color)

if __name__ == "__main__":
    """ This is executed when run from the command line """

    # -------------------------------------------------------------------------
    # ARGS
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--effect",
                        help="set effect",
                        action="store")

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-c","--color", nargs="+",
                        help="choose color (default: X color1), use one argument "
                             "for hex, or three for base10 rgb")

    parser.add_argument("-l", "--list_devices",
                        help="list available devices",
                        action="store_true")

    parser.add_argument("-ll", "--list_devices_long",
                        help="list available devices and all their capabilities",
                        action="store_true")

    parser.add_argument("-a", "--automatic",
                        help="try to find colors and set them to all devices "
                             "without user arguments, uses X or pywal colors",
                        action="store_true")

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        print("Starting Razer colors script...")

    main()
