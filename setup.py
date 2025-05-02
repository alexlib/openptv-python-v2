"""
Setup script for the openptv-python package.
"""

import os
import sys
import subprocess
import numpy
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.develop import develop
from setuptools.command.install import install
from Cython.Build import cythonize

# Check if we're in a Git repository
is_git_repo = os.path.exists('.git')

# Custom commands to initialize submodules
def init_submodules():
    """Initialize Git submodules if they're not already initialized."""
    if is_git_repo:
        print("Initializing Git submodules...")
        try:
            subprocess.check_call(['git', 'submodule', 'update', '--init', '--recursive'])
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Warning: Failed to initialize Git submodules: {e}")
            print("You may need to initialize them manually with: git submodule update --init --recursive")

class DevelopCommand(develop):
    """Custom develop command to initialize submodules."""
    def run(self):
        init_submodules()
        develop.run(self)

class InstallCommand(install):
    """Custom install command to initialize submodules."""
    def run(self):
        init_submodules()
        install.run(self)

class BuildExtCommand(build_ext):
    """Custom build_ext command to initialize submodules."""
    def run(self):
        init_submodules()
        build_ext.run(self)

# Define the extension modules
extensions = [
    Extension(
        "openptv.binding.tracking_cy",
        [
            "openptv/binding/tracking_cy.pyx",
            "openptv/binding/optv.c",  # Our implementation of the functions
            # Commenting out the liboptv sources for now until we properly integrate them
            # "liboptv/liboptv/src/track.c",
            # "liboptv/liboptv/src/tracking_frame_buf.c",
            # "liboptv/liboptv/src/parameters.c",
            # "liboptv/liboptv/src/calibration.c",
            # "liboptv/liboptv/src/orientation.c",
            # "liboptv/liboptv/src/trafo.c",
            # "liboptv/liboptv/src/multimed.c",
            # "liboptv/liboptv/src/imgcoord.c",
            # "liboptv/liboptv/src/ray_tracing.c",
            # "liboptv/liboptv/src/lsqadj.c",
            # "liboptv/liboptv/src/vec_utils.c",
            # "liboptv/liboptv/src/correspondences.c",
            # "liboptv/liboptv/src/epi.c",
            # "liboptv/liboptv/src/segmentation.c",
            # "liboptv/liboptv/src/tracking_run.c",
            # "liboptv/liboptv/src/sortgrid.c",
            # "liboptv/liboptv/src/image_processing.c",
        ],
        include_dirs=[
            numpy.get_include(),
            "openptv/binding",  # For optv.h
            "liboptv/liboptv/include",  # Keep this for future integration
        ],
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
    cmdclass={
        'develop': DevelopCommand,
        'install': InstallCommand,
        'build_ext': BuildExtCommand,
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
    # Include data files from submodules
    package_data={
        'openptv': ['binding/*.pyx', 'binding/*.pxd'],
    },
    include_package_data=True,
)
