# cython: language_level=3
# distutils: language = c

import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free

cdef extern from "../liboptv/include/vec_utils.h":
    void vec_copy(double dest[3], double src[3])
    int vec_cmp(double vec1[3], double vec2[3], double eps)

cpdef int py_vec_cmp(double[:] vec1, double[:] vec2, double eps=0.0001):
    """
    Compare two 3D vectors for equality within a small epsilon.
    
    Arguments:
    vec1, vec2 - the vectors to compare.
    eps - the allowed difference between vectors.
    
    Returns:
    1 if vectors are equal within epsilon, 0 otherwise.
    """
    cdef:
        double c_vec1[3]
        double c_vec2[3]
    
    # Copy from memory views to C arrays
    for i in range(3):
        c_vec1[i] = vec1[i]
        c_vec2[i] = vec2[i]
    
    return vec_cmp(c_vec1, c_vec2, eps)

cpdef double[:] py_vec_copy(double[:] src):
    """
    Copy a 3D vector.
    
    Arguments:
    src - the source vector to copy.
    
    Returns:
    A new vector with the same values.
    """
    cdef:
        double c_src[3]
        double c_dest[3]
        double[:] dest = np.zeros(3, dtype=np.float64)
    
    # Copy from memory view to C array
    for i in range(3):
        c_src[i] = src[i]
    
    # Call C function
    vec_copy(c_dest, c_src)
    
    # Copy back to memory view
    for i in range(3):
        dest[i] = c_dest[i]
    
    return dest
