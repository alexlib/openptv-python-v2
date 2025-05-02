"""
Setup script for the openptv-python package.
"""

import os
import sys
import numpy
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

# Define the extension modules
extensions = [
    Extension(
        "openptv.binding.tracking_cy",
        ["openptv/binding/tracking_cy.pyx", "liboptv/src/tracking.c"],
        include_dirs=[numpy.get_include(), "liboptv/include"],
        language="c",
    ),
    # Add more extensions as needed
]

# Cythonize the extensions
ext_modules = cythonize(extensions)

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
    install_requires=[
        "numpy",
        "scipy",
        "traits",
        "traitsui",
        "chaco",
        "enable",
        "pyface",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "flake8",
            "black",
            "sphinx",
            "sphinx_rtd_theme",
        ],
        "gui": [
            "pyside6",  # or "pyqt5"
            "pillow",
            "matplotlib",
        ],
        "dist": [
            "wheel",
            "build",
            "twine",
            "cibuildwheel",
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
        "Programming Language :: C",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.7",
)
