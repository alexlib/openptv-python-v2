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
import importlib

__version__ = '0.1.0'

# Import constants from the standalone module
from openptv.constants import (
    TR_BUFSPACE, TR_MAX_CAMS, MAX_TARGETS,
    CORRES_NONE, PT_UNUSED,
    NPAR, COORD_UNUSED
)

# Initialize flags for available implementations
_using_cython = False
_gui_available = True
_gui_import_error = None

# Try to import the Cython bindings
try:
    # Import core tracking functions from tracking_framebuf as a test for Cython availability
    from openptv.binding.tracking_framebuf import TargetArray, Target
    _using_cython = True
except ImportError as e:
    # Fall back to pure Python implementation
    warnings.warn(
        f"Cython bindings not available ({e}), using pure Python implementation. "
        "This may be significantly slower for large datasets."
    )
    _using_cython = False

def using_cython():
    """Return True if using Cython bindings, False if using pure Python."""
    return _using_cython

# Directly expose binding modules at the top level
# This makes imports like "from openptv import calibration" work
# instead of requiring "from openptv.binding import calibration"

# List of binding modules to expose
_binding_modules = [
    'calibration',
    'parameters',
    'tracking_framebuf',
    'correspondences',
    'image_processing',
    'segmentation',
    'orientation',
    'tracker',
    'epipolar',
    'transforms'
]

# Import and expose each module
for _module_name in _binding_modules:
    try:
        # Try to import from binding
        _module = importlib.import_module(f'openptv.binding.{_module_name}')
        # Set the module in the openptv namespace
        globals()[_module_name] = _module
    except ImportError:
        # If binding import fails, try to import from backup_pyoptv
        try:
            # Convert module name if needed (e.g., epipolar -> epi)
            _backup_name = _module_name
            if _module_name == 'epipolar':
                _backup_name = 'epi'
            elif _module_name == 'tracking_framebuf':
                _backup_name = 'tracking_frame_buf'

            _module = importlib.import_module(f'openptv.backup_pyoptv.{_backup_name}')
            globals()[_module_name] = _module
        except ImportError:
            # If both imports fail, set to None
            globals()[_module_name] = None
            warnings.warn(f"Could not import module {_module_name} from either binding or backup_pyoptv")

# Clean up temporary variables
del _module_name, _binding_modules, _module
if '_backup_name' in locals():
    del _backup_name

# High-level API that automatically selects the appropriate implementation
# Calibration
if _using_cython:
    try:
        from openptv.binding.calibration import Calibration
    except ImportError:
        from openptv.backup_pyoptv.calibration import Calibration
else:
    from openptv.backup_pyoptv.calibration import Calibration

# Parameters
# Explicitly import and rename to avoid confusion
try:
    # Import Cython binding parameters with explicit names
    from openptv.binding.parameters import (
        MultimediaParams as CythonMultimediaParams,
        TrackingParams as CythonTrackingParams,
        SequenceParams as CythonSequenceParams,
        VolumeParams as CythonVolumeParams,
        ControlParams as CythonControlParams,
        TargetParams as CythonTargetParams
    )

    # Set default parameter classes to Cython versions
    MultimediaParams = CythonMultimediaParams
    TrackingParams = CythonTrackingParams
    SequenceParams = CythonSequenceParams
    VolumeParams = CythonVolumeParams
    ControlParams = CythonControlParams
    TargetParams = CythonTargetParams

except ImportError:
    # Import Python implementations with explicit names
    from openptv.backup_pyoptv.parameters import (
        MultimediaPar as PythonMultimediaParams,
        TrackPar as PythonTrackingParams,
        SequencePar as PythonSequenceParams,
        VolumePar as PythonVolumeParams,
        ControlPar as PythonControlParams,
        TargetPar as PythonTargetParams
    )

    # Set default parameter classes to Python versions
    MultimediaParams = PythonMultimediaParams
    TrackingParams = PythonTrackingParams
    SequenceParams = PythonSequenceParams
    VolumeParams = PythonVolumeParams
    ControlParams = PythonControlParams
    TargetParams = PythonTargetParams

# Import Python-only parameters that don't have Cython equivalents
from openptv.backup_pyoptv.parameters import ExaminePar as ExamineParams

# # No GUI parameters imported here

# # Import GUI components if available
# try:
#     from openptv.gui import pyptv_gui
#     _gui_available = True
# except ImportError as e:
#     _gui_available = False
#     _gui_import_error = str(e)

# def is_gui_available():
#     """Return True if GUI components are available, False otherwise."""
#     return _gui_available

# def run_gui():
#     """Run the OpenPTV GUI application."""
#     if not _gui_available:
#         raise ImportError(
#             f"GUI components are not available: {_gui_import_error}. "
#             "Make sure the required dependencies are installed: "
#             "pip install openptv-python[gui]"
#         )

#     try:
#         from openptv.gui.pyptv_gui import PYPTV_GUI
#         gui = PYPTV_GUI()
#         gui.configure_traits()
#         return gui
#     except Exception as e:
#         import traceback
#         print(f"Error starting GUI: {e}")
#         traceback.print_exc()
#         raise

# Tracking and frame buffer
if _using_cython:
    try:
        from openptv.binding.tracking_framebuf import TargetArray, Target, Frame
    except ImportError:
        from openptv.backup_pyoptv.tracking_frame_buf import TargetArray, Target, Frame
else:
    from openptv.backup_pyoptv.tracking_frame_buf import TargetArray, Target, Frame

# Correspondences
if _using_cython:
    try:
        from openptv.binding.correspondences import correspondences, MatchedCoords
    except ImportError:
        from openptv.backup_pyoptv.correspondences import correspondences, MatchedCoords
else:
    from openptv.backup_pyoptv.correspondences import correspondences, MatchedCoords

# Image processing
if _using_cython:
    try:
        from openptv.binding.image_processing import preprocess_image
    except ImportError:
        from openptv.backup_pyoptv.image_processing import prepare_image as preprocess_image
else:
    from openptv.backup_pyoptv.image_processing import prepare_image as preprocess_image

# Segmentation
if _using_cython:
    try:
        from openptv.binding.segmentation import target_recognition
    except ImportError:
        from openptv.backup_pyoptv.segmentation import target_recognition
else:
    from openptv.backup_pyoptv.segmentation import target_recognition

# Orientation
if _using_cython:
    try:
        from openptv.binding.orientation import (
            point_positions, external_calibration, full_calibration
        )
    except ImportError:
        from openptv.backup_pyoptv.orientation import (
            point_positions, external_calibration, full_calibration
        )
else:
    from openptv.backup_pyoptv.orientation import (
        point_positions, external_calibration, full_calibration
    )

# Tracker
if _using_cython:
    try:
        from openptv.binding.tracker import Tracker, default_naming
    except ImportError:
        from openptv.backup_pyoptv.tracker import Tracker, default_naming
else:
    from openptv.backup_pyoptv.tracker import Tracker, default_naming

# Epipolar geometry
if _using_cython:
    try:
        from openptv.binding.epipolar import epipolar_curve
    except ImportError:
        from openptv.backup_pyoptv.epi import epipolar_curve
else:
    from openptv.backup_pyoptv.epi import epipolar_curve

# Vector utilities
if _using_cython:
    try:
        from openptv.binding.vec_utils import py_vec_copy, py_vec_cmp
    except ImportError:
        from openptv.backup_pyoptv.vec_utils import vec_copy as py_vec_copy, vec_cmp as py_vec_cmp
else:
    from openptv.backup_pyoptv.vec_utils import vec_copy as py_vec_copy, vec_cmp as py_vec_cmp

# # Import constants from binding modules
# if _using_cython:
#     try:
#         # Import constants from tracking_framebuf
#         from openptv.binding.tracking_framebuf import (
#             CORRES_NONE, PT_UNUSED
#         )

#         # Import constants from orientation
#         from openptv.binding.orientation import (
#             NPAR, COORD_UNUSED
#         )

#         # Import constants from tracker
#         from openptv.binding.tracker import (
#             TR_BUFSPACE, MAX_TARGETS, TR_MAX_CAMS
#         )

#     except ImportError as e:
#         # Fall back to constants from pyoptv
#         from openptv.backup_pyoptv.constants import (
#             CORRES_NONE, PT_UNUSED, NPAR, COORD_UNUSED,
#             TR_BUFSPACE, MAX_TARGETS, TR_MAX_CAMS
#         )
# else:
#     # Use constants from pyoptv
#     from openptv.backup_pyoptv.constants import (
#         CORRES_NONE, PT_UNUSED, NPAR, COORD_UNUSED,
#         TR_BUFSPACE, MAX_TARGETS, TR_MAX_CAMS
#     )




