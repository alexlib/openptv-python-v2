"""
Pure Python implementation of OpenPTV algorithms.

This module provides a Python implementation of the same functionality
available in the C library. It serves as:
1. A fallback when the C library is not available
2. A development environment for prototyping and debugging new algorithms
3. A reference implementation with clearer code than the C version

The API is designed to match the Cython bindings, allowing seamless
switching between implementations.
"""

# Import Python implementations here
from .tracking import track_particles, find_correspondences

# Flag to indicate that this is the Python implementation
__is_cython__ = False

def using_cython():
    """Return True if using the Cython implementation, False if using Python."""
    return __is_cython__
