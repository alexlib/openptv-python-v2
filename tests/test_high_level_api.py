"""
Test the high-level API of the openptv package.
"""

import pytest
import numpy as np


def test_using_cython():
    """Test that we can determine which implementation is being used."""
    from openptv import using_cython

    # Check that using_cython() returns a boolean
    assert isinstance(using_cython(), bool)

    # We expect Cython to be available since we just built it
    assert using_cython() is True, "Cython implementation should be available"


def test_track_particles():
    """Test the high-level track_particles function."""
    # Skip this test as the high-level API is not yet implemented
    pytest.skip("High-level track_particles API not yet implemented")


def test_find_correspondences():
    """Test the high-level find_correspondences function."""
    # Skip this test as the high-level API is not yet implemented
    pytest.skip("High-level find_correspondences API not yet implemented")


if __name__ == "__main__":
    # This allows running the tests directly with python
    import sys
    sys.exit(pytest.main(["-v", __file__]))