"""
OpenPTV Python package for Particle Tracking Velocimetry.

This package provides tools for PTV analysis with a flexible architecture:
- High-performance C implementation (liboptv)
- Cython bindings for Python access to C functions
"""

import importlib
import warnings
import sys

__version__ = '0.1.0'

# Import constants from the standalone module
from openptv.constants import (
    TR_BUFSPACE, TR_MAX_CAMS, MAX_TARGETS,
    CORRES_NONE, PT_UNUSED,
    NPAR, COORD_UNUSED
)

# Initialize flag for Cython availability
_using_cython = False

# Try to import the Cython bindings
try:
    # Import core tracking functions from tracking_framebuf as a test for Cython availability
    from openptv.binding.tracking_framebuf import TargetArray, Target
    _using_cython = True
except ImportError as e:
    # Cython bindings are required
    raise ImportError(
        f"Cython bindings not available ({e}). "
        "Please build the Cython extensions with 'python setup.py build_ext --inplace'"
    ) from e

def using_cython():
    """Return True if using Cython bindings, False if using pure Python."""
    return _using_cython

# List of binding modules to expose at the top level
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
    'transforms',
    'vec_utils'
]

# Import and expose each module at the top level
for _module_name in _binding_modules:
    try:
        _module = importlib.import_module(f'openptv.binding.{_module_name}')
        globals()[_module_name] = _module
    except ImportError as e:
        warnings.warn(f"Could not import module {_module_name}: {e}")

# Clean up temporary variables
if '_module_name' in locals():
    del _module_name
if '_binding_modules' in locals():
    del _binding_modules
if '_module' in locals():
    del _module

# Direct imports of commonly used classes and functions
try:
    from openptv.binding.calibration import Calibration
    from openptv.binding.tracking_framebuf import TargetArray, Target, Frame
    from openptv.binding.correspondences import correspondences, MatchedCoords
    from openptv.binding.image_processing import preprocess_image
    from openptv.binding.segmentation import target_recognition
    from openptv.binding.orientation import point_positions, external_calibration, full_calibration
    from openptv.binding.tracker import Tracker, default_naming
    from openptv.binding.epipolar import epipolar_curve
    from openptv.binding.vec_utils import py_vec_copy, py_vec_cmp
except ImportError as e:
    # If any of the direct imports fail, log a warning but don't crash
    warnings.warn(f"Some Cython bindings could not be imported: {e}")

from .parameters.control import ControlParams
from .parameters.volume import VolumeParams
from .parameters.tracking import TrackingParams
from .parameters.sequence import SequenceParams
from .parameters.target import TargetParams
from .parameters.examine import ExamineParams
from .parameters.criteria import CriteriaParams
from .parameters.detect_plate import DetectPlateParams
from .parameters.dumbbell import DumbbellParams
from .parameters.man_ori import ManOriParams
from .parameters.multi_plane import MultiPlaneParams
from .parameters.pft_version import PftVersionParams
from .parameters.control import PtvParams
from .parameters.shaking import ShakingParams
from .parameters.target import TargRecParams

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




