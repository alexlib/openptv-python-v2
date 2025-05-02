# cython: language_level=3
# distutils: language = c

import numpy as np
cimport numpy as np
np.import_array()

from libc.stdlib cimport malloc, free

# Import the C declarations
from openptv.binding.vec_utils cimport vec3d, vec_cmp, vec_copy

cpdef int py_vec_cmp(double[:] vec1, double[:] vec2):
    """
    Compare two 3D vectors for equality.
    
    Parameters
    ----------
    vec1 : array_like
        First 3D vector
    vec2 : array_like
        Second 3D vector
        
    Returns
    -------
    int
        1 if vectors are equal, 0 otherwise
    """
    cdef vec3d c_vec1
    cdef vec3d c_vec2
    
    # Copy data to C arrays
    for i in range(3):
        c_vec1[i] = vec1[i]
        c_vec2[i] = vec2[i]
    
    return vec_cmp(c_vec1, c_vec2)

cpdef double[:] py_vec_copy(double[:] src):
    """
    Copy a 3D vector.
    
    Parameters
    ----------
    src : array_like
        Source 3D vector
        
    Returns
    -------
    ndarray
        Copy of the input vector
    """
    cdef vec3d c_src
    cdef vec3d c_dest
    
    # Copy data to C array
    for i in range(3):
        c_src[i] = src[i]
    
    # Call C function
    vec_copy(c_dest, c_src)
    
    # Create numpy array from C array
    result = np.zeros(3, dtype=np.float64)
    for i in range(3):
        result[i] = c_dest[i]
    
    return result