"""
OpenPTV Python package for Particle Tracking Velocimetry.

This package provides tools for PTV analysis with a flexible architecture:
- High-performance C implementation (liboptv)
- Cython bindings for Python access to C functions
- Pure Python implementation for development and fallback
- GUI components based on TraitsUI/Chaco/Enable/Pyface
"""

import importlib.util
import os
import sys
import warnings

__version__ = '0.1.0'

# Try to import the Cython bindings
try:
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

# Try to import GUI components
try:
    # Defer the actual import to avoid circular imports
    def is_gui_available():
        """Return True if GUI components are available, False otherwise."""
        try:
            from openptv.gui import gui_available
            return gui_available
        except ImportError:
            return False

    def launch_gui():
        """Run the OpenPTV GUI application."""
        try:
            from openptv.gui import launch_gui as _launch_gui
            return _launch_gui()
        except ImportError:
            raise ImportError(
                "GUI components are not available. Make sure the required dependencies "
                "are installed: traitsui, chaco, enable, pyface."
            )

    _gui_available = is_gui_available()
except ImportError:
    _gui_available = False

    def is_gui_available():
        """Return True if GUI components are available, False otherwise."""
        return False

    def launch_gui():
        """Placeholder function when GUI is not available."""
        raise ImportError(
            "GUI components are not available. Make sure the required dependencies "
            "are installed: traitsui, chaco, enable, pyface."
        )

def is_gui_available():
    """Return True if GUI components are available, False otherwise."""
    return _gui_available

# Define a function to run the GUI
def run_gui():
    """Run the OpenPTV GUI application."""
    if not _gui_available:
        raise ImportError(
            "GUI components are not available. Make sure the required dependencies "
            "are installed: traitsui, chaco, enable, pyface."
        )

    # Launch the GUI
    return launch_gui()
