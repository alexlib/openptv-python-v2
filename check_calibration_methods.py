"""
Script to check the signature of the set_pos method in the Calibration class.
"""

import os
import sys
import inspect

def main():
    """Main function."""
    print("Checking set_pos method in Calibration class...")
    
    # Import the modules
    try:
        from openptv.pyoptv.calibration import Calibration as CalibrationPython
        cal_python = CalibrationPython()
        print("\nPure Python Calibration.set_pos method:")
        print(inspect.signature(cal_python.set_pos))
        print(inspect.getdoc(cal_python.set_pos))
    except (ImportError, AttributeError) as e:
        print(f"Failed to inspect pure Python Calibration.set_pos method: {e}")
    
    try:
        from openptv.binding.calibration import Calibration as CalibrationCython
        cal_cython = CalibrationCython()
        print("\nCython Calibration.set_pos method:")
        print(inspect.signature(cal_cython.set_pos))
        print(inspect.getdoc(cal_cython.set_pos))
    except (ImportError, AttributeError) as e:
        print(f"Failed to inspect Cython Calibration.set_pos method: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
