#!/usr/bin/env python
import sys
import traceback

try:
    from openptv.coptv.parameters import ControlParams
    from openptv.coptv.calibration import Calibration
    import numpy as np
    
    print("Imports successful")
    
    # Create a control params object
    control = ControlParams(4)
    print("ControlParams created successfully")
    
    # Create a calibration object
    calibration = Calibration()
    print("Calibration created successfully")
    
    # Set some values
    calibration.set_pos(np.array([0.0, 0.0, 40.0]))
    calibration.set_angles(np.array([0.0, 0.0, 0.0]))
    print("Calibration values set successfully")
    
    print("All tests passed!")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
