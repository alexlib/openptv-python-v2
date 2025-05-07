"""
Configuration system for file paths used in OpenPTV.

This module provides a centralized configuration system for managing file paths
used throughout the OpenPTV codebase, ensuring consistent handling across
different platforms and between Python, Cython, and C code.
"""

import os
from pathlib import Path
from typing import Dict, Union, Optional, Any

from openptv.utils.string_utils import (
    ensure_bytes,
    ensure_str,
    ensure_path,
    ensure_directory_exists
)

class PathConfig:
    """
    Configuration for file paths used in OpenPTV.
    
    This class provides a centralized way to manage file paths used in OpenPTV,
    ensuring consistent handling of paths across different platforms and between
    Python, Cython, and C code.
    """
    
    def __init__(self):
        """Initialize with default paths."""
        self._paths = {
            'corres': Path('res/rt_is'),
            'linkage': Path('res/ptv_is'),
            'prio': Path('res/added'),
            'calibration': Path('cal'),
            'parameters': Path('parameters'),
            'img_base': Path('img'),
            'res': Path('res')
        }
    
    def get_path(self, key: str) -> Path:
        """
        Get a path by key.
        
        Args:
            key: Path key
            
        Returns:
            Path object
            
        Raises:
            KeyError: If the key is not found
        """
        return self._paths[key]
    
    def set_path(self, key: str, path: Union[str, bytes, Path]) -> None:
        """
        Set a path by key.
        
        Args:
            key: Path key
            path: New path value
            
        Raises:
            TypeError: If the path cannot be converted to a Path object
        """
        self._paths[key] = ensure_path(path)
    
    def get_str(self, key: str) -> str:
        """
        Get a path as a string.
        
        Args:
            key: Path key
            
        Returns:
            Path as a string
            
        Raises:
            KeyError: If the key is not found
        """
        return str(self._paths[key])
    
    def get_bytes(self, key: str) -> bytes:
        """
        Get a path as bytes.
        
        Args:
            key: Path key
            
        Returns:
            Path as bytes
            
        Raises:
            KeyError: If the key is not found
        """
        return str(self._paths[key]).encode('utf-8')
    
    def ensure_directories(self) -> None:
        """
        Ensure all directories exist.
        
        Creates all directories in the configuration if they don't exist.
        """
        for path in self._paths.values():
            directory = path
            if path.suffix:  # If it's a file path, get the parent directory
                directory = path.parent
            directory.mkdir(parents=True, exist_ok=True)
    
    def ensure_directory(self, key: str) -> Path:
        """
        Ensure a specific directory exists.
        
        Args:
            key: Path key
            
        Returns:
            Path to the created/existing directory
            
        Raises:
            KeyError: If the key is not found
        """
        return ensure_directory_exists(self._paths[key])
    
    def with_suffix(self, key: str, suffix: str) -> Path:
        """
        Get a path with a specific suffix.
        
        Args:
            key: Path key
            suffix: Suffix to add (e.g., '.txt', '10000')
            
        Returns:
            Path with the suffix
            
        Raises:
            KeyError: If the key is not found
        """
        path = self._paths[key]
        
        # If suffix doesn't start with a dot and we're adding a file extension, add it
        if not suffix.startswith('.') and '.' in suffix:
            suffix = '.' + suffix
            
        return path.with_suffix(suffix)
    
    def join(self, key: str, *parts: str) -> Path:
        """
        Join a base path with additional parts.
        
        Args:
            key: Path key for the base path
            *parts: Additional path components
            
        Returns:
            Joined path
            
        Raises:
            KeyError: If the key is not found
        """
        base = self._paths[key]
        result = base
        for part in parts:
            result = result / part
        return result


# Create a global instance
path_config = PathConfig()
