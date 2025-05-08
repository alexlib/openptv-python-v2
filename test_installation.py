"""
Test script to verify that the openptv-python package is installed correctly.
"""

import sys
import os
import importlib

def main():
    """Main function."""
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")

    # Try to import the package
    try:
        # First try to import the package directly
        try:
            import openptv
            print(f"OpenPTV version: {openptv.__version__}")
            print("OpenPTV imported successfully!")
        except ImportError as e:
            print(f"Failed to import openptv directly: {e}")
            print("Trying to import individual modules...")

            # Try to import individual modules
            modules_to_try = [
                'openptv.pyoptv.calibration',
                'openptv.pyoptv.constants',
                'openptv.pyoptv.correspondences',
                'openptv.pyoptv.epi',
                'openptv.pyoptv.find_candidate',
                'openptv.pyoptv.image_processing',
                'openptv.pyoptv.imgcoord',
                'openptv.pyoptv.multimed',
                'openptv.pyoptv.orientation',
                'openptv.pyoptv.parameters',
                'openptv.pyoptv.ray_tracing',
                'openptv.pyoptv.segmentation',
                'openptv.pyoptv.sortgrid',
                'openptv.pyoptv.track',
                'openptv.pyoptv.tracking',
                'openptv.pyoptv.tracking_frame_buf',
                'openptv.pyoptv.tracking_run',
                'openptv.pyoptv.trafo',
                'openptv.pyoptv.vec_utils',
                'openptv.pyoptv.version',
            ]

            for module_name in modules_to_try:
                try:
                    module = importlib.import_module(module_name)
                    print(f"Successfully imported {module_name}")
                except ImportError as e:
                    print(f"Failed to import {module_name}: {e}")

            return 1

        # Check if the binding directory exists
        binding_dir = os.path.join(os.path.dirname(openptv.__file__), 'binding')
        if os.path.exists(binding_dir):
            print(f"Binding directory exists: {binding_dir}")

            # List the files in the binding directory
            print("Files in binding directory:")
            for file in os.listdir(binding_dir):
                print(f"  {file}")
        else:
            print("Binding directory does not exist!")

        # Try to import some modules
        try:
            from openptv.pyoptv import calibration
            print("Successfully imported calibration module from pyoptv")
        except ImportError as e:
            print(f"Failed to import calibration from pyoptv: {e}")

        # Print the path to the openptv package
        print(f"OpenPTV package path: {os.path.dirname(openptv.__file__)}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
