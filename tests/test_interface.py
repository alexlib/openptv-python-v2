"""
Tests for the unified interface functionality.
"""
import pytest
from unittest.mock import patch
import numpy as np  # Import numpy
from openptv.factory import get_ptv_implementation
from openptv.interface import PTV_Interface

# Define dtypes for mocking, similar to openptv/pyoptv/calibration.py
exterior_dtype_mock = np.dtype([
    ('x0', np.float64), ('y0', np.float64), ('z0', np.float64),
    ('omega', np.float64), ('phi', np.float64), ('kappa', np.float64),
    ('dm', np.float64, (3, 3))
])

interior_dtype_mock = np.dtype([
    ('xh', np.float64), ('yh', np.float64), ('cc', np.float64)
])

mmlut_dtype_mock = np.dtype([
    ('origin', np.float64, 3), ('nr', np.int32), ('nz', np.int32), ('rw', np.int32)
])

@pytest.mark.parametrize("prefer_c", [True, False])
def test_calibration_methods(prefer_c):
    """Test calibration methods for both C and Python implementations."""
    ptv = get_ptv_implementation(prefer_c=prefer_c)
    assert isinstance(ptv, PTV_Interface), "Implementation does not conform to PTV_Interface"

    # Mock inputs
    file_path = "mock_calibration_file.cal"
    
    # Create a mock calibration object with numpy structured arrays
    class MockCalibration:
        def __init__(self):
            self.ext_par = np.array((0., 0., 0., 0., 0., 0., np.eye(3)), dtype=exterior_dtype_mock).view(np.recarray)
            self.int_par = np.array((0., 0., 0.), dtype=interior_dtype_mock).view(np.recarray)
            self.glass_par = np.array([0., 0., 1.], dtype=np.float64)
            self.added_par = np.array([0., 0., 0., 0., 0., 1., 0.], dtype=np.float64)
            self.mmlut = np.array((np.zeros(3), 0, 0, 0), dtype=mmlut_dtype_mock).view(np.recarray)
            # Ensure mmlut_data has dimensions based on mmlut.nr and mmlut.nz
            # If nr or nz are 0 by default, this will be an empty array with correct shape.
            self.mmlut_data = np.zeros((self.mmlut.nr, self.mmlut.nz), dtype=np.float64)


    cal_obj = MockCalibration()
    known_points = [(0, 0, 0), (1, 1, 1)]
    image_points = [(100, 100), (200, 200)]
    cpar = "mock_camera_parameters"
    flags = "mock_flags"

    # Mock the from_file method to bypass file existence check
    with patch("openptv.pyoptv.calibration.Calibration.from_file", return_value=cal_obj):
        # Test read_calibration and write_calibration
        try:
            ptv.read_calibration(file_path)
            ptv.write_calibration(cal_obj, file_path)
        except NotImplementedError:
            pytest.fail("read_calibration or write_calibration not implemented")

        # Test calibration_ori
        try:
            ptv.calibration_ori(cal_obj, known_points, image_points, cpar)
        except NotImplementedError:
            pytest.fail("calibration_ori not implemented")

        # Test full_calibration
        try:
            ptv.full_calibration(cal_obj, known_points, image_points, cpar, flags)
        except NotImplementedError:
            pytest.fail("full_calibration not implemented")

        # Test external_calibration
        try:
            ptv.external_calibration(cal_obj, known_points, image_points, cpar, flags)
        except NotImplementedError:
            pytest.fail("external_calibration not implemented")

        # Test point_position
        try:
            ptv.point_position((100, 100), cal_obj, flags)
        except NotImplementedError:
            pytest.fail("point_position not implemented")

        # Test image_coordinates
        try:
            ptv.image_coordinates((1, 1, 1), cal_obj, flags)
        except NotImplementedError:
            pytest.fail("image_coordinates not implemented")

        # Test distort_point_positions
        try:
            ptv.distort_point_positions([(100, 100)], "mock_ap", flags)
        except NotImplementedError:
            pytest.fail("distort_point_positions not implemented")

        # Test remove_distortion
        try:
            ptv.remove_distortion([(100, 100)], cal_obj, flags)
        except NotImplementedError:
            pytest.fail("remove_distortion not implemented")

        print(f"All calibration methods passed for {'C' if prefer_c else 'Python'} implementation.")
