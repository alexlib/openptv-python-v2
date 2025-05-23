# cython: language_level=3
# distutils: language = c

from openptv.binding.parameters cimport control_par

cdef extern from "../liboptv/include/image_processing.h":
    int prepare_image(unsigned char * img,
                        unsigned char * img_hp,
                        int dim_lp,
                        int filter_hp,
                        char * filter_file,
                        control_par * cpar)
