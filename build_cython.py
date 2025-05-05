"""
Script to build Cython extensions directly.
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

# Create extensions for all .pyx files
cython_files = glob.glob('./openptv/binding/*.pyx')
extensions = []

for pyx_file in cython_files:
    # Get the module name from the .pyx file path
    module_name = os.path.splitext(os.path.basename(pyx_file))[0]
    module_path = f"openptv.binding.{module_name}"
    
    # Create an extension for this module
    extensions.append(
        Extension(
            module_path,
            [pyx_file] + get_liboptv_sources(),
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
    )

# Build the extensions
cythonize(
    extensions,
    compiler_directives={
        'language_level': '3',
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
    },
    force=True,
)

print("Cython extensions built successfully!")
