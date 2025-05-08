"""
Script to verify that the openptv-python package is installed correctly.
"""

import os
import sys

def main():
    """Main function."""
    print("Verifying openptv-python installation...")
    
    try:
        import openptv
        print(f"OpenPTV version: {openptv.__version__}")
        print("OpenPTV imported successfully!")
        
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
        
        print("\nInstallation verification successful!")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
