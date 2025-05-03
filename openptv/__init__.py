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

# Import constants from the standalone module
from openptv.constants import (
    TR_BUFSPACE, TR_MAX_CAMS, MAX_TARGETS,
    CORRES_NONE, PT_UNUSED,
    NPAR, COORD_UNUSED
)

# Initialize flags for available implementations
_using_cython = False
_gui_available = False
_gui_import_error = None

# Try to import the Cython bindings
try:
    # Import core tracking functions
    from openptv.binding.vec_utils import py_vec_cmp as vec_cmp
    from openptv.binding.vec_utils import py_vec_copy as vec_copy
    
    _using_cython = True

except ImportError as e:
    # Fall back to pure Python implementation
    warnings.warn(
        f"Cython bindings not available ({e}), using pure Python implementation. "
        "This may be significantly slower for large datasets."
    )

    from openptv.pyoptv.vec_utils import vec_cmp as vec_cmp, vec_copy as vec_copy

    _using_cython = False

def using_cython():
    """Return True if using Cython bindings, False if using pure Python."""
    return _using_cython

# High-level API that automatically selects the appropriate implementation
# Calibration
if _using_cython:
    try:
        from openptv.binding.calibration import Calibration
    except ImportError:
        from openptv.pyoptv.calibration import Calibration
else:
    from openptv.pyoptv.calibration import Calibration

# Parameters
if _using_cython:
    try:
        from openptv.binding.parameters import (
            ControlParams, VolumeParams, TrackingParams, SequenceParams, TargetParams
        )
    except ImportError:
        from openptv.pyoptv.parameters import (
            ControlPar as ControlParams, 
            VolumePar as VolumeParams, 
            TrackPar as TrackingParams, 
            SequencePar as SequenceParams, 
            TargetPar as TargetParams,
        )
else:
    from openptv.pyoptv.parameters import (
        ControlPar as ControlParams, 
        VolumePar as VolumeParams, 
        TrackPar as TrackingParams, 
        SequencePar as SequenceParams, 
        TargetPar as TargetParams,
    )

# exists only in Python 
from openptv.pyoptv.parameters import ExaminePar as ExamineParams

# Import GUI components if available
try:
    from openptv.gui import pyptv_gui
    _gui_available = True
except ImportError as e:
    _gui_available = False
    _gui_import_error = str(e)

def is_gui_available():
    """Return True if GUI components are available, False otherwise."""
    return _gui_available

def run_gui():
    """Run the OpenPTV GUI application."""
    if not _gui_available:
        raise ImportError(
            f"GUI components are not available: {_gui_import_error}. "
            "Make sure the required dependencies are installed: "
            "pip install openptv-python[gui]"
        )

    try:
        from openptv.gui.pyptv_gui import PYPTV_GUI
        gui = PYPTV_GUI()
        gui.configure_traits()
        return gui
    except Exception as e:
        import traceback
        print(f"Error starting GUI: {e}")
        traceback.print_exc()
        raise

# Tracking and frame buffer
if _using_cython:
    try:
        from openptv.binding.tracking_framebuf import TargetArray, Target, Frame
    except ImportError:
        from openptv.pyoptv.tracking_frame_buf import TargetArray, Target, Frame
else:
    from openptv.pyoptv.tracking_frame_buf import TargetArray, Target, Frame

# Correspondences
if _using_cython:
    try:
        from openptv.binding.correspondences import correspondences, MatchedCoords
    except ImportError:
        from openptv.pyoptv.correspondences import correspondences, MatchedCoords
else:
    from openptv.pyoptv.correspondences import correspondences, MatchedCoords

# Image processing
if _using_cython:
    try:
        from openptv.binding.image_processing import preprocess_image
    except ImportError:
        from openptv.pyoptv.image_processing import prepare_image as preprocess_image
else:
    from openptv.pyoptv.image_processing import prepare_image as preprocess_image

# Segmentation
if _using_cython:
    try:
        from openptv.binding.segmentation import target_recognition
    except ImportError:
        from openptv.pyoptv.segmentation import target_recognition
else:
    from openptv.pyoptv.segmentation import target_recognition

# Orientation
if _using_cython:
    try:
        from openptv.binding.orientation import (
            point_positions, external_calibration, full_calibration
        )
    except ImportError:
        from openptv.pyoptv.orientation import (
            point_positions, external_calibration, full_calibration
        )
else:
    from openptv.pyoptv.orientation import (
        point_positions, external_calibration, full_calibration
    )

# Tracker
if _using_cython:
    try:
        from openptv.binding.tracker import Tracker, default_naming
    except ImportError:
        from openptv.pyoptv.tracker import Tracker, default_naming
else:
    from openptv.pyoptv.tracker import Tracker, default_naming

# Import constants from binding modules
if _using_cython:
    try:
        # Import constants from tracking_framebuf
        from openptv.binding.tracking_framebuf import (
            CORRES_NONE, PT_UNUSED
        )
        
        # Import constants from orientation
        from openptv.binding.orientation import (
            NPAR, COORD_UNUSED
        )
        
        # Import constants from tracker
        from openptv.binding.tracker import (
            TR_BUFSPACE, MAX_TARGETS, TR_MAX_CAMS
        )
        
    except ImportError as e:
        # Fall back to constants from pyoptv
        from openptv.pyoptv.constants import (
            CORRES_NONE, PT_UNUSED, NPAR, COORD_UNUSED,
            TR_BUFSPACE, MAX_TARGETS, TR_MAX_CAMS
        )
else:
    # Use constants from pyoptv
    from openptv.pyoptv.constants import (
        CORRES_NONE, PT_UNUSED, NPAR, COORD_UNUSED,
        TR_BUFSPACE, MAX_TARGETS, TR_MAX_CAMS
    )




