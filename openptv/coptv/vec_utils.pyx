# cython: language_level=3
# distutils: language = c

"""
Cython binding for vector utilities in liboptv.

This module provides Python bindings for the vector utilities in liboptv,
which are used for handling 3D vectors.
"""

import numpy as np
cimport numpy as np

# Import the declarations from the .pxd file
from openptv.coptv.vec_utils cimport vec3d, vec_copy, vec_cmp

# Make sure NumPy is initialized
np.import_array()

def py_vec_copy(np.ndarray[double, ndim=1] src not None):
    """
    Copy a 3D vector.
    
    Args:
        src: Source vector (numpy array of shape (3,))
        
    Returns:
        numpy.ndarray: Copy of the source vector
    """
    if src.shape[0] != 3:
        raise ValueError("Vector must have exactly 3 elements")
    
    # Create output array
    cdef np.ndarray[double, ndim=1] dest = np.zeros(3, dtype=np.float64)
    
    # Create C-compatible arrays
    cdef vec3d c_src
    cdef vec3d c_dest
    
    # Copy data from NumPy arrays to C arrays
    for i in range(3):
        c_src[i] = src[i]
    
    # Call the C function
    vec_copy(c_dest, c_src)
    
    # Copy data from C array to NumPy array
    for i in range(3):
        dest[i] = c_dest[i]
    
    return dest

def py_vec_cmp(np.ndarray[double, ndim=1] vec1 not None, 
               np.ndarray[double, ndim=1] vec2 not None):
    """
    Compare two 3D vectors for equality.
    
    Args:
        vec1: First vector (numpy array of shape (3,))
        vec2: Second vector (numpy array of shape (3,))
        
    Returns:
        int: 1 if vectors are equal, 0 otherwise
    """
    if vec1.shape[0] != 3 or vec2.shape[0] != 3:
        raise ValueError("Vectors must have exactly 3 elements")
    
    # Create C-compatible arrays
    cdef vec3d c_vec1
    cdef vec3d c_vec2
    
    # Copy data from NumPy arrays to C arrays
    for i in range(3):
        c_vec1[i] = vec1[i]
        c_vec2[i] = vec2[i]
    
    # Call the C function
    return vec_cmp(c_vec1, c_vec2)
