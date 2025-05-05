"""
Cython bindings for vec_utils.c
"""

cimport numpy as np
import numpy as np

from libc.stdlib cimport malloc, free

cdef extern from "vec_utils.h":
    int vec_copy(double *from_vec, double *to_vec, int dim)
    int vec_cmp(double *vec1, double *vec2, int dim)

def py_vec_copy(np.ndarray[double, ndim=1] vec):
    """
    Copy a vector.
    
    Parameters
    ----------
    vec : ndarray
        Input vector to copy.
        
    Returns
    -------
    ndarray
        A copy of the input vector.
    """
    cdef int dim = vec.shape[0]
    cdef np.ndarray[double, ndim=1] result = np.zeros(dim, dtype=np.float64)
    
    vec_copy(&vec[0], &result[0], dim)
    
    return result

def py_vec_cmp(np.ndarray[double, ndim=1] vec1, np.ndarray[double, ndim=1] vec2):
    """
    Compare two vectors for equality.
    
    Parameters
    ----------
    vec1 : ndarray
        First vector.
    vec2 : ndarray
        Second vector.
        
    Returns
    -------
    int
        1 if vectors are equal, 0 otherwise.
    """
    cdef int dim = vec1.shape[0]
    
    if vec2.shape[0] != dim:
        return 0
    
    return vec_cmp(&vec1[0], &vec2[0], dim)
