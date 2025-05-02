"""
OpenPTV Python package for Particle Tracking Velocimetry.

This package provides tools for PTV analysis with a flexible architecture:
- High-performance C implementation (liboptv)
- Cython bindings for Python access to C functions
- Pure Python implementation for development and fallback
- GUI components based on TraitsUI/Chaco/Enable/Pyface
"""

import importlib.util
import sys
import warnings

__version__ = '0.1.0'

# Try to import the Cython bindings
try:
    from openptv.binding.tracking_cy import track_particles_py as track_particles
    from openptv.binding.tracking_cy import find_correspondences_py as find_correspondences
    _using_cython = True
except ImportError:
    # Fall back to pure Python implementation
    from openptv.pyoptv.tracking import track_particles, find_correspondences
    _using_cython = False
    warnings.warn(
        "Cython bindings not available, using pure Python implementation. "
        "This may be significantly slower for large datasets."
    )

def using_cython():
    """Return True if using Cython bindings, False if using pure Python."""
    return _using_cython
