"""
Utility functions for handling string/bytes conversion in a cross-platform way.

This module provides functions to ensure consistent handling of strings, bytes, and paths
across different platforms (Windows, macOS, Linux) and between Python, Cython, and C code.
"""

import os
import sys
from pathlib import Path
from typing import Union, Optional, Any, List, Tuple

# Type alias for path-like objects
PathLike = Union[str, bytes, Path, None]


def ensure_bytes(s: PathLike) -> Optional[bytes]:
    """
    Convert a string, Path, or bytes to bytes, or return None if input is None.
    
    Args:
        s: String, bytes, Path object, or None
        
    Returns:
        Bytes representation or None if input is None
        
    Raises:
        TypeError: If the input cannot be converted to bytes
    """
    if s is None:
        return None
    if isinstance(s, bytes):
        return s
    if isinstance(s, Path):
        s = str(s)
    if isinstance(s, str):
        return s.encode('utf-8')
    raise TypeError(f"Cannot convert {type(s)} to bytes")


def ensure_str(b: PathLike) -> Optional[str]:
    """
    Convert bytes, Path, or string to string, or return None if input is None.
    
    Args:
        b: Bytes, string, Path object, or None
        
    Returns:
        String representation or None if input is None
        
    Raises:
        TypeError: If the input cannot be converted to string
    """
    if b is None:
        return None
    if isinstance(b, str):
        return b
    if isinstance(b, Path):
        return str(b)
    if isinstance(b, bytes):
        return b.decode('utf-8')
    raise TypeError(f"Cannot convert {type(b)} to str")


def ensure_path(p: PathLike) -> Optional[Path]:
    """
    Convert string, bytes, or Path to Path, or return None if input is None.
    
    Args:
        p: String, bytes, Path object, or None
        
    Returns:
        Path object or None if input is None
        
    Raises:
        TypeError: If the input cannot be converted to Path
    """
    if p is None:
        return None
    if isinstance(p, Path):
        return p
    if isinstance(p, bytes):
        return Path(b.decode('utf-8'))
    if isinstance(p, str):
        return Path(p)
    raise TypeError(f"Cannot convert {type(p)} to Path")


def normalize_path_separators(path: PathLike) -> str:
    """
    Normalize path separators to the current platform's standard.
    
    Args:
        path: Path as string, bytes, or Path object
        
    Returns:
        Normalized path string
    """
    path_str = ensure_str(path)
    if path_str is None:
        return None
    
    # Replace both types of separators with os.sep
    normalized = path_str.replace('\\', os.sep).replace('/', os.sep)
    return normalized


def ensure_directory_exists(path: PathLike) -> Path:
    """
    Ensure that the directory for the given path exists.
    
    Args:
        path: Path to a file or directory
        
    Returns:
        Path object for the created/existing directory
    """
    path_obj = ensure_path(path)
    if path_obj is None:
        raise ValueError("Cannot create directory for None path")
    
    # If path is a file path, get its parent directory
    if path_obj.suffix:
        directory = path_obj.parent
    else:
        directory = path_obj
    
    # Create directory if it doesn't exist
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def path_with_suffix(path: PathLike, suffix: str) -> Path:
    """
    Return a new path with the given suffix.
    
    Args:
        path: Original path
        suffix: New suffix (e.g., '.txt', '10000')
        
    Returns:
        New Path object with the suffix
    """
    path_obj = ensure_path(path)
    if path_obj is None:
        raise ValueError("Cannot add suffix to None path")
    
    # If suffix doesn't start with a dot and we're adding a file extension, add it
    if not suffix.startswith('.') and '.' in suffix:
        suffix = '.' + suffix
        
    return path_obj.with_suffix(suffix)


def join_path(base: PathLike, *parts: str) -> Path:
    """
    Join path components in a cross-platform way.
    
    Args:
        base: Base path
        *parts: Additional path components
        
    Returns:
        Joined Path object
    """
    base_path = ensure_path(base)
    if base_path is None:
        raise ValueError("Cannot join with None base path")
    
    result = base_path
    for part in parts:
        result = result / part
    
    return result
