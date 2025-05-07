"""
Utility functions for OpenPTV.

This module provides helper functions and utilities used across the package.
"""

# String and path utilities
from openptv.utils.string_utils import (
    ensure_bytes,
    ensure_str,
    ensure_path,
    normalize_path_separators,
    ensure_directory_exists,
    path_with_suffix,
    join_path
)

# Path configuration
from openptv.utils.path_config import PathConfig, path_config

# Decorators
from openptv.utils.decorators import string_bytes_handler, path_handler

# Naming utilities
from openptv.utils.naming import (
    get_default_naming,
    get_default_naming_str,
    get_default_naming_path,
    ensure_naming_directories,
    get_path_with_frame,
    get_str_with_frame,
    get_bytes_with_frame
)

__all__ = [
    # String utilities
    'ensure_bytes',
    'ensure_str',
    'ensure_path',
    'normalize_path_separators',
    'ensure_directory_exists',
    'path_with_suffix',
    'join_path',

    # Path configuration
    'PathConfig',
    'path_config',

    # Decorators
    'string_bytes_handler',
    'path_handler',

    # Naming utilities
    'get_default_naming',
    'get_default_naming_str',
    'get_default_naming_path',
    'ensure_naming_directories',
    'get_path_with_frame',
    'get_str_with_frame',
    'get_bytes_with_frame'
]
