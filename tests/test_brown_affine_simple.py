#!/usr/bin/env python
import sys
import traceback
import numpy as np

try:
    from openptv.binding.calibration import Calibration
    from openptv.binding.transforms import distort_arr_brown_affine, correct_arr_brown_affine
    
    print("Imports successful")
    
    # Create a calibration object
    cal = Calibration()
    cal.set_pos(np.array([0.0, 0.0, 40.0]))
    cal.set_angles(np.array([0.0, 0.0, 0.0]))
    cal.set_primary_point(np.array([0.0, 0.0, 10.0]))
    cal.set_glass_vec(np.array([0.0, 0.0, 20.0]))
    cal.set_radial_distortion(np.zeros(3))
    cal.set_decentering(np.zeros(2))
    cal.set_affine_trans(np.array([1.0, 0.0]))
    print("Calibration created and configured successfully")
    
    # Create a test array
    ref_pos = np.array([
        [0.1, 0.1],
        [1.0, -1.0],
        [-5.0, 5.0]
    ])
    print("Test array created successfully")
    
    # Try to distort
    distorted = distort_arr_brown_affine(ref_pos, cal)
    print("Distortion successful")
    print("Distorted:", distorted)
    
    # Try to correct
    corrected = correct_arr_brown_affine(distorted, cal)
    print("Correction successful")
    print("Corrected:", corrected)
    
    print("All tests passed!")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
