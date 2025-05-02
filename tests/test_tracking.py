"""
Tests for the tracking functionality.
"""

import numpy as np
import pytest

# Try to import from Cython bindings first, fall back to Python implementation
try:
    from openptv.binding.tracking_cy import track_particles, find_correspondences
    using_cython = True
except ImportError:
    from openptv.pyoptv.tracking import track_particles, find_correspondences
    using_cython = False

def test_track_particles():
    """Test the track_particles function."""
    # Create some test particles
    particles = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 1.0, 1.0],
        [2.0, 2.0, 2.0],
    ])
    
    # Call the function
    trajectories = track_particles(particles, max_link_distance=1.5)
    
    # Check the result
    # This is a minimal test that just ensures the function runs
    # A real test would check the correctness of the trajectories
    assert isinstance(trajectories, list)

def test_find_correspondences():
    """Test the find_correspondences function."""
    # Create some test points
    points1 = np.array([
        [0.0, 0.0],
        [1.0, 1.0],
        [2.0, 2.0],
    ])
    
    points2 = np.array([
        [0.1, 0.1],
        [1.1, 1.1],
        [2.1, 2.1],
    ])
    
    # Call the function
    if using_cython:
        correspondences = find_correspondences(points1, points2)
    else:
        correspondences = find_correspondences(points1, points2, max_distance=0.5)
    
    # Check the result
    # This is a minimal test that just ensures the function runs
    # A real test would check the correctness of the correspondences
    assert isinstance(correspondences, np.ndarray)
