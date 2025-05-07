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

# Import bridge functions
try:
    from openptv.binding.param_bridge import (
        tracking_params_to_c, tracking_params_from_c,
        sequence_params_to_c, sequence_params_from_c,
        volume_params_to_c, volume_params_from_c,
        control_params_to_c, control_params_from_c,
        target_params_to_c, target_params_from_c,
        orient_params_to_c, orient_params_from_c,
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


# Add similar test classes for other parameter types


if __name__ == "__main__":
    pytest.main(["-v", __file__])
