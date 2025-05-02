"""
Test script to verify the implementation (Cython or Python).
"""

import numpy as np
import pytest
from openptv import using_cython, track_particles, find_correspondences

def test_implementation_info():
    """Test that we can determine which implementation is being used."""
    # Check that using_cython() returns a boolean
    assert isinstance(using_cython(), bool)

    # Print which implementation we're using (for information)
    print(f"Using Cython implementation: {using_cython()}")

def test_track_particles_basic():
    """Test basic functionality of track_particles."""
    # Create test data
    np.random.seed(42)  # For reproducibility
    particles = np.random.rand(10, 3)  # 10 particles with x, y, z coordinates

    # Call the function
    trajectories = track_particles(particles, max_link_distance=1.0)

    # Check the result
    assert isinstance(trajectories, list)

    # Print information (for debugging)
    print(f"  Return type: {type(trajectories)}")
    print(f"  Return value: {trajectories}")

def test_find_correspondences_basic():
    """Test basic functionality of find_correspondences."""
    # Create test data
    np.random.seed(42)  # For reproducibility
    points1 = np.random.rand(5, 2)     # 5 points in camera 1
    points2 = np.random.rand(5, 2)     # 5 points in camera 2

    # Call the function
    correspondences = find_correspondences(points1, points2)

    # Check the result
    assert isinstance(correspondences, np.ndarray)

    # Print information (for debugging)
    print(f"  Return type: {type(correspondences)}")
    print(f"  Return shape: {correspondences.shape}")
    print(f"  Return value: {correspondences}")
