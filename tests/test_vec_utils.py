import numpy as np
import pytest

def test_vec_utils_import():
    """Test that we can import the vector utilities from Python."""
    try:
        from openptv.binding.vec_utils import py_vec_cmp, py_vec_copy
        print("Successfully imported vector utilities")
    except ImportError as e:
        pytest.fail(f"Failed to import vector utilities: {e}")

def test_vec_cmp():
    """Test the vector comparison function."""
    from openptv.binding.vec_utils import py_vec_cmp
    
    # Create test vectors
    vec1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec3 = np.array([4.0, 5.0, 6.0], dtype=np.float64)
    
    # Test comparison
    assert py_vec_cmp(vec1, vec2) == 1, "Equal vectors should return 1"
    assert py_vec_cmp(vec1, vec3) == 0, "Different vectors should return 0"
    
    print("Vector comparison test passed")

def test_vec_copy():
    """Test the vector copy function."""
    from openptv.binding.vec_utils import py_vec_copy
    
    # Create test vector
    vec = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    
    # Copy vector
    result = py_vec_copy(vec)
    
    # Check result
    assert np.array_equal(vec, result), "Copied vector should equal original"
    
    # Modify original to verify copy is independent
    vec[0] = 10.0
    assert not np.array_equal(vec, result), "Modifying original should not affect copy"
    
    print("Vector copy test passed")

if __name__ == "__main__":
    test_vec_utils_import()
    test_vec_cmp()
    test_vec_copy()
    print("All tests passed!")