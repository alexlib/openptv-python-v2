#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for debugging path handling issues in the tracker.

This test creates a simple tracker with different path formats and prints
detailed information about how the paths are being handled.
"""

import os
import sys
import unittest
from pathlib import Path

from openptv.binding.tracker import Tracker, _encode_if_needed
from openptv.binding.calibration import Calibration
from openptv.parameters import ControlParams, VolumeParams, TrackingParams, SequenceParams
from openptv.parameters.utils import prepare_tracker_paths


class TestPathHandling(unittest.TestCase):
    """Test path handling in the tracker."""

    def setUp(self):
        """Set up test parameters."""
        # Get the absolute path to the test file directory
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        # Create minimal parameter objects
        self.cpar = ControlParams(
            n_img=1,
            hp_flag=0,
            allcam_flag=0,
            tiff_flag=0,
            imx=1024,
            imy=1024,
            pix_x=0.01,
            pix_y=0.01,
            mmp_n1=1.0,
            mmp_n2=1.0,
            mmp_n3=1.0,
            mmp_d=0.0
        )

        self.vpar = VolumeParams(
            X_lay=[0.0, 100.0],
            Zmin_lay=[-50.0, -50.0],
            Zmax_lay=[50.0, 50.0],
            cnx=0.0,
            cny=0.0,
            cn=0.0,
            csumg=0.0,
            corrmin=0.0,
            eps0=0.0
        )

        self.tpar = TrackingParams(
            velocity_lims=[[-1.0, 1.0], [-1.0, 1.0], [-1.0, 1.0]],
            dangle=0.0,
            dacc=0.0,
            flagNewParticles=False
        )

        self.spar = SequenceParams(
            n_img=1,
            base_name=["img"],
            first=1,
            last=10
        )

        # Create a minimal calibration
        self.cal = Calibration()
        self.cal.set_pos([0.0, 0.0, 0.0])
        self.cal.set_angles([0.0, 0.0, 0.0])
        self.cals = [self.cal]

        # Ensure test directories exist
        self.test_dir = os.path.join(self.current_dir, "testing_fodder/path_test")
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def test_path_handling(self):
        """Test different path formats."""
        print("\n=== Testing Path Handling ===")

        # Test 1: Using relative paths with strings
        print("\nTest 1: Using relative paths with strings")
        paths1 = {
            'corres': "testing_fodder/path_test/rt_is",
            'linkage': "testing_fodder/path_test/ptv_is",
            'prio': "testing_fodder/path_test/added"
        }

        print("Original paths:")
        for k, v in paths1.items():
            print(f"  {k}: {v} (type: {type(v)})")

        # Convert using our utility
        prepared_paths1 = prepare_tracker_paths(paths1)
        print("\nPrepared paths:")
        for k, v in prepared_paths1.items():
            print(f"  {k}: {v} (type: {type(v)})")

        # Test with Tracker
        try:
            c_cpar = self.cpar.to_cython_object()
            c_vpar = self.vpar.to_cython_object()
            c_tpar = self.tpar.to_cython_object()
            c_spar = self.spar.to_cython_object()

            tracker1 = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals, prepared_paths1)
            print("  ✓ Successfully created tracker with prepared relative paths")
        except Exception as e:
            print(f"  ✗ Failed to create tracker: {str(e)}")

        # Test 2: Using absolute paths with strings
        print("\nTest 2: Using absolute paths with strings")
        paths2 = {
            'corres': os.path.join(self.current_dir, "testing_fodder/path_test/rt_is"),
            'linkage': os.path.join(self.current_dir, "testing_fodder/path_test/ptv_is"),
            'prio': os.path.join(self.current_dir, "testing_fodder/path_test/added")
        }

        print("Original paths:")
        for k, v in paths2.items():
            print(f"  {k}: {v} (type: {type(v)})")

        # Convert using our utility
        prepared_paths2 = prepare_tracker_paths(paths2)
        print("\nPrepared paths:")
        for k, v in prepared_paths2.items():
            print(f"  {k}: {v} (type: {type(v)})")

        # Test with Tracker
        try:
            c_cpar = self.cpar.to_cython_object()
            c_vpar = self.vpar.to_cython_object()
            c_tpar = self.tpar.to_cython_object()
            c_spar = self.spar.to_cython_object()

            tracker2 = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals, prepared_paths2)
            print("  ✓ Successfully created tracker with prepared absolute paths")
        except Exception as e:
            print(f"  ✗ Failed to create tracker: {str(e)}")

        # Test 3: Using default paths
        print("\nTest 3: Using default paths")
        try:
            c_cpar = self.cpar.to_cython_object()
            c_vpar = self.vpar.to_cython_object()
            c_tpar = self.tpar.to_cython_object()
            c_spar = self.spar.to_cython_object()

            tracker3 = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals)
            print("  ✓ Successfully created tracker with default paths")
        except Exception as e:
            print(f"  ✗ Failed to create tracker: {str(e)}")

    def tearDown(self):
        """Clean up after tests."""
        # Clean up test directories
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir)


if __name__ == "__main__":
    unittest.main()
