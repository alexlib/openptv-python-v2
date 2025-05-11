# cython: language_level=3
# distutils: language = c

from openptv.coptv.calibration cimport calibration
from openptv.coptv.parameters cimport mm_np
from openptv.coptv.vec_utils cimport vec3d

cdef extern from "../liboptv/include/imgcoord.h":
    void img_coord(vec3d pos,
                     calibration * cal,
                     mm_np * mm,
                     double * x,
                     double * y)
    
    void flat_image_coord(vec3d pos,
                           calibration * cal,
                           mm_np * mm,
                           double * x,
                           double * y)