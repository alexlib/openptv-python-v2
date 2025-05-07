"""
Unified parameter handling for OpenPTV.

This module provides a single source of truth for parameter handling in OpenPTV.
It replaces the separate parameter handling in openptv.gui.parameters and
openptv.binding.parameters.
"""

# Import parameter classes to make them available at the module level
from openptv.parameters.base import Parameters
from openptv.parameters.tracking import TrackingParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.control import ControlParams, PtvParams
from openptv.parameters.target import TargetParams, TargRecParams
from openptv.parameters.calibration import CalOriParams
from openptv.parameters.criteria import CriteriaParams
from openptv.parameters.examine import ExamineParams
from openptv.parameters.orient import OrientParams
from openptv.parameters.detect_plate import DetectPlateParams
from openptv.parameters.dumbbell import DumbbellParams
from openptv.parameters.shaking import ShakingParams
from openptv.parameters.pft_version import PftVersionParams
from openptv.parameters.man_ori import ManOriParams

# Re-export utility functions
from openptv.parameters.utils import copy_params_dir, par_dir_prefix

# Export all parameter classes
__all__ = [
    'Parameters',
    'TrackingParams',
    'SequenceParams',
    'VolumeParams',
    'ControlParams',
    'PtvParams',
    'TargetParams',
    'TargRecParams',
    'CalOriParams',
    'CriteriaParams',
    'ExamineParams',
    'OrientParams',
    'DetectPlateParams',
    'DumbbellParams',
    'ShakingParams',
    'PftVersionParams',
    'ManOriParams',
    'copy_params_dir',
    'par_dir_prefix',
]
