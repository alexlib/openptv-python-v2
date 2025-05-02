import numpy as np
import sys
import os

def test_vec_utils_direct():
    """Test vector utilities by importing the module directly."""
    # Import the module through the package
    from openptv.binding import vec_utils

    # Test with some vectors
    vec1 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec2 = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    vec3 = np.array([4.0, 5.0, 6.0], dtype=np.float64)

    # Test comparison
    assert vec_utils.py_vec_cmp(vec1, vec2) == 1, "Equal vectors should return 1"
    assert vec_utils.py_vec_cmp(vec1, vec3) == 0, "Different vectors should return 0"

    # Test copy
    copied = vec_utils.py_vec_copy(vec1)
    assert np.array_equal(vec1, copied), "Copied vector should equal original"

    print("All tests passed!")

if __name__ == "__main__":
    test_vec_utils_direct()