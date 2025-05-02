# Vector utilities definitions for import in to other Cython files.

cdef extern from "../liboptv/include/vec_utils.h":
    ctypedef double vec3d[3]
    
    int vec_cmp(vec3d vec1, vec3d vec2)
    void vec_copy(vec3d dest, vec3d src)

# Export these for Python use
cpdef int py_vec_cmp(double[:] vec1, double[:] vec2)
cpdef double[:] py_vec_copy(double[:] src)

