"""
Test script to verify both Cython and Python implementations.
"""

import numpy as np
import os
import shutil
import subprocess
import pytest

def run_implementation_test(implementation_name):
    """Run tests on the current implementation."""
    from openptv import using_cython, track_particles, find_correspondences

    # Create test data
    np.random.seed(42)  # For reproducibility
    particles = np.random.rand(10, 3)
    points1 = np.random.rand(5, 2)
    points2 = np.random.rand(5, 2)

    # Check which implementation we're using
    if implementation_name == "Cython":
        assert using_cython() == True, "Should be using Cython implementation"
    else:
        assert using_cython() == False, "Should be using Python implementation"

    # Print which implementation we're using (for information)
    print(f"Using Cython implementation: {using_cython()}")

    # Test tracking function
    trajectories = track_particles(particles, max_link_distance=1.0)
    assert isinstance(trajectories, list)

    # Test correspondence function
    correspondences = find_correspondences(points1, points2)
    assert isinstance(correspondences, np.ndarray)

    return trajectories, correspondences

@pytest.fixture
def cython_extension():
    """Find the Cython extension file."""
    so_file = None
    for file in os.listdir("openptv/binding"):
        if file.endswith(".so"):
            so_file = os.path.join("openptv/binding", file)
            break

    if not so_file:
        # Try to build the extension
        subprocess.run(["python", "setup.py", "build_ext", "--inplace"])
        for file in os.listdir("openptv/binding"):
            if file.endswith(".so"):
                so_file = os.path.join("openptv/binding", file)
                break

    return so_file

def test_cython_implementation(cython_extension):
    """Test the Cython implementation."""
    if not cython_extension:
        pytest.skip("No Cython extension found")

    print("\n=== Testing with Cython implementation ===")
    cython_results = run_implementation_test("Cython")
    assert cython_results is not None

def test_python_implementation(cython_extension):
    """Test the Python implementation by temporarily moving the Cython extension."""
    if not cython_extension:
        pytest.skip("No Cython extension found")

    print("\n=== Testing with Python implementation ===")
    backup_file = cython_extension + ".bak"

    try:
        # Move the extension to force Python implementation
        shutil.move(cython_extension, backup_file)

        # Use a subprocess to run the test with Python implementation
        # This ensures a clean Python environment without cached imports
        script = """
import numpy as np
from openptv import using_cython, track_particles, find_correspondences

# Create test data
np.random.seed(42)
particles = np.random.rand(10, 3)
points1 = np.random.rand(5, 2)
points2 = np.random.rand(5, 2)

# Check which implementation we're using
assert using_cython() == False, "Should be using Python implementation"
print(f"Using Cython implementation: {using_cython()}")

# Test tracking function
trajectories = track_particles(particles, max_link_distance=1.0)
assert isinstance(trajectories, list)

# Test correspondence function
correspondences = find_correspondences(points1, points2)
assert isinstance(correspondences, np.ndarray)

print("Python implementation test passed!")
        """

        # Run the script in a separate process
        result = subprocess.run(
            ["python", "-c", script],
            capture_output=True,
            text=True
        )

        # Check if the test passed
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            pytest.fail("Python implementation test failed")

        assert "Python implementation test passed!" in result.stdout

    finally:
        # Restore the extension
        if os.path.exists(backup_file):
            shutil.move(backup_file, cython_extension)

def test_implementations_api_consistency(cython_extension):
    """Test that both implementations provide consistent APIs."""
    if not cython_extension:
        pytest.skip("No Cython extension found")

    print("\n=== Testing API consistency between implementations ===")

    # First get information about the Cython implementation
    cython_info = subprocess.run(
        ["python", "-c", """
import numpy as np
from openptv import using_cython, track_particles, find_correspondences

# Create test data
np.random.seed(42)
particles = np.random.rand(10, 3)
points1 = np.random.rand(5, 2)
points2 = np.random.rand(5, 2)

# Check which implementation we're using
assert using_cython() == True, "Should be using Cython implementation"
print(f"Using Cython implementation: {using_cython()}")

# Test tracking function
trajectories = track_particles(particles, max_link_distance=1.0)
print(f"Trajectories type: {type(trajectories).__name__}")

# Test correspondence function
correspondences = find_correspondences(points1, points2)
print(f"Correspondences type: {type(correspondences).__name__}")
print(f"Correspondences shape: {correspondences.shape}")
        """],
        capture_output=True,
        text=True
    )

    print("Cython implementation info:")
    print(cython_info.stdout)

    # Now test the Python implementation
    backup_file = cython_extension + ".bak"

    try:
        # Move the extension to force Python implementation
        shutil.move(cython_extension, backup_file)

        # Get information about the Python implementation
        python_info = subprocess.run(
            ["python", "-c", """
import numpy as np
from openptv import using_cython, track_particles, find_correspondences

# Create test data
np.random.seed(42)
particles = np.random.rand(10, 3)
points1 = np.random.rand(5, 2)
points2 = np.random.rand(5, 2)

# Check which implementation we're using
assert using_cython() == False, "Should be using Python implementation"
print(f"Using Cython implementation: {using_cython()}")

# Test tracking function
trajectories = track_particles(particles, max_link_distance=1.0)
print(f"Trajectories type: {type(trajectories).__name__}")

# Test correspondence function
correspondences = find_correspondences(points1, points2)
print(f"Correspondences type: {type(correspondences).__name__}")
print(f"Correspondences shape: {correspondences.shape}")
            """],
            capture_output=True,
            text=True
        )

        print("\nPython implementation info:")
        print(python_info.stdout)

        # Check if both tests passed
        if python_info.returncode != 0:
            print(f"Error in Python implementation: {python_info.stderr}")
            pytest.fail("Python implementation test failed")

        # Extract and compare type information
        cython_traj_type = None
        python_traj_type = None
        cython_corr_type = None
        python_corr_type = None

        for line in cython_info.stdout.splitlines():
            if "Trajectories type:" in line:
                cython_traj_type = line.split(":")[1].strip()
            elif "Correspondences type:" in line:
                cython_corr_type = line.split(":")[1].strip()

        for line in python_info.stdout.splitlines():
            if "Trajectories type:" in line:
                python_traj_type = line.split(":")[1].strip()
            elif "Correspondences type:" in line:
                python_corr_type = line.split(":")[1].strip()

        # Check API consistency
        assert cython_traj_type == python_traj_type, f"Trajectory types differ: {cython_traj_type} vs {python_traj_type}"
        assert cython_corr_type == python_corr_type, f"Correspondence types differ: {cython_corr_type} vs {python_corr_type}"

        print("\nAPI consistency test passed!")

    finally:
        # Restore the extension
        if os.path.exists(backup_file):
            shutil.move(backup_file, cython_extension)
