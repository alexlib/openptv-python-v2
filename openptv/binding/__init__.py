"""
OpenPTV Cython bindings for the liboptv C library.

This package provides Cython bindings for the liboptv C library,
allowing Python code to call the C functions directly.
"""

from openptv.binding.utils import encode_if_needed, decode_if_needed

__all__ = ['encode_if_needed', 'decode_if_needed']
