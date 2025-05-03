# cython: language_level=3
# distutils: language = c

# Cython definitions for vec_utils.h

cdef extern from "../liboptv/include/vec_utils.h":
    ctypedef double vec3d[3]
    void vec_copy(double dest[3], double src[3])
    int vec_cmp(double vec1[3], double vec2[3], double eps)

# Export these for Python use
cpdef int py_vec_cmp(double[:] vec1, double[:] vec2, double eps)
cpdef double[:] py_vec_copy(double[:] src)
