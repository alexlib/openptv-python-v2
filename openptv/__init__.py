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
    # First check if the binding directory exists and has .pyd files
    binding_dir = os.path.join(os.path.dirname(__file__), 'binding')
    if os.path.exists(binding_dir) and any(f.endswith('.pyd') for f in os.listdir(binding_dir)):
        # Try to import from the binding directory
        import importlib.util

        # Find the appropriate .pyd file for tracking_framebuf
        pyd_files = [f for f in os.listdir(binding_dir) if f.startswith('tracking_framebuf') and f.endswith('.pyd')]
        if pyd_files:
            # Use the first matching .pyd file
            pyd_file = os.path.join(binding_dir, pyd_files[0])

            # Load the module from the .pyd file
            spec = importlib.util.spec_from_file_location("openptv.binding.tracking_framebuf", pyd_file)
            tracking_framebuf = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tracking_framebuf)

            # Get the TargetArray and Target classes from the module
            TargetArray = tracking_framebuf.TargetArray
            Target = tracking_framebuf.Target

            _using_cython = True
        else:
            raise ImportError("No tracking_framebuf.pyd file found in binding directory")
    else:
        raise ImportError("No binding directory or no .pyd files found")

except ImportError as e:
    # Fall back to pure Python implementation
    warnings.warn(
        f"Cython bindings not available ({e}), using pure Python implementation. "
        "This may be significantly slower for large datasets."
    )

    from openptv.pyoptv.tracking_frame_buf import TargetArray, Target

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
    _using_cython = True

    # Set default parameter classes to Cython versions
    MultimediaParams = CythonMultimediaParams
    TrackingParams = CythonTrackingParams
    SequenceParams = CythonSequenceParams
    VolumeParams = CythonVolumeParams
    ControlParams = CythonControlParams
    TargetParams = CythonTargetParams

except ImportError:
    # Import Python implementations with explicit names
    from openptv.pyoptv.parameters import (
        MultimediaPar as PythonMultimediaParams,
        TrackPar as PythonTrackingParams,
        SequencePar as PythonSequenceParams,
        VolumePar as PythonVolumeParams,
        ControlPar as PythonControlParams,
        TargetPar as PythonTargetParams
    )
    _using_cython = False

    # Set default parameter classes to Python versions
    MultimediaParams = PythonMultimediaParams
    TrackingParams = PythonTrackingParams
    SequenceParams = PythonSequenceParams
    VolumeParams = PythonVolumeParams
    ControlParams = PythonControlParams
    TargetParams = PythonTargetParams

# Import Python-only parameters that don't have Cython equivalents
from openptv.pyoptv.parameters import ExaminePar as ExamineParams

# No GUI parameters imported here

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

# Epipolar geometry
if _using_cython:
    try:
        from openptv.binding.epipolar import epipolar_curve
    except ImportError:
        from openptv.pyoptv.epi import epipolar_curve
else:
    from openptv.pyoptv.epi import epipolar_curve

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




