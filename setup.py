"""
Setup script for the openptv-python package.
"""

import os
import sys
import glob
import numpy
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

class CustomBuildExt(build_ext):
    """Custom build_ext command with optimized compiler flags"""
    
    def finalize_options(self):
        build_ext.finalize_options(self)
        # Add NumPy include directory
        self.include_dirs.append(numpy.get_include())
    
    def build_extensions(self):
        # Customize compiler options if needed
        if self.compiler.compiler_type == 'unix':
            for e in self.extensions:
                e.extra_compile_args = ['-O3', '-ffast-math', '-march=native']
        build_ext.build_extensions(self)


def get_liboptv_sources():
    """Get all C source files from liboptv"""
    return glob.glob('./openptv/liboptv/src/*.c')


def create_extension(name, sources):
    """Create an Extension object with common settings"""
    
    extra_compile_args = []
    extra_link_args = []
    
    # Set platform-specific compiler flags
    if not sys.platform.startswith('win'):
        extra_compile_args.extend(['-Wno-cpp', '-Wno-unused-function'])
        extra_link_args.extend(['-Wl,-rpath,$ORIGIN'])
    else:
        extra_compile_args.append('/W4')
    
    include_dirs = [
        numpy.get_include(),
        './openptv/liboptv/include/',
        './openptv/binding/',
    ]
    
    # Add absolute paths for Windows
    if sys.platform.startswith('win'):
        include_dirs.extend([
            os.path.abspath('./openptv/liboptv/include/'),
            os.path.abspath('./openptv/binding/'),
        ])
    
    return Extension(
        name,
        sources + get_liboptv_sources(),
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    )


# First, cythonize all .pyx files to generate .c files
cython_files = glob.glob('./openptv/binding/*.pyx')
cythonize(
    cython_files,
    compiler_directives={
        'language_level': '3',
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
    }
)

# Now create extensions from the generated .c files
extensions = []

# Create extensions for openptv package only
for pyx_file in cython_files:
    # Get the module name from the .pyx file path
    module = os.path.splitext(pyx_file)[0].replace(os.path.sep, '.')
    # Get the corresponding .c file
    c_file = os.path.splitext(pyx_file)[0] + '.c'
    # Create an extension for this module
    extensions.append(create_extension(module, [c_file]))

# Package metadata
setup(
    name="openptv-python",
    version="0.1.0",
    description="Python package for Particle Tracking Velocimetry",
    author="OpenPTV Contributors",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/openptv-python-v2",
    packages=find_packages(),
    ext_modules=extensions,
    include_dirs=[numpy.get_include()],
    cmdclass={
        'build_ext': CustomBuildExt,
    },
    install_requires=[
        "numpy>=1.19.0,<2.0",
        "scipy>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "flake8>=3.8.0",
            "black>=20.8b1",
            "sphinx>=3.2.0",
            "sphinx_rtd_theme>=0.5.0",
        ],
        "gui": [
            "traits>=6.1.0",
            "traitsui>=7.1.0",
            "chaco>=4.8.0",
            "enable>=4.8.0",
            "pyface>=7.1.0",
            "pillow>=8.0.0",
            "matplotlib>=3.3.0",
            "scikit-image>=0.18.0",  # For image processing functions
            "pandas>=1.3.0",  # For data handling
            # Optional dependencies that might be difficult to install
            # "pyqt5>=5.15.0",  # Using PyQt5 for compatibility with the existing GUI
            # "flowtracks>=0.1.0",  # For trajectory analysis
        ],
        "dist": [
            "wheel>=0.35.0",
            "build>=0.5.0",
            "twine>=3.3.0",
            "cibuildwheel>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "openptv-gui=openptv.gui.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: C",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.7",
    zip_safe=False,  # Required for Cython extensions
    include_package_data=True,
    package_data={
        'openptv': [
            'liboptv/include/*.h',
            'binding/*.pxd',
        ],
    },
)
