"""
Tests for the calibration utilities in openptv/gui/test_calibration.py

This module tests the calibration utility functions and provides clear feedback
on test success or failure.
"""
import os
import pytest
import numpy as np
import tempfile
from pathlib import Path

# Import the functions from the original file
from tests.test_calibration import (
    read_dt_lsq,
    read_calblock,
    pair_cal_points,
    plot_cal_points,
    plot_cal_err_histogram
)

@pytest.fixture
def sample_dt_lsq_file():
    """Create a sample dt_lsq file for testing"""
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
        f.write("3\n")  # 3 particles
        f.write("1 10.0 20.0 30.0\n")
        f.write("2 40.0 50.0 60.0\n")
        f.write("3 70.0 80.0 90.0\n")

    yield Path(f.name)
    os.unlink(f.name)

@pytest.fixture
def sample_calblock_file():
    """Create a sample calblock file for testing"""
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
        f.write("1 12.0 22.0 32.0\n")
        f.write("2 42.0 52.0 62.0\n")
        f.write("3 72.0 82.0 92.0\n")

    yield Path(f.name)
    os.unlink(f.name)

def test_read_dt_lsq(sample_dt_lsq_file):
    """Test reading a dt_lsq file"""
    print("\nTesting read_dt_lsq function...")
    try:
        points = read_dt_lsq(sample_dt_lsq_file)

        # Check number of points
        if len(points) != 3:
            pytest.fail(f"Expected 3 points, but got {len(points)}")

        # Check point values
        expected_points = [
            np.array([10.0, 20.0, 30.0]),
            np.array([40.0, 50.0, 60.0]),
            np.array([70.0, 80.0, 90.0])
        ]

        for i, (actual, expected) in enumerate(zip(points, expected_points)):
            if not np.allclose(actual, expected):
                pytest.fail(f"Point {i} mismatch: expected {expected}, got {actual}")

        print("✓ read_dt_lsq test passed successfully!")
    except Exception as e:
        pytest.fail(f"read_dt_lsq test failed with error: {str(e)}")

def test_read_calblock(sample_calblock_file):
    """Test reading a calblock file"""
    print("\nTesting read_calblock function...")
    try:
        points = read_calblock(sample_calblock_file)

        # Check number of points
        if len(points) != 3:
            pytest.fail(f"Expected 3 points, but got {len(points)}")

        # Check point values
        expected_points = [
            np.array([12.0, 22.0, 32.0]),
            np.array([42.0, 52.0, 62.0]),
            np.array([72.0, 82.0, 92.0])
        ]

        for i, (actual, expected) in enumerate(zip(points, expected_points)):
            if not np.allclose(actual, expected):
                pytest.fail(f"Point {i} mismatch: expected {expected}, got {actual}")

        print("✓ read_calblock test passed successfully!")
    except Exception as e:
        pytest.fail(f"read_calblock test failed with error: {str(e)}")

def test_pair_cal_points():
    """Test pairing calibration points"""
    calblock_points = [
        np.array([10.0, 20.0, 30.0]),
        np.array([40.0, 50.0, 60.0]),
        np.array([70.0, 80.0, 90.0])
    ]

    dt_lsq_points = [
        np.array([12.0, 22.0, 32.0]),
        np.array([42.0, 52.0, 62.0]),
        np.array([72.0, 82.0, 92.0])
    ]

    # Test with large enough max_dist to include all pairs
    # The distance between corresponding points is sqrt(12) ≈ 3.464
    pairs = pair_cal_points(calblock_points, dt_lsq_points, max_dist=6.0)
    assert len(pairs) == 3

    # Test with smaller max_dist that should exclude some pairs
    pairs = pair_cal_points(calblock_points, dt_lsq_points, max_dist=2.0)
    assert len(pairs) == 0  # All distances are > 2.0

    # Test with points that are closer
    dt_lsq_points_closer = [
        np.array([10.1, 20.1, 30.1]),
        np.array([40.1, 50.1, 60.1]),
        np.array([70.1, 80.1, 90.1])
    ]

    # The distance between corresponding points is sqrt(0.03) ≈ 0.173
    pairs = pair_cal_points(calblock_points, dt_lsq_points_closer, max_dist=1.0)
    assert len(pairs) == 3

def test_plot_cal_points():
    """Test plotting calibration points"""
    # Create a simple pair list
    pairs = [
        (np.array([10.0, 20.0, 30.0]), np.array([12.0, 22.0, 32.0])),
        (np.array([40.0, 50.0, 60.0]), np.array([42.0, 52.0, 62.0]))
    ]

    # Just test that the function runs without errors
    fig, ax = plot_cal_points(pairs)
    assert fig is not None
    assert ax is not None

def test_plot_cal_err_histogram():
    """Test plotting calibration error histogram"""
    # Create a simple pair list
    pairs = [
        (np.array([10.0, 20.0, 30.0]), np.array([12.0, 22.0, 32.0])),
        (np.array([40.0, 50.0, 60.0]), np.array([42.0, 52.0, 62.0]))
    ]

    # Just test that the function runs without errors
    fig, ax = plot_cal_err_histogram(pairs)
    assert fig is not None
    assert ax is not None

if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys
    import pytest

    print("\n=== Running Calibration Utils Tests ===\n")

    # Run the tests with verbose output
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All calibration utility tests passed successfully!")
    else:
        print("\n❌ Some calibration utility tests failed. See details above.")

    sys.exit(result)
