#!/usr/bin/env python
import sys
import traceback
import os

try:
    print("Current working directory:", os.getcwd())
    
    # Check if the files exist
    control_file = "testing_fodder/control_parameters/control.par"
    ori_file = "testing_fodder/calibration/cam1.tif.ori"
    add_file = "testing_fodder/calibration/cam2.tif.addpar"
    
    print(f"Control file exists: {os.path.exists(control_file)}")
    print(f"Ori file exists: {os.path.exists(ori_file)}")
    print(f"Add file exists: {os.path.exists(add_file)}")
    
    # Try to read the files
    with open(control_file, 'rb') as f:
        control_content = f.read()
        print(f"Control file size: {len(control_content)} bytes")
    
    with open(ori_file, 'rb') as f:
        ori_content = f.read()
        print(f"Ori file size: {len(ori_content)} bytes")
    
    with open(add_file, 'rb') as f:
        add_content = f.read()
        print(f"Add file size: {len(add_content)} bytes")
    
    print("All files read successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
