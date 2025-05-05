"""
Script to build the vec_utils Cython extension directly.
"""

import os
import sys
import glob
import numpy
from setuptools import Extension
from Cython.Build import cythonize

# Get all C source files from liboptv
def get_liboptv_sources():
    return glob.glob('./openptv/liboptv/src/*.c')

# Create an extension for vec_utils
extension = Extension(
    "openptv.binding.vec_utils",
    ['./openptv/binding/vec_utils.pyx'] + get_liboptv_sources(),
    include_dirs=[
        numpy.get_include(),
        './openptv/liboptv/include/',
        './openptv/binding/',
        os.path.abspath('./openptv/liboptv/include/'),
        os.path.abspath('./openptv/binding/'),
    ],
    extra_compile_args=['/W4'] if sys.platform.startswith('win') else ['-Wno-cpp', '-Wno-unused-function'],
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
)

# Build the extension
cythonize(
    extension,
    compiler_directives={
        'language_level': '3',
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
    },
    force=True,
)

print("vec_utils extension built successfully!")
