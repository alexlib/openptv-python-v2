"""
Tests for the parameter bridge functions.

This module tests the bridge functions in openptv.binding.param_bridge.
"""

import os
import pytest
import tempfile
from pathlib import Path

import numpy as np

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.control import ControlParams
from openptv.parameters.target import TargetParams
from openptv.parameters.orient import OrientParams
from openptv.parameters.calibration import CalOriParams

# Import bridge functions
try:
    from openptv.binding.param_bridge import (
        tracking_params_to_c, tracking_params_from_c,
        sequence_params_to_c, sequence_params_from_c,
        volume_params_to_c, volume_params_from_c,
        control_params_to_c, control_params_from_c,
        target_params_to_c, target_params_from_c,
        orient_params_to_c, orient_params_from_c,
        cal_ori_params_to_c, cal_ori_params_from_c,
    )
    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Parameter bridge not available")
class TestTrackingParamsBridge:
    """Tests for the tracking parameters bridge functions."""

    def test_tracking_params_roundtrip(self):
        """Test conversion of TrackingParams to C struct and back."""
        # Create a parameter object
        params = TrackingParams(
            dvxmin=-10.0,
            dvxmax=10.0,
            dvymin=-10.0,
            dvymax=10.0,
            dvzmin=-10.0,
            dvzmax=10.0,
            angle=0.5,
            dacc=0.5,
            flagNewParticles=True,
        )

        # Convert to C struct
        c_params = tracking_params_to_c(params)

        # Convert back to Python object
        params2 = tracking_params_from_c(c_params)

        # Check that parameters match
        assert params2.dvxmin == params.dvxmin
        assert params2.dvxmax == params.dvxmax
        assert params2.dvymin == params.dvymin
        assert params2.dvymax == params.dvymax
        assert params2.dvzmin == params.dvzmin
        assert params2.dvzmax == params.dvzmax
        assert params2.angle == params.angle
        assert params2.dacc == params.dacc
        assert params2.flagNewParticles == params.flagNewParticles


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Parameter bridge not available")
class TestSequenceParamsBridge:
    """Tests for the sequence parameters bridge functions."""

    def test_sequence_params_roundtrip(self):
        """Test conversion of SequenceParams to C struct and back."""
        # Create a parameter object
        params = SequenceParams(
            n_img=4,
            base_name=['cam1', 'cam2', 'cam3', 'cam4'],
            first=1,
            last=100,
        )

        # Convert to C struct
        c_params = sequence_params_to_c(params)

        # Convert back to Python object
        params2 = sequence_params_from_c(c_params)

        # Check that parameters match
        assert params2.n_img == params.n_img
        assert params2.base_name == params.base_name
        assert params2.first == params.first
        assert params2.last == params.last


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Parameter bridge not available")
class TestVolumeParamsBridge:
    """Tests for the volume parameters bridge functions."""

    def test_volume_params_roundtrip(self):
        """Test conversion of VolumeParams to C struct and back."""
        # Create a parameter object
        params = VolumeParams(
            X_lay=[0.0, 10.0],
            Zmin_lay=[-5.0, -5.0],
            Zmax_lay=[5.0, 5.0],
            cnx=0.1,
            cny=0.1,
            cn=0.1,
            csumg=0.1,
            corrmin=0.5,
            eps0=0.1,
        )

        # Convert to C struct
        c_params = volume_params_to_c(params)

        # Convert back to Python object
        params2 = volume_params_from_c(c_params)

        # Check that parameters match
        assert params2.X_lay == params.X_lay
        assert params2.Zmin_lay == params.Zmin_lay
        assert params2.Zmax_lay == params.Zmax_lay
        assert params2.cnx == params.cnx
        assert params2.cny == params.cny
        assert params2.cn == params.cn
        assert params2.csumg == params.csumg
        assert params2.corrmin == params.corrmin
        assert params2.eps0 == params.eps0


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Parameter bridge not available")
class TestControlParamsBridge:
    """Tests for the control parameters bridge functions."""

    def test_control_params_roundtrip(self):
        """Test conversion of ControlParams to C struct and back."""
        # Create a parameter object
        params = ControlParams(
            n_img=4,
            img_base_name=['cam1', 'cam2', 'cam3', 'cam4'],
            cal_img_base_name=['cal1', 'cal2', 'cal3', 'cal4'],
            hp_flag=True,
            allcam_flag=True,
            tiff_flag=True,
            imx=1280,
            imy=1024,
            pix_x=0.01,
            pix_y=0.01,
            chfield=0,
            mm_np={
                'nlay': 1,
                'n1': 1.0,
                'n2': [1.33, 0.0, 0.0],
                'n3': 1.0,
                'd': [10.0, 0.0, 0.0],
            },
        )

        # Convert to C struct
        c_params = control_params_to_c(params)

        # Convert back to Python object
        params2 = control_params_from_c(c_params)

        # Check that parameters match
        assert params2.n_img == params.n_img
        assert params2.img_base_name == params.img_base_name
        assert params2.cal_img_base_name == params.cal_img_base_name
        assert params2.hp_flag == params.hp_flag
        assert params2.allcam_flag == params.allcam_flag
        assert params2.tiff_flag == params.tiff_flag
        assert params2.imx == params.imx
        assert params2.imy == params.imy
        assert params2.pix_x == params.pix_x
        assert params2.pix_y == params.pix_y
        assert params2.chfield == params.chfield
        assert params2.mm_np['nlay'] == params.mm_np['nlay']
        assert params2.mm_np['n1'] == params.mm_np['n1']
        assert params2.mm_np['n2'][0] == params.mm_np['n2'][0]
        assert params2.mm_np['n3'] == params.mm_np['n3']
        assert params2.mm_np['d'][0] == params.mm_np['d'][0]


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Parameter bridge not available")
class TestTargetParamsBridge:
    """Tests for the target parameters bridge functions."""

    def test_target_params_roundtrip(self):
        """Test conversion of TargetParams to C struct and back."""
        # Create a parameter object
        params = TargetParams(
            gvthres=[10, 10, 10, 10],
            discont=1,
            nnmin=10,
            nnmax=100,
            nxmin=10,
            nxmax=100,
            nymin=10,
            nymax=100,
            sumg_min=10,
            cr_sz=10,
        )

        # Convert to C struct
        c_params = target_params_to_c(params)

        # Convert back to Python object
        params2 = target_params_from_c(c_params)

        # Check that parameters match
        assert params2.gvthres == params.gvthres
        assert params2.discont == params.discont
        assert params2.nnmin == params.nnmin
        assert params2.nnmax == params.nnmax
        assert params2.nxmin == params.nxmin
        assert params2.nxmax == params.nxmax
        assert params2.nymin == params.nymin
        assert params2.nymax == params.nymax
        assert params2.sumg_min == params.sumg_min
        assert params2.cr_sz == params.cr_sz


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Parameter bridge not available")
class TestOrientParamsBridge:
    """Tests for the orient parameters bridge functions."""

    def test_orient_params_roundtrip(self):
        """Test conversion of OrientParams to C struct and back."""
        # Create a parameter object
        params = OrientParams(
            useflag=1,
            ccflag=1,
            xhflag=1,
            yhflag=1,
            k1flag=1,
            k2flag=1,
            k3flag=1,
            p1flag=1,
            p2flag=1,
            scxflag=1,
            sheflag=1,
            interfflag=1,
        )

        # Convert to C struct
        c_params = orient_params_to_c(params)

        # Convert back to Python object
        params2 = orient_params_from_c(c_params)

        # Check that parameters match
        assert params2.useflag == params.useflag
        assert params2.ccflag == params.ccflag
        assert params2.xhflag == params.xhflag
        assert params2.yhflag == params.yhflag
        assert params2.k1flag == params.k1flag
        assert params2.k2flag == params.k2flag
        assert params2.k3flag == params.k3flag
        assert params2.p1flag == params.p1flag
        assert params2.p2flag == params.p2flag
        assert params2.scxflag == params.scxflag
        assert params2.sheflag == params.sheflag
        assert params2.interfflag == params.interfflag


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Parameter bridge not available")
class TestCalOriParamsBridge:
    """Tests for the calibration and orientation parameters bridge functions."""

    def test_cal_ori_params_roundtrip(self):
        """Test conversion of CalOriParams to C struct and back."""
        # Create a parameter object
        params = CalOriParams(
            ext_par={
                'x0': 0.0,
                'y0': 0.0,
                'z0': 0.0,
                'omega': 0.0,
                'phi': 0.0,
                'kappa': 0.0,
                'dm': [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            },
            int_par={
                'xh': 0.0,
                'yh': 0.0,
                'cc': 100.0,
            },
            glass_par={
                'vec_x': 0.0,
                'vec_y': 0.0,
                'vec_z': 1.0,
                'n1': 1.0,
                'n2': 1.33,
                'n3': 1.0,
                'd': 10.0,
            },
            added_par={
                'k1': 0.0,
                'k2': 0.0,
                'k3': 0.0,
                'p1': 0.0,
                'p2': 0.0,
                'scx': 1.0,
                'she': 0.0,
                'field': 0,
            },
        )

        # Convert to C struct
        c_params = cal_ori_params_to_c(params)

        # Convert back to Python object
        params2 = cal_ori_params_from_c(c_params)

        # Check that parameters match
        assert params2.ext_par['x0'] == params.ext_par['x0']
        assert params2.ext_par['y0'] == params.ext_par['y0']
        assert params2.ext_par['z0'] == params.ext_par['z0']
        assert params2.ext_par['omega'] == params.ext_par['omega']
        assert params2.ext_par['phi'] == params.ext_par['phi']
        assert params2.ext_par['kappa'] == params.ext_par['kappa']
        assert params2.int_par['xh'] == params.int_par['xh']
        assert params2.int_par['yh'] == params.int_par['yh']
        assert params2.int_par['cc'] == params.int_par['cc']
        assert params2.glass_par['vec_x'] == params.glass_par['vec_x']
        assert params2.glass_par['vec_y'] == params.glass_par['vec_y']
        assert params2.glass_par['vec_z'] == params.glass_par['vec_z']
        assert params2.added_par['k1'] == params.added_par['k1']
        assert params2.added_par['k2'] == params.added_par['k2']
        assert params2.added_par['k3'] == params.added_par['k3']
        assert params2.added_par['p1'] == params.added_par['p1']
        assert params2.added_par['p2'] == params.added_par['p2']
        assert params2.added_par['scx'] == params.added_par['scx']
        assert params2.added_par['she'] == params.added_par['she']


if __name__ == "__main__":
    pytest.main(["-v", __file__])
