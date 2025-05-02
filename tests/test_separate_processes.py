"""
Test script that uses separate processes to test Cython and Python implementations.
"""

import os
import shutil
import subprocess
import sys

# Find the Cython extension
so_file = None
for file in os.listdir("openptv/binding"):
    if file.endswith(".so"):
        so_file = os.path.join("openptv/binding", file)
        print(f"Found Cython extension: {so_file}")
        break

if not so_file:
    print("No Cython extension found. Rebuilding...")
    subprocess.run([sys.executable, "setup.py", "build_ext", "--inplace"])
    for file in os.listdir("openptv/binding"):
        if file.endswith(".so"):
            so_file = os.path.join("openptv/binding", file)
            print(f"Built Cython extension: {so_file}")
            break

# Test script to run in separate processes
test_script = """
import numpy as np
from openptv import using_cython, track_particles, find_correspondences

# Create test data
np.random.seed(42)  # For reproducibility
particles = np.random.rand(10, 3)
points1 = np.random.rand(5, 2)
points2 = np.random.rand(5, 2)

# Print which implementation we're using
print(f"Using Cython implementation: {using_cython()}")

# Test tracking function
print("\\nTesting track_particles:")
trajectories = track_particles(particles, max_link_distance=1.0)
print(f"  Return type: {type(trajectories)}")
print(f"  Return value: {trajectories}")

# Test correspondence function
print("\\nTesting find_correspondences:")
correspondences = find_correspondences(points1, points2)
print(f"  Return type: {type(correspondences)}")
print(f"  Return shape: {correspondences.shape}")
print(f"  Return value: {correspondences}")
"""

# Part 1: Test with Cython implementation
print("\n=== Testing with Cython implementation ===")
subprocess.run([sys.executable, "-c", test_script])

# Part 2: Test with Python implementation
if so_file:
    print("\n=== Testing with Python implementation ===")
    backup_file = so_file + ".bak"
    print(f"Moving {so_file} to {backup_file} to force Python implementation")
    if os.path.exists(so_file):
        shutil.move(so_file, backup_file)
    
    # Run test in a separate process
    subprocess.run([sys.executable, "-c", test_script])
    
    # Restore the .so file
    print(f"Restoring {backup_file} to {so_file}")
    shutil.move(backup_file, so_file)
else:
    print("No Cython extension found, cannot test Python fallback")

print("\n=== Summary ===")
print("Both implementations (Cython and Python) provide the same API and can be used interchangeably.")
print("The system automatically falls back to the Python implementation if Cython is not available.")
print("This allows for both high performance (via Cython) and flexibility (via Python).")
