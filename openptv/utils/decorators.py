"""
Decorators for OpenPTV.

This module provides decorators used throughout the OpenPTV codebase to handle
common patterns like string/bytes conversion, error handling, etc.
"""

import functools
import inspect
from typing import Callable, Any, Dict, List, Union, Optional, TypeVar

from openptv.utils.string_utils import ensure_bytes, ensure_str, ensure_path

# Type variables for better type hints
F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')


def string_bytes_handler(param_names: Union[str, List[str]], return_as_str: bool = True) -> Callable[[F], F]:
    """
    Decorator to handle string/bytes conversion for parameters and return values.
    
    Args:
        param_names: Name(s) of parameters to convert to bytes
        return_as_str: Whether to convert return value to string if it's bytes
        
    Returns:
        Decorated function
    """
    if isinstance(param_names, str):
        param_names = [param_names]
        
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get the function's signature
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(*args, **kwargs)
            
            # Convert positional arguments if they match parameter names
            new_args = list(args)
            for i, (param_name, param) in enumerate(sig.parameters.items()):
                if i < len(args) and param_name in param_names:
                    new_args[i] = ensure_bytes(args[i])
            
            # Convert keyword arguments
            new_kwargs = kwargs.copy()
            for param_name in param_names:
                if param_name in kwargs:
                    new_kwargs[param_name] = ensure_bytes(kwargs[param_name])
            
            # Call the function with converted arguments
            result = func(*new_args, **new_kwargs)
            
            # Convert return value if needed
            if return_as_str and isinstance(result, bytes):
                return ensure_str(result)
            return result
        
        return wrapper
    
    return decorator


def path_handler(param_names: Union[str, List[str]], ensure_exists: bool = False) -> Callable[[F], F]:
    """
    Decorator to handle path conversion for parameters.
    
    Args:
        param_names: Name(s) of parameters to convert to Path objects
        ensure_exists: Whether to ensure directories exist for the paths
        
    Returns:
        Decorated function
    """
    if isinstance(param_names, str):
        param_names = [param_names]
        
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get the function's signature
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(*args, **kwargs)
            
            # Convert positional arguments if they match parameter names
            new_args = list(args)
            for i, (param_name, param) in enumerate(sig.parameters.items()):
                if i < len(args) and param_name in param_names:
                    path = ensure_path(args[i])
                    if ensure_exists and path is not None:
                        if path.suffix:  # If it's a file path
                            path.parent.mkdir(parents=True, exist_ok=True)
                        else:  # If it's a directory path
                            path.mkdir(parents=True, exist_ok=True)
                    new_args[i] = path
            
            # Convert keyword arguments
            new_kwargs = kwargs.copy()
            for param_name in param_names:
                if param_name in kwargs:
                    path = ensure_path(kwargs[param_name])
                    if ensure_exists and path is not None:
                        if path.suffix:  # If it's a file path
                            path.parent.mkdir(parents=True, exist_ok=True)
                        else:  # If it's a directory path
                            path.mkdir(parents=True, exist_ok=True)
                    new_kwargs[param_name] = path
            
            # Call the function with converted arguments
            return func(*new_args, **new_kwargs)
        
        return wrapper
    
    return decorator
