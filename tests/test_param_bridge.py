"""
Tests for the parameter bridge functions.

This module tests the bridge functions in openptv.binding.param_bridge that convert
between Python parameter objects and C structs.
"""

import pytest
import numpy as np
from pathlib import Path

# Import parameter classes
from openptv.parameters import (
    TrackingParams, SequenceParams, VolumeParams, ControlParams, TargetParams
)

# Import bridge functions
from openptv.binding.param_bridge import (
    tracking_params_to_c_capsule, tracking_params_from_c,
    sequence_params_to_c_capsule, sequence_params_from_c,
    volume_params_to_c_capsule, volume_params_from_c,
    control_params_to_c_capsule, control_params_from_c,
    target_params_to_c_capsule, target_params_from_c
)


class TestTrackingParamsBridge:
    """Tests for the tracking parameters bridge functions."""

    def test_tracking_params_to_c(self):
        """Test conversion from Python TrackingParams to C track_par struct."""
        # Create a TrackingParams object
        params = TrackingParams(
            dvxmin=-10.0,
            dvxmax=10.0,
            dvymin=-10.0,
            dvymax=10.0,
            dvzmin=-10.0,
            dvzmax=10.0,
            dangle=0.5,
            dacc=0.5,
            flagNewParticles=True
        )

        # Convert to C struct
        c_params = tracking_params_to_c_capsule(params)

        # Convert back to Python object
        params2 = tracking_params_from_c(c_params)

        # Check that the values are preserved
        assert params2.dvxmin == params.dvxmin
        assert params2.dvxmax == params.dvxmax
        assert params2.dvymin == params.dvymin
        assert params2.dvymax == params.dvymax
        assert params2.dvzmin == params.dvzmin
        assert params2.dvzmax == params.dvzmax
        assert params2.dangle == params.dangle
        assert params2.dacc == params.dacc
        assert params2.flagNewParticles == params.flagNewParticles


class TestSequenceParamsBridge:
    """Tests for the sequence parameters bridge functions."""

    def test_sequence_params_to_c(self):
        """Test conversion from Python SequenceParams to C sequence_par struct."""
        # Create a SequenceParams object
        params = SequenceParams(
            n_img=2,
            base_name=["img1", "img2"],
            first=0,
            last=10
        )

        # Convert to C struct
        c_params = sequence_params_to_c_capsule(params)

        # Convert back to Python object
        params2 = sequence_params_from_c(c_params)

        # Check that the values are preserved
        assert params2.first == params.first
        assert params2.last == params.last
        assert len(params2.img_base_name) == len(params.img_base_name)
        for i in range(len(params.img_base_name)):
            assert params2.img_base_name[i] == params.img_base_name[i]


class TestVolumeParamsBridge:
    """Tests for the volume parameters bridge functions."""

    def test_volume_params_to_c(self):
        """Test conversion from Python VolumeParams to C volume_par struct."""
        # Create a VolumeParams object
        params = VolumeParams(
            X_lay=[0.0, 100.0],
            Zmin_lay=[0.0, 0.0],
            Zmax_lay=[100.0, 100.0],
            cnx=1.0,
            cny=1.0,
            cn=1.0,
            csumg=1.0,
            corrmin=0.5,
            eps0=0.1
        )

        # Convert to C struct
        c_params = volume_params_to_c_capsule(params)

        # Convert back to Python object
        params2 = volume_params_from_c(c_params)

        # Check that the values are preserved
        np.testing.assert_array_almost_equal(params2.X_lay, params.X_lay)
        np.testing.assert_array_almost_equal(params2.Zmin_lay, params.Zmin_lay)
        np.testing.assert_array_almost_equal(params2.Zmax_lay, params.Zmax_lay)
        assert params2.cnx == params.cnx
        assert params2.cny == params.cny
        assert params2.cn == params.cn
        assert params2.csumg == params.csumg
        assert params2.corrmin == params.corrmin
        assert params2.eps0 == params.eps0


class TestControlParamsBridge:
    """Tests for the control parameters bridge functions."""

    def test_control_params_to_c(self):
        """Test conversion from Python ControlParams to C control_par struct."""
        # Create a ControlParams object
        params = ControlParams(
            n_img=2,
            img_name=["img1.%d", "img2.%d"],
            img_cal=["cal1.tif", "cal2.tif"],
            hp_flag=True,
            allcam_flag=True,
            tiff_flag=True,
            imx=1280,
            imy=1024,
            pix_x=0.01,
            pix_y=0.01,
            chfield=0,
            mmp_n1=1.0,
            mmp_n2=1.33,
            mmp_n3=1.46,
            mmp_d=5.0
        )

        # Convert to C struct
        c_params = control_params_to_c_capsule(params)

        # Convert back to Python object
        params2 = control_params_from_c(c_params)

        # Check that the values are preserved
        assert params2.n_img == params.n_img
        assert params2.hp_flag == params.hp_flag
        assert params2.allcam_flag == params.allcam_flag
        assert params2.tiff_flag == params.tiff_flag
        assert params2.imx == params.imx
        assert params2.imy == params.imy
        assert params2.pix_x == params.pix_x
        assert params2.pix_y == params.pix_y
        assert params2.chfield == params.chfield
        assert params2.mmp_n1 == params.mmp_n1
        assert params2.mmp_n2 == params.mmp_n2
        assert params2.mmp_n3 == params.mmp_n3
        assert params2.mmp_d == params.mmp_d
        for i in range(params.n_img):
            assert params2.img_name[i] == params.img_name[i]
            assert params2.img_cal[i] == params.img_cal[i]


class TestTargetParamsBridge:
    """Tests for the target parameters bridge functions."""

    def test_target_params_to_c(self):
        """Test conversion from Python TargetParams to C target_par struct."""
        # Create a TargetParams object
        params = TargetParams(
            gvthres=[20, 15, 15, 20],
            discont=5,
            nnmin=3,
            nnmax=100,
            nxmin=1,
            nxmax=20,
            nymin=1,
            nymax=20,
            sumg_min=3,
            cr_sz=13
        )

        # Convert to C struct
        c_params = target_params_to_c_capsule(params)

        # Convert back to Python object
        params2 = target_params_from_c(c_params)

        # Check that the values are preserved
        np.testing.assert_array_equal(params2.gvthres, params.gvthres)
        assert params2.discont == params.discont
        assert params2.nnmin == params.nnmin
        assert params2.nnmax == params.nnmax
        assert params2.nxmin == params.nxmin
        assert params2.nxmax == params.nxmax
        assert params2.nymin == params.nymin
        assert params2.nymax == params.nymax
        assert params2.sumg_min == params.sumg_min
        assert params2.cr_sz == params.cr_sz


if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys

    print("\n=== Running Parameter Bridge Tests ===\n")

    # Run the tests with verbose output
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All parameter bridge tests passed successfully!")
    else:
        print("\n❌ Some parameter bridge tests failed. See details above.")

    sys.exit(result)
