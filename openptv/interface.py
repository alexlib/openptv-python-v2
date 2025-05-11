"""
Abstract interface defining the API for OpenPTV functionality,
allowing transparent switching between C and Python implementations.
"""
from abc import ABC, abstractmethod
import numpy as np

class CalibrationInterface(ABC):
    """Interface for camera calibration functionality"""
    
    @abstractmethod
    def read_calibration(self, file_path):
        """Read calibration parameters from file"""
        pass
    
    @abstractmethod
    def write_calibration(self, cal_obj, file_path):
        """Write calibration parameters to file"""
        pass
    
    @abstractmethod
    def calibration_ori(self, cal_obj, known_points, image_points, cpar):
        """Initial orientation for one camera"""
        pass
    
    @abstractmethod
    def full_calibration(self, cal_obj, known_points, image_points, cpar, flags):
        """Perform full calibration with optimization"""
        pass

    @abstractmethod
    def external_calibration(self, cal_obj, known_points, image_points, cpar, flags):
        """Optimize only external parameters"""
        pass
    
    @abstractmethod
    def point_position(self, point_2d, cal_obj, flags):
        """Calculate 3D ray from 2D point based on calibration"""
        pass
    
    @abstractmethod
    def image_coordinates(self, point_3d, cal_obj, flags):
        """Project 3D point to camera's image plane using calibration"""
        pass
    
    @abstractmethod
    def distort_point_positions(self, pos, ap, flags):
        """Apply distortion to image positions"""
        pass
    
    @abstractmethod
    def remove_distortion(self, pos, cal_obj, flags):
        """Remove distortion from image positions"""
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


class PTV_Interface(CalibrationInterface, DetectionInterface, CorrespondenceInterface, TrackingInterface):
    """Combined interface providing all OpenPTV functionality"""
    
    @property
    @abstractmethod
    def implementation_name(self):
        """Returns the name of the implementation (C or Python)"""
        pass
