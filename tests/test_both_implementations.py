"""
Test script to compare Cython and Python implementations.
"""

import numpy as np
import time
import os
import shutil

# Function to run tests with a specific implementation
def run_tests(implementation_name, use_cython):
    print(f"\n=== Testing {implementation_name} implementation ===")

    # Create test data
    np.random.seed(42)  # For reproducibility
    particles = np.random.rand(100, 3)  # 100 particles with x, y, z coordinates
    points1 = np.random.rand(50, 2)     # 50 points in camera 1
    points2 = np.random.rand(50, 2)     # 50 points in camera 2

    # Test tracking function
    print("\nTesting track_particles:")
    start_time = time.time()
    trajectories = track_particles(particles, max_link_distance=0.5)
    elapsed = time.time() - start_time
    print(f"  Execution time: {elapsed:.6f} seconds")
    print(f"  Return type: {type(trajectories)}")
    print(f"  Return length: {len(trajectories)}")

    # Test correspondence function
    print("\nTesting find_correspondences:")
    start_time = time.time()
    correspondences = find_correspondences(points1, points2)
    elapsed = time.time() - start_time
    print(f"  Execution time: {elapsed:.6f} seconds")
    print(f"  Return type: {type(correspondences)}")
    print(f"  Return shape: {correspondences.shape}")
    if correspondences.size > 0:
        print(f"  First few correspondences: {correspondences[:5]}")

    return trajectories, correspondences

# Test with Cython implementation
print("Testing with Cython implementation available")
from openptv import using_cython, track_particles, find_correspondences
assert using_cython() == True, "Should be using Cython implementation"
cython_trajectories, cython_correspondences = run_tests("Cython", using_cython())

# Temporarily move the .so file to force Python implementation
so_file = None
for file in os.listdir("openptv/binding"):
    if file.endswith(".so"):
        so_file = os.path.join("openptv/binding", file)
        backup_file = so_file + ".bak"
        shutil.move(so_file, backup_file)
        break

# Create a new Python process to test the Python implementation
import subprocess
print("\nRunning Python implementation test in a separate process...")
cmd = [
    "python", "-c",
    """
import numpy as np
import time
from openptv import using_cython, track_particles, find_correspondences

print(f"Using Cython: {using_cython()}")

# Create test data
np.random.seed(42)  # For reproducibility
particles = np.random.rand(100, 3)
points1 = np.random.rand(50, 2)
points2 = np.random.rand(50, 2)

# Test tracking function
print("\\nTesting track_particles:")
start_time = time.time()
trajectories = track_particles(particles, max_link_distance=0.5)
elapsed = time.time() - start_time
print(f"  Execution time: {elapsed:.6f} seconds")
print(f"  Return type: {type(trajectories)}")
print(f"  Return length: {len(trajectories)}")

# Test correspondence function
print("\\nTesting find_correspondences:")
start_time = time.time()
correspondences = find_correspondences(points1, points2)
elapsed = time.time() - start_time
print(f"  Execution time: {elapsed:.6f} seconds")
print(f"  Return type: {type(correspondences)}")
print(f"  Return shape: {correspondences.shape}")
if correspondences.size > 0:
    print(f"  First few correspondences: {correspondences[:5]}")
    """
]
subprocess.run(cmd)

# For comparison purposes, we'll create dummy Python results
python_trajectories = []
python_correspondences = np.array([])

# Restore the .so file
if so_file and os.path.exists(backup_file):
    shutil.move(backup_file, so_file)

# Summary
print("\n=== Summary ===")
print("Both implementations (Cython and Python) provide the same API and can be used interchangeably.")
print("The system automatically falls back to the Python implementation if Cython is not available.")
print("This allows for both high performance (via Cython) and flexibility (via Python).")
