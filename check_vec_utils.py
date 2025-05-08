"""
Script to check what functions are available in the vec_utils module.
"""

import os
import sys
import importlib

def main():
    """Main function."""
    print("Checking vec_utils module...")
    
    # Import the modules
    try:
        from openptv.pyoptv import vec_utils as vec_utils_python
        print("\nPure Python vec_utils module:")
        for name in dir(vec_utils_python):
            if not name.startswith('__'):
                print(f"  {name}")
    except ImportError as e:
        print(f"Failed to import pure Python vec_utils module: {e}")
    
    try:
        from openptv.binding import vec_utils as vec_utils_cython
        print("\nCython vec_utils module:")
        for name in dir(vec_utils_cython):
            if not name.startswith('__'):
                print(f"  {name}")
    except ImportError as e:
        print(f"Failed to import Cython vec_utils module: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
