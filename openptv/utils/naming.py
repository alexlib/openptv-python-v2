"""
Naming utilities for OpenPTV.

This module provides utilities for handling file naming conventions in OpenPTV.
"""

from typing import Dict, Union, Optional
from pathlib import Path

from openptv.utils.string_utils import ensure_bytes, ensure_str, ensure_path
from openptv.utils.path_config import path_config


def get_default_naming() -> Dict[str, bytes]:
    """
    Get default naming dictionary with bytes values for C code.
    
    Returns:
        Dictionary with default naming conventions as bytes
    """
    return {
        'corres': path_config.get_bytes('corres'),
        'linkage': path_config.get_bytes('linkage'),
        'prio': path_config.get_bytes('prio')
    }


def get_default_naming_str() -> Dict[str, str]:
    """
    Get default naming dictionary with string values for Python code.
    
    Returns:
        Dictionary with default naming conventions as strings
    """
    return {
        'corres': path_config.get_str('corres'),
        'linkage': path_config.get_str('linkage'),
        'prio': path_config.get_str('prio')
    }


def get_default_naming_path() -> Dict[str, Path]:
    """
    Get default naming dictionary with Path values for Python code.
    
    Returns:
        Dictionary with default naming conventions as Path objects
    """
    return {
        'corres': path_config.get_path('corres'),
        'linkage': path_config.get_path('linkage'),
        'prio': path_config.get_path('prio')
    }


def ensure_naming_directories() -> None:
    """
    Ensure that all directories in the default naming system exist.
    """
    path_config.ensure_directory('corres')
    path_config.ensure_directory('linkage')
    path_config.ensure_directory('prio')


def get_path_with_frame(key: str, frame: int) -> Path:
    """
    Get a path with a frame number suffix.
    
    Args:
        key: Path key ('corres', 'linkage', or 'prio')
        frame: Frame number
        
    Returns:
        Path with frame number suffix
    """
    return path_config.with_suffix(key, f'.{frame}')


def get_str_with_frame(key: str, frame: int) -> str:
    """
    Get a string path with a frame number suffix.
    
    Args:
        key: Path key ('corres', 'linkage', or 'prio')
        frame: Frame number
        
    Returns:
        String path with frame number suffix
    """
    return str(get_path_with_frame(key, frame))


def get_bytes_with_frame(key: str, frame: int) -> bytes:
    """
    Get a bytes path with a frame number suffix.
    
    Args:
        key: Path key ('corres', 'linkage', or 'prio')
        frame: Frame number
        
    Returns:
        Bytes path with frame number suffix
    """
    return get_str_with_frame(key, frame).encode('utf-8')
