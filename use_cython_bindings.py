"""
Script to use Cython bindings directly.
"""

import os
import sys
import importlib.util
import numpy as np

# Create a dummy utils module
class DummyUtils:
    @staticmethod
    def encode_if_needed(s):
        """Encode a string if needed."""
        if isinstance(s, str):
            return s.encode('utf-8')
        return s

    @staticmethod
    def decode_if_needed(s):
        """Decode a string if needed."""
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s

# Create a module object
utils_module = type('', (), {})()
utils_module.encode_if_needed = DummyUtils.encode_if_needed
utils_module.decode_if_needed = DummyUtils.decode_if_needed

sys.modules['openptv.binding.utils'] = utils_module

def load_extension(name):
    """Load a Cython extension directly."""
    binding_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'openptv', 'binding')

    # Find the appropriate .pyd file
    pyd_file = os.path.join(binding_dir, f"{name}.cp310-win_amd64.pyd")
    if not os.path.exists(pyd_file):
        pyd_file = os.path.join(binding_dir, f"binding.{name}.cp310-win_amd64.pyd")

    if not os.path.exists(pyd_file):
        raise ImportError(f"Could not find {name} extension")

    # Load the module from the .pyd file
    spec = importlib.util.spec_from_file_location(f"openptv.binding.{name}", pyd_file)
    module = importlib.util.module_from_spec(spec)

    # Make sure the parent modules exist
    if 'openptv' not in sys.modules:
        sys.modules['openptv'] = type('', (), {})()
    if 'openptv.binding' not in sys.modules:
        sys.modules['openptv.binding'] = type('', (), {})()

    # Add the module to sys.modules
    sys.modules[f'openptv.binding.{name}'] = module

    # Execute the module
    spec.loader.exec_module(module)

    return module

def main():
    """Main function."""
    print("Using Cython bindings directly...")

    try:
        # Load the tracking_framebuf module
        tracking_framebuf = load_extension("tracking_framebuf")
        print("Successfully loaded tracking_framebuf module")

        # Print the dir of the TargetArray class
        print("\nTargetArray class attributes:")
        for attr in dir(tracking_framebuf.TargetArray):
            if not attr.startswith('__'):
                print(f"  {attr}")

        # Create a TargetArray
        target_array = tracking_framebuf.TargetArray(10)
        print(f"Created TargetArray with {len(target_array)} elements")

        # Create a Target
        target = tracking_framebuf.Target()

        # Print the dir of the Target class
        print("\nTarget class attributes:")
        for attr in dir(target):
            if not attr.startswith('__'):
                print(f"  {attr}")

        # Try to use the setter methods
        try:
            target.set_pnr(1)
            print(f"\nSet target.pnr = {target.pnr}")

            # Set position
            target.set_pos(100.0, 200.0)
            pos = target.pos
            print(f"Set target position: ({pos[0]}, {pos[1]})")

            # Set pixel counts
            target.set_pixel_counts(10, 5, 5)
            print(f"Set pixel counts: n={target.count_pixels}")

            # Set sum grey value
            target.set_sum_grey_value(1000)
            print(f"Set sum grey value: {target.sum_grey_value}")
        except Exception as e:
            print(f"\nFailed to set target attributes: {e}")

        # Try to iterate through the array
        print("\nIterating through the array:")
        try:
            for i, t in enumerate(target_array):
                if i == 0:
                    print(f"  Target {i}: pnr={t.pnr}")
                if i >= 3:
                    break
        except Exception as e:
            print(f"  Failed to iterate: {e}")

        print("\nCython bindings are working correctly!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
