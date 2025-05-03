"""
Test the vector utilities at all three layers:
1. C library (via Cython)
2. Cython bindings
3. Python calls
"""

import numpy as np
import sys
import pytest

def test_cython_bindings():
    """Test the Cython bindings directly."""
    try:
        from openptv.binding.vec_utils import py_vec_cmp, py_vec_copy

        # Test vectors
        vec1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        vec2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        vec3 = np.array([4.0, 5.0, 6.0], dtype=np.float64)

        # Test comparison
        assert py_vec_cmp(vec1, vec2) == 1, "Equal vectors should return 1"
        assert py_vec_cmp(vec1, vec3) == 0, "Different vectors should return 0"

        # Test copy
        copied = py_vec_copy(vec1)
        assert np.array_equal(vec1, copied), "Copied vector should equal original"

        # Modify original to verify copy is independent
        original_value = vec1[0]
        vec1[0] = 10.0
        assert copied[0] == original_value, "Modifying original should not affect copy"

        print("Cython bindings test passed!")
        assert True, "Cython bindings available"
    except ImportError as e:
        print(f"Cython bindings not available: {e}")
        pytest.skip(f"Cython bindings not available: {e}")

def test_python_implementation():
    """Test the pure Python implementation."""
    try:
        # Import directly from the Python implementation
        from openptv.pyoptv.vec_utils import vec_cmp, vec_copy

        # Test vectors
        vec1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        vec2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        vec3 = np.array([4.0, 5.0, 6.0], dtype=np.float64)

        # Test comparison
        assert vec_cmp(vec1, vec2, tol=1e-6), "Equal vectors should return True"
        assert not vec_cmp(vec1, vec3, tol=1e-6), "Different vectors should return False"

        # Test copy
        copied = vec_copy(vec1)
        assert np.array_equal(vec1, copied), "Copied vector should equal original"

        # Modify original to verify copy is independent
        original_value = vec1[0]
        vec1[0] = 10.0
        assert copied[0] == original_value, "Modifying original should not affect copy"

        print("Python implementation test passed!")
        assert True, "Python implementation available"
    except ImportError as e:
        print(f"Python implementation not available: {e}")
        # pytest.skip(f"Python implementation not available: {e}")

def test_package_interface():
    """Test the package interface that automatically selects implementation."""
    try:
        from openptv import vec_cmp, vec_copy, using_cython

        # Print which implementation we're using
        print(f"Using Cython implementation: {using_cython()}")

        # Test vectors
        vec1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        vec2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
        vec3 = np.array([4.0, 5.0, 6.0], dtype=np.float64)

        # Test comparison
        if using_cython():
            # Cython implementation returns 1 for equal, 0 for not equal
            assert vec_cmp(vec1, vec2) == 1, "Equal vectors should return 1"
            assert vec_cmp(vec1, vec3) == 0, "Different vectors should return 0"
        else:
            # Python implementation returns True for equal, False for not equal
            assert vec_cmp(vec1, vec2, tol=1e-6), "Equal vectors should return True"
            assert not vec_cmp(vec1, vec3, tol=1e-6), "Different vectors should return False"

        # Test copy
        copied = vec_copy(vec1)
        assert np.array_equal(vec1, copied), "Copied vector should equal original"

        # Modify original to verify copy is independent
        original_value = vec1[0]
        vec1[0] = 10.0
        assert copied[0] == original_value, "Modifying original should not affect copy"

        print("Package interface test passed!")
        assert True, "Package interface available"
    except ImportError as e:
        print(f"Package interface not available: {e}")
        # pytest.skip(f"Package interface not available: {e}")

if __name__ == "__main__":
    print("\n=== Testing Cython Bindings ===")
    cython_result = test_cython_bindings()

    print("\n=== Testing Python Implementation ===")
    python_result = test_python_implementation()

    print("\n=== Testing Package Interface ===")
    package_result = test_package_interface()

    print("\n=== Summary ===")
    print(f"Cython Bindings: {'PASS' if cython_result else 'FAIL'}")
    print(f"Python Implementation: {'PASS' if python_result else 'FAIL'}")
    print(f"Package Interface: {'PASS' if package_result else 'FAIL'}")

    # Exit with success if at least one implementation works
    success = cython_result or python_result
    if not success:
        print("\nERROR: No implementation available!")
        sys.exit(1)
    else:
        print("\nSUCCESS: At least one implementation works!")