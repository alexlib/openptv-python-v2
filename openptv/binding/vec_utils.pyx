# cython: language_level=3
# distutils: language = c

import numpy as np
cimport numpy as np

# Import C functions from vec_utils.h
cdef extern from "../liboptv/include/vec_utils.h":
    void vec_copy(double dest[3], double src[3])
    int vec_cmp(double vec1[3], double vec2[3], double eps)

# Python-accessible wrappers
cpdef double[:] py_vec_copy(double[:] src):
    """
    Copy a vector.
    
    Arguments:
    src - the source vector to copy.
    
    Returns:
    A new vector with the same values.
    """
    cdef double[:] dest = np.empty(3, dtype=np.float64)
    # Call the C function
    vec_copy(&dest[0], &src[0])
    return dest

cpdef int py_vec_cmp(double[:] vec1, double[:] vec2, double eps):
    """
    Compare two vectors for equality within a small epsilon.
    
    Arguments:
    vec1, vec2 - the vectors to compare.
    eps - the allowed difference between vectors.
    
    Returns:
    1 if vectors are equal within epsilon, 0 otherwise.
    """
    return vec_cmp(&vec1[0], &vec2[0], eps)
