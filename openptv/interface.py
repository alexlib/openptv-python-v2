"""
Abstract interface defining the API for OpenPTV functionality,
allowing transparent switching between C and Python implementations.
"""
from abc import ABC, abstractmethod
import numpy as np
# Forward references for type hints if parameter classes are in a different file
from typing import TYPE_CHECKING, List, Optional, Tuple

if TYPE_CHECKING:
    from openptv.parameters.parameter_dataclasses import (
        CalibrationParameters,
        TrackingParameters,
        VolumeParameters,
        DetectionParameters,
        AllParametersContainer
    )

class CalibrationInterface(ABC):
    """Interface for camera calibration functionality"""
    
    @abstractmethod
    def read_calibration(self, camera_index: int, ori_file_path: str, add_file_path: Optional[str] = None) -> 'CalibrationParameters':
        """Read calibration parameters from file for a specific camera and returns them."""
        pass
    
    @abstractmethod
    def write_calibration(self, camera_index: int, ori_file_path: str, add_file_path: Optional[str] = None) -> None:
        """Write calibration parameters to file for a specific camera."""
        pass
    
    @abstractmethod
    def calibration_ori(self, camera_index: int, known_points: np.ndarray, image_points: np.ndarray, cpar_py_dataclass) -> Tuple[np.ndarray, np.ndarray, np.ndarray]: # Define cpar_py_dataclass properly later
        """Initial orientation for one camera identified by camera_index."""
        pass
    
    @abstractmethod
    def full_calibration(self, camera_index: int, known_points: np.ndarray, image_points: np.ndarray, cpar_py_dataclass, flags) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Perform full calibration with optimization for one camera."""
        pass

    @abstractmethod
    def external_calibration(self, camera_index: int, known_points: np.ndarray, image_points: np.ndarray, cpar_py_dataclass, flags):
        """Optimize only external parameters for one camera."""
        pass
    
    @abstractmethod
    def point_position(self, camera_index: int, point_2d: np.ndarray, flags) -> np.ndarray: # Assuming returns 3D ray
        """Calculate 3D ray from 2D point based on calibration of a specific camera."""
        pass
    
    @abstractmethod
    def image_coordinates(self, camera_index: int, point_3d: np.ndarray, flags) -> np.ndarray: # Assuming returns 2D point
        """Project 3D point to camera's image plane using calibration of a specific camera."""
        pass
    
    @abstractmethod
    def distort_point_positions(self, camera_index: int, pos: np.ndarray, flags) -> np.ndarray: # 'ap' removed, use camera's added_par
        """Apply distortion to image positions using calibration of a specific camera."""
        pass
    
    @abstractmethod
    def remove_distortion(self, camera_index: int, pos: np.ndarray, flags) -> np.ndarray:
        """Remove distortion from image positions using calibration of a specific camera."""
        pass


class DetectionInterface(ABC):
    """Interface for particle detection functionality"""
    
    @abstractmethod
    def detect_particles(self, img, threshold, min_area, max_area, subpix_method):
        """Detect particles in an image"""
        pass
    
    @abstractmethod
    def target_recognition(self, img, tpar, cpar):
        """Detect and process targets in an image"""
        pass
    
    @abstractmethod
    def targ_rec(self, img, par):
        """Target recognition wrapper"""
        pass


class CorrespondenceInterface(ABC):
    """Interface for multi-camera correspondence matching"""
    
    @abstractmethod
    def match_points(self, targets_lists, cal_objects, match_params, flags):
        """Find corresponding points across camera views"""
        pass
    
    @abstractmethod
    def point_position_correction(self, targets, cals, corrpar, flags):
        """Correct 3D point positions"""
        pass
    
    @abstractmethod
    def epipolar_curve(self, cal1, cal2, point_2d, flags):
        """Calculate epipolar curve"""
        pass


class TrackingInterface(ABC):
    """Interface for particle tracking across frames"""
    
    @abstractmethod
    def track_forwards(self, positions, tracking_params, flags):
        """Track particles in forward direction"""
        pass
    
    @abstractmethod
    def track_backwards(self, positions, tracking_params, flags):
        """Track particles in backward direction"""
        pass
    
    @abstractmethod
    def trackback_c(self, pos, track_par):
        """Wrapper for backward tracking"""
        pass
    
    @abstractmethod
    def trackcorr_c(self, pos, track_par):
        """Track correspondence"""
        pass


class ParameterHandlingInterface(ABC):
    """Interface for managing and accessing PTV parameters."""

    @abstractmethod
    def get_calibration_parameters(self, camera_index: int) -> 'CalibrationParameters':
        """
        Returns the current calibration parameters for a specific camera.
        If no parameters are set for the camera_index, it might return default parameters or raise an error.
        """
        pass

    @abstractmethod
    def set_calibration_parameters(self, camera_index: int, params: 'CalibrationParameters') -> None:
        """Sets the calibration parameters for a specific camera."""
        pass

    @abstractmethod
    def get_num_cameras(self) -> int:
        """Returns the number of cameras for which calibration parameters are set."""
        pass

    @abstractmethod
    def add_camera(self, params: 'CalibrationParameters') -> int:
        """Adds a new camera with the given calibration parameters and returns its index."""
        pass
        
    @abstractmethod
    def remove_camera(self, camera_index: int) -> None:
        """Removes the camera at the given index."""
        pass

    @abstractmethod
    def get_tracking_parameters(self) -> 'TrackingParameters': # Assuming single set of tracking params for now
        """Loads or returns current tracking parameters."""
        pass

    @abstractmethod
    def set_tracking_parameters(self, params: 'TrackingParameters') -> None:
        """Sets the tracking parameters."""
        pass

    @abstractmethod
    def get_volume_parameters(self) -> 'VolumeParameters':
        """Loads or returns current volume parameters."""
        pass

    @abstractmethod
    def set_volume_parameters(self, params: 'VolumeParameters') -> None:
        """Sets the volume parameters."""
        pass
        
    @abstractmethod
    def get_detection_parameters(self, camera_index: int) -> 'DetectionParameters': # Detection params can be per camera
        """Loads or returns current detection parameters for a specific camera."""
        pass

    @abstractmethod
    def set_detection_parameters(self, camera_index: int, params: 'DetectionParameters') -> None:
        """Sets the detection parameters for a specific camera."""
        pass

    # Consider if a more generic load/save from a single project/config file is needed
    # For now, focusing on get/set for individual parameter sets.
    # @abstractmethod
    # def load_project_parameters(self, file_path: str) -> 'AllParametersContainer':
    #     pass

    # @abstractmethod
    # def save_project_parameters(self, params: 'AllParametersContainer', file_path: str) -> None:
    #     pass


class PTV_Interface(CalibrationInterface, DetectionInterface, CorrespondenceInterface, TrackingInterface, ParameterHandlingInterface):
    """Combined interface providing all OpenPTV functionality including parameter management"""
    
    @property
    @abstractmethod
    def implementation_name(self):
        """Returns the name of the implementation (C or Python)"""
        pass
