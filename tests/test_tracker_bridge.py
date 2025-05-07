"""
Tests for the tracker bridge functions.

This module tests the bridge functions in openptv.binding.tracker_bridge.
"""

import os
import pytest
import numpy as np

from openptv.parameters.tracking import TrackingParams
from openptv.parameters.volume import VolumeParams
from openptv.binding.tracking_framebuf import TargetArray

# Import bridge functions
try:
    from openptv.binding.tracker_bridge import track_forward_with_params
    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False


@pytest.mark.skipif(not BRIDGE_AVAILABLE, reason="Tracker bridge not available")
class TestTrackerBridge:
    """Tests for the tracker bridge functions."""

    def test_track_forward_with_params(self):
        """Test the track_forward_with_params function."""
        # Create tracking parameters
        track_params = TrackingParams(
            dvxmin=-10.0,
            dvxmax=10.0,
            dvymin=-10.0,
            dvymax=10.0,
            dvzmin=-10.0,
            dvzmax=10.0,
            dangle=0.1,
            dacc=0.5,
            add=10,
            dsumg=10,
            dn=10,
            dnx=10,
            dny=10,
        )
        
        # Create volume parameters
        vol_params = VolumeParams(
            X_lay=[0.0, 100.0],
            Zmin_lay=[0.0, 0.0],
            Zmax_lay=[100.0, 100.0],
            cnx=1.0,
            cny=1.0,
            cn=1.0,
            csumg=1.0,
            corrmin=0.5,
            eps0=0.1,
        )
        
        # Create target arrays
        targets = [TargetArray(0) for _ in range(4)]
        
        # Call the function
        results = track_forward_with_params(targets, track_params, vol_params)
        
        # Check that the results are as expected
        assert isinstance(results, dict)
        assert 'links' in results
        assert 'lost' in results
        assert 'added' in results


if __name__ == "__main__":
    pytest.main(["-v", __file__])
