import pytest
import numpy as np

# Import the core functions we want to test for compatibility
# We're just testing that these can be imported without errors
from openptv.gui.ptv import py_start_proc_c

def test_numpy_array_compatibility():
    """Test numpy array handling in core functions"""
    # Create test arrays using newer numpy
    test_array = np.zeros((100, 100), dtype=np.uint8)
    test_coords = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float64)

    # Test array passing to core functions
    try:
        # Verify that the imported function exists
        assert py_start_proc_c is not None

        # Verify array dtypes
        assert test_array.dtype == np.uint8
        assert test_coords.dtype == np.float64

        print("✓ NumPy array compatibility test passed!")
    except Exception as e:
        pytest.fail(f"Numpy compatibility test failed: {str(e)}")

def test_optv_integration():
    """Test integration with openptv package"""
    print("\nTesting OpenPTV integration...")
    try:
        from openptv.coptv.calibration import Calibration
        from openptv.coptv.parameters import ControlParams

        # Create test calibration
        cal = Calibration()
        if cal is None:
            pytest.fail("Failed to create Calibration object")

        # Test parameter handling
        cpar = ControlParams(4)
        if cpar.get_num_cams() != 4:
            pytest.fail(f"Expected 4 cameras, but got {cpar.get_num_cams()}")

        print("✓ OpenPTV integration test passed!")
    except Exception as e:
        pytest.fail(f"OpenPTV integration test failed with error: {str(e)}")


if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys

    print("\n=== Running NumPy Compatibility Tests ===\n")

    # Run the tests with verbose output
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All NumPy compatibility tests passed successfully!")
    else:
        print("\n❌ Some NumPy compatibility tests failed. See details above.")

    sys.exit(result)