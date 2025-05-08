"""
Script to verify that the Cython bindings are installed correctly.
"""

import os
import sys
import importlib.util

def check_module(module_name):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def main():
    """Main function."""
    print("Verifying Cython bindings installation...")
    
    # Check if the binding directory exists
    import openptv
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
        return 1
    
    # Check if the utils module exists
    if check_module('openptv.binding.utils'):
        print("utils module exists")
    else:
        print("utils module does not exist!")
    
    # Check if the Cython modules can be imported
    modules_to_check = [
        'openptv.binding.calibration',
        'openptv.binding.correspondences',
        'openptv.binding.epipolar',
        'openptv.binding.image_processing',
        'openptv.binding.imgcoord',
        'openptv.binding.orientation',
        'openptv.binding.parameters',
        'openptv.binding.segmentation',
        'openptv.binding.tracker',
        'openptv.binding.tracking_framebuf',
        'openptv.binding.transforms',
        'openptv.binding.vec_utils',
    ]
    
    print("\nChecking if Cython modules can be imported:")
    for module_name in modules_to_check:
        if check_module(module_name):
            print(f"  {module_name}: OK")
        else:
            print(f"  {module_name}: FAILED")
    
    # Check if the Cython bindings are being used
    print(f"\nUsing Cython bindings: {openptv._using_cython}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
