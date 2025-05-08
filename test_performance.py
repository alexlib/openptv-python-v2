"""
Script to test the performance of the Cython bindings.
"""

import os
import sys
import time
import numpy as np

def test_vec_utils():
    """Test the performance of the vec_utils module."""
    print("Testing vec_utils performance...")

    # Import the modules
    from openptv.pyoptv.vec_utils import vec_copy as vec_copy_python
    from openptv.binding.vec_utils import py_vec_copy as vec_copy_cython

    # Create a large array of random vectors
    num_vectors = 1000000
    vectors = np.random.rand(num_vectors, 3)

    # Time the pure Python implementation
    start_time = time.time()
    for i in range(1000):
        copies = [vec_copy_python(v) for v in vectors[:1000]]
    end_time = time.time()
    python_time = end_time - start_time
    print(f"Pure Python time: {python_time:.4f} seconds")

    # Time the Cython implementation
    start_time = time.time()
    for i in range(1000):
        copies = [vec_copy_cython(v) for v in vectors[:1000]]
    end_time = time.time()
    cython_time = end_time - start_time
    print(f"Cython time: {cython_time:.4f} seconds")

    # Compare the results
    if cython_time < python_time:
        speedup = python_time / cython_time
        print(f"Cython implementation is {speedup:.2f}x faster than pure Python!")
    else:
        slowdown = cython_time / python_time
        print(f"Cython implementation is {slowdown:.2f}x slower than pure Python!")

    return python_time, cython_time

def test_calibration():
    """Test the performance of the calibration module."""
    print("\nTesting calibration performance...")

    # Import the modules
    from openptv.pyoptv.calibration import Calibration as CalibrationPython
    from openptv.binding.calibration import Calibration as CalibrationCython

    # Create a calibration object
    cal_python = CalibrationPython()
    cal_cython = CalibrationCython()

    # Create a large array of random points
    num_points = 10000
    points = np.random.rand(num_points, 3)

    # Time the pure Python implementation
    start_time = time.time()
    for i in range(100):
        for p in points[:100]:
            cal_python.set_pos(p)
    end_time = time.time()
    python_time = end_time - start_time
    print(f"Pure Python time: {python_time:.4f} seconds")

    # Time the Cython implementation
    start_time = time.time()
    for i in range(100):
        for p in points[:100]:
            cal_cython.set_pos(p)
    end_time = time.time()
    cython_time = end_time - start_time
    print(f"Cython time: {cython_time:.4f} seconds")

    # Compare the results
    if cython_time < python_time:
        speedup = python_time / cython_time
        print(f"Cython implementation is {speedup:.2f}x faster than pure Python!")
    else:
        slowdown = cython_time / python_time
        print(f"Cython implementation is {slowdown:.2f}x slower than pure Python!")

    return python_time, cython_time

def main():
    """Main function."""
    # Test the vec_utils module
    vec_utils_python_time, vec_utils_cython_time = test_vec_utils()

    # Test the calibration module
    calibration_python_time, calibration_cython_time = test_calibration()

    # Calculate the overall speedup
    python_time = vec_utils_python_time + calibration_python_time
    cython_time = vec_utils_cython_time + calibration_cython_time

    print("\nOverall results:")
    if cython_time < python_time:
        speedup = python_time / cython_time
        print(f"Cython implementation is {speedup:.2f}x faster than pure Python!")
    else:
        slowdown = cython_time / python_time
        print(f"Cython implementation is {slowdown:.2f}x slower than pure Python!")

    return 0

if __name__ == "__main__":
    sys.exit(main())
