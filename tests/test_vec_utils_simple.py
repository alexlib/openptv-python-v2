import numpy as np
import pytest

def test_vec_utils():
    """Test that we can import and use vector utilities."""
    from openptv.binding.vec_utils import py_vec_cmp, py_vec_copy
    
    # Test with some vectors
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

if __name__ == "__main__":
    # This allows running the test directly with python
    pytest.main(["-v", __file__])
