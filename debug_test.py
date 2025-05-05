#!/usr/bin/env python
import sys
import traceback

try:
    from openptv.binding.parameters import ControlParams
    from openptv.binding.calibration import Calibration
    
    print("Imports successful")
    
    # Try to read the control parameters
    control = ControlParams(4)
    control_file = "testing_fodder/control_parameters/control.par"
    print(f"Reading control file: {control_file}")
    control.read_control_par(control_file)
    print("Control parameters read successfully")
    
    # Try to read the calibration files
    ori_file = "testing_fodder/calibration/cam1.tif.ori"
    add_file = "testing_fodder/calibration/cam2.tif.addpar"
    print(f"Reading calibration files: {ori_file}, {add_file}")
    
    calibration = Calibration()
    calibration.from_file(ori_file, add_file)
    print("Calibration read successfully")
    
    print("All tests passed!")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
