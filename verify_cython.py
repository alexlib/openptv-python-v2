"""
Script to verify that the Cython bindings are being used.
"""

import os
import sys
import time
import numpy as np

def test_pure_python():
    """Test the pure Python implementation."""
    print("Testing pure Python implementation...")

    # Force the use of pure Python implementation
    os.environ['OPENPTV_USE_PYTHON'] = '1'

    # Import the module
    import openptv
    from openptv.pyoptv.tracking import track_particles

    # Check if Cython bindings are being used
    print(f"Using Cython bindings: {openptv._using_cython}")

    # Create a large array of random points
    num_points = 100000
    points = np.random.rand(num_points, 3)

    # Time the tracking function
    start_time = time.time()
    # Run multiple times to get a more accurate timing
    for _ in range(100):
        trajectories = track_particles(points)
    end_time = time.time()

    print(f"Pure Python tracking time: {end_time - start_time:.4f} seconds")
    print(f"Number of trajectories: {len(trajectories)}")

    return max(end_time - start_time, 0.001)  # Avoid division by zero

def test_cython():
    """Test the Cython implementation."""
    print("\nTesting Cython implementation...")

    # Force the use of Cython implementation
    os.environ.pop('OPENPTV_USE_PYTHON', None)

    # Reload the module
    import importlib
    import openptv
    importlib.reload(openptv)

    try:
        # Try to import from binding
        from openptv.binding.tracking_framebuf import track_particles
        print("Successfully imported track_particles from binding")
    except ImportError:
        # Fall back to pyoptv
        from openptv.pyoptv.tracking import track_particles
        print("Falling back to track_particles from pyoptv")

    # Check if Cython bindings are being used
    print(f"Using Cython bindings: {openptv._using_cython}")

    # Create a large array of random points
    num_points = 100000
    points = np.random.rand(num_points, 3)

    # Time the tracking function
    start_time = time.time()
    # Run multiple times to get a more accurate timing
    for _ in range(100):
        trajectories = track_particles(points)
    end_time = time.time()

    print(f"Cython tracking time: {end_time - start_time:.4f} seconds")
    print(f"Number of trajectories: {len(trajectories)}")

    return max(end_time - start_time, 0.001)  # Avoid division by zero

def main():
    """Main function."""
    # Test the pure Python implementation
    python_time = test_pure_python()

    # Test the Cython implementation
    cython_time = test_cython()

    # Compare the results
    if cython_time < python_time:
        speedup = python_time / cython_time
        print(f"\nCython implementation is {speedup:.2f}x faster than pure Python!")
    else:
        slowdown = cython_time / python_time
        print(f"\nCython implementation is {slowdown:.2f}x slower than pure Python!")

    return 0

if __name__ == "__main__":
    sys.exit(main())
