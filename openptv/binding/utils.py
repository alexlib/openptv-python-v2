"""Utility functions for OpenPTV bindings."""

from typing import Union
Str = Union[str, bytes]

def encode_if_needed(s: Str) -> bytes:
    """
    Encode a string to UTF-8 bytes if it's a string, otherwise return as is.
    
    Args:
        s: String or bytes object
        
    Returns:
        Bytes object
    """
    if isinstance(s, str):
        return s.encode('utf-8')
    return s  # Already bytes or None

def decode_if_needed(b: Str) -> str:
    """
    Decode bytes to UTF-8 string if it's bytes, otherwise return as is.
    
    Args:
        b: Bytes or string object
        
    Returns:
        String object
    """
    if isinstance(b, bytes):
        return b.decode('utf-8')
    return b  # Already string or None