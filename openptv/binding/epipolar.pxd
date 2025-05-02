# cython: language_level=3
# distutils: language = c

from openptv.binding.calibration cimport calibration
from openptv.binding.parameters cimport mm_np, volume_par
from openptv.binding.vec_utils cimport vec3d

cdef extern from "../liboptv/include/epi.h":
    void  epi_mm_2D (double xl, double yl, calibration *cal, mm_np *mmp, 
        volume_par *vpar, vec3d out);