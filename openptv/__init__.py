"""
OpenPTV Python package for Particle Tracking Velocimetry.

This package provides tools for PTV analysis with a flexible architecture:
- High-performance C implementation (liboptv)
- Cython bindings for Python access to C functions
- Pure Python implementation for development and fallback
- GUI components based on TraitsUI/Chaco/Enable/Pyface
"""

import importlib.util
import sys
import warnings
import os

__version__ = '0.1.0'

# Try to import the Cython bindings
try:
    # Import core tracking functions
    from openptv.binding.tracking_cy import track_particles_py as track_particles
    from openptv.binding.tracking_cy import find_correspondences_py as find_correspondences

    _using_cython = True

except ImportError as e:
    # Fall back to pure Python implementation
    warnings.warn(
        f"Cython bindings not available ({e}), using pure Python implementation. "
        "This may be significantly slower for large datasets."
    )

    from openptv.pyoptv.tracking import track_particles, find_correspondences

    _using_cython = False

def using_cython():
    """Return True if using Cython bindings, False if using pure Python."""
    return _using_cython

# Import GUI components if available
try:
    from openptv.gui import pyptv_gui
    _gui_available = True
except ImportError:
    _gui_available = False

def is_gui_available():
    """Return True if GUI components are available, False otherwise."""
    return _gui_available

def run_gui():
    """Run the OpenPTV GUI application."""
    if not _gui_available:
        raise ImportError(
            "GUI components are not available. Make sure the required dependencies "
            "are installed: pip install openptv-python[gui]"
        )

    from openptv.gui.pyptv_gui import PYPTV_GUI
    gui = PYPTV_GUI()
    gui.configure_traits()
    return gui
