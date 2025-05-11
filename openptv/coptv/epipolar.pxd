# cython: language_level=3
# distutils: language = c

from openptv.coptv.calibration cimport calibration
from openptv.coptv.parameters cimport mm_np, volume_par
from openptv.coptv.vec_utils cimport vec3d

cdef extern from "../liboptv/include/epi.h":
    void  epi_mm_2D (double xl, double yl, calibration *cal, mm_np *mmp, 
        volume_par *vpar, vec3d out);