import pytest
import numpy as np
from openptv.binding.vec_utils import py_vec_cmp, py_vec_copy

def test_py_vec_cmp():
    """Test vector comparison function."""
    vec1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec3 = np.array([1.0, 2.0, 3.001], dtype=np.float64)
    
    # Identical vectors should return 1
    assert py_vec_cmp(vec1, vec2, 1e-10) == 1
    
    # Different vectors with tolerance smaller than difference should return 0
    assert py_vec_cmp(vec1, vec3, 1e-10) == 0
    
    # Different vectors with tolerance larger than difference should return 1
    assert py_vec_cmp(vec1, vec3, 0.01) == 1

def test_py_vec_copy():
    """Test vector copy function."""
    src = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    
    # Copy the vector
    dest = py_vec_copy(src)
    
    # Check that the copy is equal to the original
    assert np.array_equal(src, dest)
    
    # Modify the original and check that the copy is unchanged
    src[0] = 10.0
    assert dest[0] == 1.0

if __name__ == "__main__":
    test_py_vec_cmp()
    test_py_vec_copy()
    print("All tests passed!")
