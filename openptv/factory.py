"""
Factory for creating appropriate OpenPTV implementation.
"""
import os
import sys

def get_ptv_implementation(prefer_c=True):
    """Factory function to get the appropriate implementation
    
    Args:
        prefer_c: Whether to try C implementation first
        
    Returns:
        An implementation of PTV_Interface
    """
    if prefer_c:
        try:
            from openptv.c_implementation import CPTVImplementation
            impl = CPTVImplementation()
            print(f"Using {impl.implementation_name}")
            return impl
        except ImportError as e:
            print(f"Warning: C implementation not available: {e}")
            print("Falling back to Python implementation...")
    
    try:
        from openptv.py_implementation import PyPTVImplementation
        impl = PyPTVImplementation()
        print(f"Using {impl.implementation_name}")
        return impl
    except ImportError as e:
        raise ImportError(f"No implementation available: {e}")
