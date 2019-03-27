# https://github.com/openrazer/openrazer/blob/feature_docs/examples/basic_effect.py

import subprocess, sys
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import argparse

# -----------------------------------------------------------------------------
# ARGS

parser = argparse.ArgumentParser()
parser.add_argument("--effect", help="set effect",
                    action="store")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()

if args.verbose:
    print("Starting Razer colors script...")

# -----------------------------------------------------------------------------
# COLORS
# Get current primary color used by pywal
output = subprocess.check_output(
        "xrdb -query | grep \"*color1:\" | awk -F '#' '{print $2}'", 
        shell=True)
rgb = output.decode()
# Colors could also be read from ~/.cache/wal/colors.json, but this way it
# doesn't depend on pywal, in case the X colors are set from a different origin

r = int(rgb[0:2], 16)
g = int(rgb[2:4], 16)
b = int(rgb[4:6], 16)

if args.verbose:
    print("Found color1 RGB: {}".format(rgb))
    print("In decimal: ")
    sys.stdout.write(str(r) + " ")
    sys.stdout.write(str(g) + " ")
    sys.stdout.write(str(b) + "\n\n")

# -----------------------------------------------------------------------------
# DEVICES
# Create a DeviceManager. This is used to get specific devices
device_manager = DeviceManager()

if args.verbose:
    print("Found {} Razer devices".format(len(device_manager.devices)))

# Disable daemon effect syncing.
# Without this, the daemon will try to set the lighting effect to every device.
device_manager.sync_effects = False

# Iterate over each device and set the wave effect
for device in device_manager.devices:

    if args.verbose:
        print("Setting {} to static".format(device.name))

    if not args.effect:
        print("No effect set, using default effect: static. Use --effect to set\
                a custom effect.")
        # Default effect is static, if no argument is specified
        # Set the effect to static, requires colors in 0-255 range
        device.fx.static(r, g, b)

    elif (args.effect == "static"):
        print("Using effect: static")
        # Set the effect to static, requires colors in 0-255 range
        device.fx.static(r, g, b)
    else:
        print("Unkown effect. Available effects: static, wave, TODO")


