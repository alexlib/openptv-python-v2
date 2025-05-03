"""
Comprehensive tests for each binding module.
"""

import pytest
import numpy as np
import os


def test_vec_utils():
    """Test the vector utilities module."""
    from openptv.binding.vec_utils import py_vec_copy, py_vec_cmp

    # Create test vectors
    vec1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec3 = np.array([4.0, 5.0, 6.0], dtype=np.float64)

    # Test vector comparison
    assert py_vec_cmp(vec1, vec2) == 1, "Equal vectors should return 1"
    assert py_vec_cmp(vec1, vec3) == 0, "Different vectors should return 0"

    # Test vector copy
    copied = py_vec_copy(vec1)
    assert np.array_equal(vec1, copied), "Copied vector should equal original"

    # Modify original to verify copy is independent
    original_value = vec1[0]
    vec1[0] = 10.0
    assert copied[0] == original_value, "Modifying original should not affect copy"


def test_tracking_framebuf():
    """Test the tracking_framebuf module."""
    from openptv.binding.tracking_framebuf import Frame, TargetArray, read_targets

    # Test that we can create a TargetArray
    targets = TargetArray(5)  # Create an array with 5 targets

    # Basic validation
    assert len(targets) == 5, "TargetArray should have 5 elements"


def test_correspondences():
    """Test the correspondences module."""
    from openptv.binding.correspondences import MatchedCoords, correspondences, single_cam_correspondence

    # Just test that we can import the module and its classes
    assert MatchedCoords is not None, "MatchedCoords class should be available"
    assert correspondences is not None, "correspondences function should be available"
    assert single_cam_correspondence is not None, "single_cam_correspondence function should be available"


def test_calibration():
    """Test the calibration module."""
    try:
        from openptv.binding.calibration import Calibration

        # This is just an import test for now
        assert Calibration is not None
    except ImportError as e:
        pytest.fail(f"Failed to import calibration: {e}")


def test_parameters():
    """Test the parameters module."""
    try:
        from openptv.binding.parameters import ControlParams, VolumeParams

        # This is just an import test for now
        assert ControlParams is not None
        assert VolumeParams is not None
    except ImportError as e:
        pytest.fail(f"Failed to import parameters: {e}")


def test_transforms():
    """Test the transforms module."""
    try:
        # Check if the module can be imported
        import openptv.binding.transforms

        # This is just an import test for now
        assert openptv.binding.transforms is not None
    except ImportError as e:
        pytest.fail(f"Failed to import transforms: {e}")


def test_imgcoord():
    """Test the imgcoord module."""
    try:
        # Check if the module can be imported
        import openptv.binding.imgcoord

        # This is just an import test for now
        assert openptv.binding.imgcoord is not None
    except ImportError as e:
        pytest.fail(f"Failed to import imgcoord: {e}")


def test_orientation():
    """Test the orientation module."""
    try:
        # Check if the module can be imported
        import openptv.binding.orientation

        # This is just an import test for now
        assert openptv.binding.orientation is not None
    except ImportError as e:
        pytest.fail(f"Failed to import orientation: {e}")


def test_epipolar():
    """Test the epipolar module."""
    try:
        # Check if the module can be imported
        import openptv.binding.epipolar

        # This is just an import test for now
        assert openptv.binding.epipolar is not None
    except ImportError as e:
        pytest.fail(f"Failed to import epipolar: {e}")


def test_segmentation():
    """Test the segmentation module."""
    try:
        from openptv.binding.segmentation import target_recognition

        # This is just an import test for now
        assert target_recognition is not None
    except ImportError as e:
        pytest.fail(f"Failed to import segmentation: {e}")


def test_tracker():
    """Test the tracker module."""
    try:
        # Check if the module can be imported
        import openptv.binding.tracker

        # This is just an import test for now
        assert openptv.binding.tracker is not None
    except ImportError as e:
        pytest.fail(f"Failed to import tracker: {e}")


def test_image_processing():
    """Test the image_processing module."""
    try:
        # Check if the module can be imported
        import openptv.binding.image_processing

        # This is just an import test for now
        assert openptv.binding.image_processing is not None
    except ImportError as e:
        pytest.fail(f"Failed to import image_processing: {e}")


if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys

    print("\n=== Running Binding Modules Tests ===\n")

    # Run the tests with verbose output
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All binding modules tests passed successfully!")
    else:
        print("\n❌ Some binding modules tests failed. See details above.")

    sys.exit(result)