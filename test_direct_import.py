"""
Test script to directly import the compiled extensions.
"""

import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.getcwd())

try:
    # Try to import the compiled extensions directly
    import openptv.binding.calibration
    print("Successfully imported calibration module")
except ImportError as e:
    print(f"Failed to import calibration: {e}")

try:
    # Try to import the compiled extensions directly
    import openptv.binding.tracking_framebuf
    print("Successfully imported tracking_framebuf module")
except ImportError as e:
    print(f"Failed to import tracking_framebuf: {e}")

# Print the Python path
print("\nPython path:")
for path in sys.path:
    print(path)

# Print the contents of the binding directory
print("\nContents of the binding directory:")
binding_dir = os.path.join(os.getcwd(), 'openptv', 'binding')
for file in os.listdir(binding_dir):
    print(file)
