"""
Wrapper for the C implementation of OpenPTV functionality.
"""
import numpy as np
from openptv.interface import PTV_Interface
from pathlib import Path

# Import C bindings
try:
    from openptv.coptv import (
        calibration as c_cal,
        tracking as c_track,
        correspondences as c_corresp,
        image_processing as c_imgproc
    )
except ImportError:
    raise ImportError("C bindings for OpenPTV not available")

class CPTVImplementation(PTV_Interface):
    """Implementation of the PTV interface using C library bindings"""
    
    @property
    def implementation_name(self):
        return "C Implementation"
    
    # Calibration methods
    def read_calibration(self, ori_file, addpar_file=None):
        ori_file = Path(ori_file)
        addpar_file = Path(addpar_file) if addpar_file else None
        return c_cal.read_calibration(ori_file, addpar_file)
    
    def write_calibration(self, cal_obj, ori_file, add_file=None):
        return c_cal.write_calibration(cal_obj, ori_file, add_file)
    
    def calibration_ori(self, cal_obj, known_points, image_points, cpar):
        return c_cal.calibration_ori(cal_obj, known_points, image_points, cpar)
    
    def full_calibration(self, cal_obj, known_points, image_points, cpar, flags):
        return c_cal.full_calibration(cal_obj, known_points, image_points, cpar, flags)
    
    def external_calibration(self, cal_obj, known_points, image_points, cpar, flags):
        return c_cal.external_calibration(cal_obj, known_points, image_points, cpar, flags)
    
    def point_position(self, point_2d, cal_obj, flags):
        return c_cal.point_position(point_2d, cal_obj, flags)
    
    def image_coordinates(self, point_3d, cal_obj, flags):
        return c_cal.image_coordinates(point_3d, cal_obj, flags)
    
    def distort_point_positions(self, pos, ap, flags):
        return c_cal.distort_point_positions(pos, ap, flags)
    
    def remove_distortion(self, pos, cal_obj, flags):
        return c_cal.remove_distortion(pos, cal_obj, flags)
    
    # Detection methods
    def detect_particles(self, img, threshold, min_area, max_area, subpix_method):
        return c_imgproc.detect_particles(img, threshold, min_area, max_area, subpix_method)
    
    def target_recognition(self, img, tpar, cpar):
        return c_imgproc.target_recognition(img, tpar, cpar)
    
    def targ_rec(self, img, par):
        return c_imgproc.targ_rec(img, par)
    
    # Correspondence methods
    def match_points(self, targets_lists, cal_objects, match_params, flags):
        return c_corresp.match_points(targets_lists, cal_objects, match_params, flags)
    
    def point_position_correction(self, targets, cals, corrpar, flags):
        return c_corresp.point_position_correction(targets, cals, corrpar, flags)
    
    def epipolar_curve(self, cal1, cal2, point_2d, flags):
        return c_corresp.epipolar_curve(cal1, cal2, point_2d, flags)
    
    # Tracking methods
    def track_forwards(self, positions, tracking_params, flags):
        return c_track.track_forwards(positions, tracking_params, flags)
    
    def track_backwards(self, positions, tracking_params, flags):
        return c_track.track_backwards(positions, tracking_params, flags)
    
    def trackback_c(self, pos, track_par):
        return c_track.trackback_c(pos, track_par)
    
    def trackcorr_c(self, pos, track_par):
        return c_track.trackcorr_c(pos, track_par)
