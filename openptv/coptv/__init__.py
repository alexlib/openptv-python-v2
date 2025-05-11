"""
OpenPTV Cython bindings for the liboptv C library.

This package provides Cython bindings for the liboptv C library,
allowing Python code to call the C functions directly.
"""

# Import utility functions for string/bytes conversion
from openptv.coptv.utils import encode_if_needed, decode_if_needed

__all__ = ['encode_if_needed', 'decode_if_needed']
