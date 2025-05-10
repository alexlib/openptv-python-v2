"""
Test that all Cython bindings can be imported correctly.
"""

import pytest
import os
import glob
import importlib


def get_binding_modules():
    """Get a list of all binding module names."""
    binding_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'openptv', 'binding')
    pyx_files = glob.glob(os.path.join(binding_dir, '*.pyx'))
    module_names = [os.path.splitext(os.path.basename(f))[0] for f in pyx_files]
    return module_names


@pytest.mark.parametrize("module_name", get_binding_modules())
def test_import_binding(module_name):
    """Test that each binding module can be imported."""
    # Skip param_bridge and tracker_bridge tests since they're not compiled yet
    # if module_name in ['param_bridge', 'tracker_bridge']:
        # pytest.skip(f"Skipping {module_name} test since it's not compiled yet")

    try:
        module = importlib.import_module(f"openptv.binding.{module_name}")
        assert module is not None, f"Failed to import {module_name}"
        print(f"Successfully imported {module_name}")

        # Get all public attributes (functions, classes, etc.)
        public_attrs = [attr for attr in dir(module) if not attr.startswith('_')]
        print(f"  Public attributes: {', '.join(public_attrs) or 'None'}")

    except ImportError as e:
        pytest.fail(f"Failed to import {module_name}: {e}")


def test_vec_utils_basic_functionality():
    """Test basic functionality of vec_utils module."""
    try:
        from openptv.binding.vec_utils import py_vec_copy, py_vec_cmp
        import numpy as np

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

        print("vec_utils basic functionality test passed")
    except ImportError as e:
        pytest.fail(f"Failed to import vec_utils: {e}")
    except Exception as e:
        pytest.fail(f"Error testing vec_utils functionality: {e}")


def test_tracking_basic_functionality():
    """Test basic functionality of tracking module."""
    try:
        from openptv.binding.tracking_framebuf import Frame, TargetArray, read_targets
        import numpy as np

        # Test that we can create a TargetArray
        targets = TargetArray(5)  # Create an array with 5 targets

        # Basic validation
        assert len(targets) == 5, "TargetArray should have 5 elements"

        print("tracking_framebuf basic functionality test passed")
    except ImportError as e:
        pytest.fail(f"Failed to import tracking_framebuf: {e}")
    except Exception as e:
        pytest.fail(f"Error testing tracking functionality: {e}")


def test_correspondences_basic_functionality():
    """Test basic functionality of correspondences module."""
    try:
        from openptv.binding.correspondences import MatchedCoords, correspondences, single_cam_correspondence
        import numpy as np

        # Just test that we can import the module and its classes
        assert MatchedCoords is not None, "MatchedCoords class should be available"
        assert correspondences is not None, "correspondences function should be available"
        assert single_cam_correspondence is not None, "single_cam_correspondence function should be available"

        print("correspondences basic functionality test passed")
    except ImportError as e:
        pytest.fail(f"Failed to import correspondences: {e}")
    except Exception as e:
        pytest.fail(f"Error testing correspondences functionality: {e}")


if __name__ == "__main__":
    # This allows running the tests directly with python
    pytest.main(["-v", __file__])
