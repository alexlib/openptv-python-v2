"""
Utility functions for the Cython bindings.
"""

def encode_if_needed(s):
    """Encode a string if needed."""
    if isinstance(s, str):
        return s.encode('utf-8')
    return s

def decode_if_needed(s):
    """Decode a string if needed."""
    if isinstance(s, bytes):
        return s.decode('utf-8')
    return s
