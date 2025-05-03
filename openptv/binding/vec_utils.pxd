# cython: language_level=3
# distutils: language = c

# Cython definitions for vec_utils.h

cdef extern from "../liboptv/include/vec_utils.h":
    ctypedef double vec3d[3]
    void vec_copy(vec3d dest, vec3d src)
    int vec_cmp(vec3d vec1, vec3d vec2)
