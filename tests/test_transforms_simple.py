#!/usr/bin/env python
import sys
import traceback
import numpy as np

try:
    from openptv.coptv.parameters import ControlParams
    from openptv.coptv.transforms import convert_arr_metric_to_pixel
    
    print("Imports successful")
    
    # Create a control params object
    cpar = ControlParams(1)
    cpar.set_image_size((1280, 1000))
    cpar.set_pixel_size((0.1, 0.1))
    print("ControlParams created and configured successfully")
    
    # Create a test array
    metric_pos = np.array([
        [1., 1.],
        [-10., 15.],
        [20., -30.]
    ])
    print("Test array created successfully")
    
    # Try to convert
    pixel_pos = convert_arr_metric_to_pixel(metric_pos, cpar)
    print("Conversion successful")
    print("Result:", pixel_pos)
    
    print("All tests passed!")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
    sys.exit(1)
