"""
Script to check what attributes are available in the Calibration class.
"""

import os
import sys
import importlib

def main():
    """Main function."""
    print("Checking Calibration class...")
    
    # Import the modules
    try:
        from openptv.pyoptv.calibration import Calibration as CalibrationPython
        cal_python = CalibrationPython()
        print("\nPure Python Calibration class:")
        for name in dir(cal_python):
            if not name.startswith('__'):
                print(f"  {name}")
    except ImportError as e:
        print(f"Failed to import pure Python Calibration class: {e}")
    
    try:
        from openptv.binding.calibration import Calibration as CalibrationCython
        cal_cython = CalibrationCython()
        print("\nCython Calibration class:")
        for name in dir(cal_cython):
            if not name.startswith('__'):
                print(f"  {name}")
    except ImportError as e:
        print(f"Failed to import Cython Calibration class: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
