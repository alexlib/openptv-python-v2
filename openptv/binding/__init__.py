"""
Cython bindings to the liboptv C library.

This module provides Python access to the high-performance C implementation
of the OpenPTV algorithms.
"""

# Import Cython-wrapped functions here
try:
    from .tracking_cy import track_particles_py as track_particles
    from .tracking_cy import find_correspondences_py as find_correspondences
except ImportError:
    # If Cython bindings are not available, this will be caught by the main __init__.py
    pass
