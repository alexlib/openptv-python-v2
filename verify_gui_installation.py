"""
Script to verify that OpenPTV with GUI support is installed correctly.
"""

import os
import sys

def main():
    """Main function."""
    print(f"Python executable: {sys.executable}")
    
    # Check if we're in a conda environment
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_prefix:
        print(f"Conda environment: {os.path.basename(conda_prefix)}")
    else:
        print("Not in a conda environment")
    
    # Try to import OpenPTV
    try:
        import openptv
        print(f"OpenPTV version: {openptv.__version__}")
        print("OpenPTV imported successfully!")
        
        # Check if GUI components are available
        try:
            from openptv.gui import pyptv_gui
            print("GUI components imported successfully!")
        except ImportError as e:
            print(f"Failed to import GUI components: {e}")
        
        # Check if the binding directory exists
        binding_dir = os.path.join(os.path.dirname(openptv.__file__), 'binding')
        if os.path.exists(binding_dir):
            print(f"Binding directory exists: {binding_dir}")
            
            # List the files in the binding directory
            print("Files in binding directory:")
            for file in os.listdir(binding_dir):
                if file.endswith('.pyd'):
                    print(f"  {file}")
        else:
            print("Binding directory does not exist!")
        
        return 0
    except ImportError as e:
        print(f"Failed to import OpenPTV: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
