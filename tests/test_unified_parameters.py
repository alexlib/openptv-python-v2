"""
Tests for the unified parameter module.

This module tests the parameter classes in the openptv.parameters module
and the bridge functions in openptv.binding.param_bridge.
"""

import os
import pytest
import tempfile
from pathlib import Path

import numpy as np

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.control import ControlParams, PtvParams
from openptv.parameters.target import TargetParams, TargRecParams
from openptv.parameters.calibration import CalOriParams
from openptv.parameters.orient import OrientParams
from openptv.parameters.man_ori import ManOriParams
from openptv.parameters.examine import ExamineParams
from openptv.parameters.criteria import CriteriaParams
from openptv.parameters.detect_plate import DetectPlateParams
from openptv.parameters.dumbbell import DumbbellParams
from openptv.parameters.shaking import ShakingParams
from openptv.parameters.pft_version import PftVersionParams


class TestTrackingParams:
    """Tests for the TrackingParams class."""

    def test_init(self):
        """Test initialization of TrackingParams."""
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
        
        assert params.dvxmin == -10.0
        assert params.dvxmax == 10.0
        assert params.dvymin == -10.0
        assert params.dvymax == 10.0
        assert params.dvzmin == -10.0
        assert params.dvzmax == 10.0
        assert params.angle == 0.5
        assert params.dacc == 0.5
        assert params.flagNewParticles is True
    
    def test_to_c_struct(self):
        """Test conversion to C struct."""
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
        
        c_struct = params.to_c_struct()
        
        assert c_struct['dvxmin'] == -10.0
        assert c_struct['dvxmax'] == 10.0
        assert c_struct['dvymin'] == -10.0
        assert c_struct['dvymax'] == 10.0
        assert c_struct['dvzmin'] == -10.0
        assert c_struct['dvzmax'] == 10.0
        assert c_struct['dangle'] == 0.5
        assert c_struct['dacc'] == 0.5
        assert c_struct['add'] == 1
    
    def test_from_c_struct(self):
        """Test creation from C struct."""
        c_struct = {
            'dvxmin': -10.0,
            'dvxmax': 10.0,
            'dvymin': -10.0,
            'dvymax': 10.0,
            'dvzmin': -10.0,
            'dvzmax': 10.0,
            'dangle': 0.5,
            'dacc': 0.5,
            'add': 1,
        }
        
        params = TrackingParams.from_c_struct(c_struct)
        
        assert params.dvxmin == -10.0
        assert params.dvxmax == 10.0
        assert params.dvymin == -10.0
        assert params.dvymax == 10.0
        assert params.dvzmin == -10.0
        assert params.dvzmax == 10.0
        assert params.angle == 0.5
        assert params.dacc == 0.5
        assert params.flagNewParticles is True
    
    def test_read_write(self):
        """Test reading and writing parameters to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
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
                path=temp_dir,
            )
            
            # Write parameters to file
            params.write()
            
            # Create a new parameter object
            params2 = TrackingParams(path=temp_dir)
            
            # Read parameters from file
            params2.read()
            
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


class TestSequenceParams:
    """Tests for the SequenceParams class."""

    def test_init(self):
        """Test initialization of SequenceParams."""
        params = SequenceParams(
            n_img=4,
            base_name=['cam1', 'cam2', 'cam3', 'cam4'],
            first=1,
            last=100,
        )
        
        assert params.n_img == 4
        assert params.base_name == ['cam1', 'cam2', 'cam3', 'cam4']
        assert params.first == 1
        assert params.last == 100
    
    def test_to_c_struct(self):
        """Test conversion to C struct."""
        params = SequenceParams(
            n_img=4,
            base_name=['cam1', 'cam2', 'cam3', 'cam4'],
            first=1,
            last=100,
        )
        
        c_struct = params.to_c_struct()
        
        assert c_struct['num_cams'] == 4
        assert c_struct['img_base_name'] == ['cam1', 'cam2', 'cam3', 'cam4']
        assert c_struct['first'] == 1
        assert c_struct['last'] == 100
    
    def test_from_c_struct(self):
        """Test creation from C struct."""
        c_struct = {
            'num_cams': 4,
            'img_base_name': ['cam1', 'cam2', 'cam3', 'cam4'],
            'first': 1,
            'last': 100,
        }
        
        params = SequenceParams.from_c_struct(c_struct)
        
        assert params.n_img == 4
        assert params.base_name == ['cam1', 'cam2', 'cam3', 'cam4']
        assert params.first == 1
        assert params.last == 100
    
    def test_read_write(self):
        """Test reading and writing parameters to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a parameter object
            params = SequenceParams(
                n_img=4,
                base_name=['cam1', 'cam2', 'cam3', 'cam4'],
                first=1,
                last=100,
                path=temp_dir,
            )
            
            # Write parameters to file
            params.write()
            
            # Create a new parameter object
            params2 = SequenceParams(n_img=4, path=temp_dir)
            
            # Read parameters from file
            params2.read()
            
            # Check that parameters match
            assert params2.n_img == params.n_img
            assert params2.base_name == params.base_name
            assert params2.first == params.first
            assert params2.last == params.last


# Add similar test classes for other parameter types


if __name__ == "__main__":
    pytest.main(["-v", __file__])
