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

# Get all C source files
c_sources = glob.glob("openptv/liboptv/src/*.c")

# Define the extension modules
extensions = [
    # Main tracking extension
    Extension(
        "openptv.binding.tracking_cy",
        ["openptv/binding/tracking_cy.pyx", "openptv/binding/optv.c"],
        include_dirs=[
            numpy.get_include(),
            "openptv/binding",
            "openptv/liboptv/include",
        ],
        language="c",
    ),

    # For now, we'll only include the tracking_cy extension
    # We'll add the other extensions once we fix the .pxd file issues
]

# Cythonize the extensions with compiler directives
compiler_directives = {
    'language_level': 3,
    'boundscheck': False,
    'wraparound': False,
    'initializedcheck': False,
    'nonecheck': False,
}

ext_modules = cythonize(
    extensions,
    compiler_directives=compiler_directives,
)

# Custom build_ext command to handle binary wheels
class CustomBuildExt(build_ext):
    def build_extensions(self):
        # Customize compiler options if needed
        if self.compiler.compiler_type == 'unix':
            for e in self.extensions:
                e.extra_compile_args = ['-O3', '-ffast-math', '-march=native']
        build_ext.build_extensions(self)

# Package metadata
setup(
    name="openptv-python",
    version="0.1.0",
    description="Python package for Particle Tracking Velocimetry",
    author="OpenPTV Contributors",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/openptv-python-v2",
    packages=find_packages(),
    ext_modules=ext_modules,
    include_dirs=[numpy.get_include()],
    cmdclass={'build_ext': CustomBuildExt},
    install_requires=[
        "numpy>=1.19.0",
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
            "pyside6>=6.0.0",  # or "pyqt5>=5.15.0"
            "pillow>=8.0.0",
            "matplotlib>=3.3.0",
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
