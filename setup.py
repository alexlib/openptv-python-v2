"""
Setup script for the openptv-python package.
"""

import os
import sys
import glob
import re
import importlib.util
import site
import numpy
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
from setuptools.command.develop import develop
from Cython.Build import cythonize

def patch_chaco_for_numpy_compatibility():
    """
    Patch Chaco files to work with newer versions of NumPy.

    This function patches the Chaco library files to replace deprecated NumPy functions
    with their modern equivalents:
    - sometrue -> any
    - alltrue -> all
    """
    try:
        # Find all site-packages directories
        site_packages = site.getsitepackages()

        # Add user site-packages if it exists
        if site.USER_SITE:
            site_packages.append(site.USER_SITE)

        # Files to patch and their replacements
        files_to_patch = {
            'chaco/log_mapper.py': [
                (r'from numpy import \(([^)]*?)sometrue([^)]*?)\)', r'from numpy import \g<1>any as sometrue\g<2>)'),
                (r'from numpy import \(([^)]*?)alltrue([^)]*?)\)', r'from numpy import \g<1>all as alltrue\g<2>)')
            ],
            'chaco/grid_mapper.py': [
                (r'from numpy import \(([^)]*?)sometrue([^)]*?)\)', r'from numpy import \g<1>any as sometrue\g<2>)'),
                (r'from numpy import \(([^)]*?)alltrue([^)]*?)\)', r'from numpy import \g<1>all as alltrue\g<2>)')
            ]
        }

        patched_files = []

        # Try to find and patch each file
        for site_pkg in site_packages:
            for file_path, replacements in files_to_patch.items():
                full_path = os.path.join(site_pkg, file_path)
                if os.path.exists(full_path):
                    try:
                        with open(full_path, 'r') as f:
                            content = f.read()

                        # Apply all replacements
                        modified = False
                        for pattern, replacement in replacements:
                            new_content = re.sub(pattern, replacement, content)
                            if new_content != content:
                                content = new_content
                                modified = True

                        # Only write if changes were made
                        if modified:
                            with open(full_path, 'w') as f:
                                f.write(content)
                            patched_files.append(full_path)
                            print(f"Patched {full_path} for NumPy compatibility")
                    except Exception as e:
                        print(f"Error patching {full_path}: {str(e)}")

        if not patched_files:
            print("No Chaco files were found or needed patching")

        return patched_files

    except Exception as e:
        print(f"Error during patching: {str(e)}")
        return []

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


class CustomInstall(install):
    """Custom install command that applies patches after installation"""

    def run(self):
        # Run the standard install
        install.run(self)

        # Apply patches after installation
        print("Applying patches for NumPy compatibility...")
        patch_chaco_for_numpy_compatibility()


class CustomDevelop(develop):
    """Custom develop command that applies patches after development installation"""

    def run(self):
        # Run the standard develop command
        develop.run(self)

        # Apply patches after development installation
        print("Applying patches for NumPy compatibility...")
        patch_chaco_for_numpy_compatibility()


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


# Create extensions with explicit module names and in a specific order
extensions = [
    # Build vec_utils first as it's needed by other modules
    create_extension('openptv.binding.vec_utils', ['./openptv/binding/vec_utils.pyx']),

    # Build parameters next as it's needed by many modules
    create_extension('openptv.binding.parameters', ['./openptv/binding/parameters.pyx']),

    # Build the rest of the modules
    create_extension('openptv.binding.calibration', ['./openptv/binding/calibration.pyx']),
    create_extension('openptv.binding.transforms', ['./openptv/binding/transforms.pyx']),
    create_extension('openptv.binding.tracking_framebuf', ['./openptv/binding/tracking_framebuf.pyx']),
    create_extension('openptv.binding.imgcoord', ['./openptv/binding/imgcoord.pyx']),
    create_extension('openptv.binding.orientation', ['./openptv/binding/orientation.pyx']),
    create_extension('openptv.binding.segmentation', ['./openptv/binding/segmentation.pyx']),
    create_extension('openptv.binding.tracker', ['./openptv/binding/tracker.pyx']),
    create_extension('openptv.binding.correspondences', ['./openptv/binding/correspondences.pyx']),
    create_extension('openptv.binding.epipolar', ['./openptv/binding/epipolar.pyx']),
    create_extension('openptv.binding.image_processing', ['./openptv/binding/image_processing.pyx']),
]

# Use cythonize on the extensions
ext_modules = cythonize(
    extensions,
    compiler_directives={
        'language_level': '3',
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
    },
    include_path=['./openptv/binding/']
)

# Get version from openptv/__init__.py
with open('openptv/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break
    else:
        version = '0.1.1'  # Default if not found

# Package metadata
setup(
    name="openptv-python",
    version=version,
    description="Python package for Particle Tracking Velocimetry",
    author="OpenPTV Contributors",
    author_email="alex@libptv.org",
    url="https://github.com/alexlib/openptv-python-v2",
    packages=find_packages(),
    ext_modules=ext_modules,  # Use the cythonized extensions
    include_dirs=[numpy.get_include()],
    cmdclass={
        'build_ext': CustomBuildExt,
        'install': CustomInstall,
        'develop': CustomDevelop,
    },
    install_requires=[
        "numpy>=1.19.0,<2.0",
        "scipy>=1.5.0",
        "tqdm>=4.60.0",  # Add tqdm as a dependency
        "imagecodecs>=2021.0.0",  # Add imagecodecs for image processing
        "PyYAML>=6.0",  # Add PyYAML for configuration files
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
        'console_scripts': [
            'openptv-gui=openptv.gui.cli:cli',
            'pyptv=openptv.gui.pyptv_gui:main_cli',
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

# Apply patches immediately if this is a direct installation
if __name__ == "__main__" and any(arg.startswith(("install", "develop")) for arg in sys.argv):
    print("Applying patches for NumPy compatibility during direct installation...")
    patch_chaco_for_numpy_compatibility()
