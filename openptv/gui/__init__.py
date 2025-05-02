"""
GUI components for OpenPTV based on TraitsUI/Chaco/Enable/Pyface.

This module provides visualization and user interface components for
working with PTV data and algorithms. It serves as an adapter layer
to the pyptv-gui submodule.
"""

import os
import sys

# Add the pyptv-gui directory to the Python path
pyptv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pyptv-gui'))
if pyptv_path not in sys.path:
    sys.path.insert(0, pyptv_path)

# Import components from pyptv-gui
try:
    # Import the trajectory viewer we've already created
    from .trajectory_viewer import TrajectoryViewer

    # Try to import components from pyptv-gui
    try:
        from pyptv.pyptv_gui import PYPTV_GUI
        from pyptv.gui_options import Experiment
        from pyptv.ptv import PTV
        from pyptv.calibration_gui import CalibrationGUI
        from pyptv.directory_editor import DirectoryEditor

        # Set a flag to indicate that the pyptv GUI components are available
        pyptv_available = True
    except ImportError as e:
        import warnings
        warnings.warn(f"Could not import pyptv GUI components: {e}. Some GUI functionality will be limited.")
        pyptv_available = False

    # Set a flag to indicate that basic GUI components are available
    gui_available = True
except ImportError as e:
    import warnings
    warnings.warn(f"Could not import basic GUI components: {e}. GUI functionality will not be available.")
    gui_available = False
    pyptv_available = False

# Define functions to check if GUI is available and to launch the GUI
def is_gui_available():
    """Check if the GUI components are available."""
    return gui_available

def is_pyptv_available():
    """Check if the pyptv GUI components are available."""
    return pyptv_available

def launch_gui():
    """Launch the main GUI application."""
    if not pyptv_available:
        raise ImportError("PyPTV GUI components are not available. Make sure pyptv-gui is properly installed.")

    # Import and run the main GUI
    gui = PYPTV_GUI()
    gui.configure_traits()

    return gui
