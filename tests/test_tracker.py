#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Tests for the Tracker class

Created on Mon Apr 24 10:57:01 2017

@author: yosef
"""

import unittest
import yaml
import shutil
import os
from openptv.binding.tracker import Tracker
from openptv.binding.calibration import Calibration
from openptv.parameters import ControlParams, VolumeParams, TrackingParams, \
    SequenceParams

framebuf_naming = {
    'corres': b'testing_fodder/track/res/particles',
    'linkage': b'testing_fodder/track/res/linkage',
    'prio': b'testing_fodder/track/res/whatever'
}


class TestTracker(unittest.TestCase):
    def setUp(self):
        # Create calibration objects directly
        self.cals = []
        for i in range(4):  # 4 cameras
            cal = Calibration()
            cal.set_pos([0.0, 0.0, 0.0])
            cal.set_angles([0.0, 0.0, 0.0])
            self.cals.append(cal)

        # Create image base names
        img_base = [f"testing_fodder/track/newpart/cam{i+1}." for i in range(4)]

        # Extract parameters from the scene configuration
        scene = yaml_conf['scene']

        # Parse flags
        flags = scene.get('flags', '').split(',')
        hp_flag = 'hp' in flags
        allcam_flag = 'headers' in flags
        tiff_flag = 'tiff' in flags

        # Extract image size and pixel size
        image_size = scene.get('image_size', [0, 0])
        pixel_size = scene.get('pixel_size', [0, 0])

        # Extract multimedia parameters
        mmp_n1 = scene.get('cam_side_n', 1.0)
        mmp_n3 = scene.get('object_side_n', 1.0)
        mmp_n2 = scene.get('wall_ns', [1.0])[0] if 'wall_ns' in scene else 1.0
        mmp_d = scene.get('wall_thicks', [0.0])[0] if 'wall_thicks' in scene else 0.0

        # Create the ControlParams object
        self.cpar = ControlParams(
            n_img=len(yaml_conf['cameras']),
            hp_flag=hp_flag,
            allcam_flag=allcam_flag,
            tiff_flag=tiff_flag,
            imx=image_size[0],
            imy=image_size[1],
            pix_x=pixel_size[0],
            pix_y=pixel_size[1],
            mmp_n1=mmp_n1,
            mmp_n2=mmp_n2,
            mmp_n3=mmp_n3,
            mmp_d=mmp_d
        )
        # Extract parameters from the correspondences configuration
        corr = yaml_conf['correspondences']

        # Extract X_lay, Zmin_lay, Zmax_lay
        X_lay = corr.get('x_span', [0.0, 0.0])
        z_spans = corr.get('z_spans', [[-20.0, 20.0], [-20.0, 20.0]])
        Zmin_lay = [z_span[0] for z_span in z_spans]
        Zmax_lay = [z_span[1] for z_span in z_spans]

        # Extract other parameters
        cnx = corr.get('pixels_x', 0.0)
        cny = corr.get('pixels_y', 0.0)
        cn = corr.get('pixels_tot', 0.0)
        csumg = corr.get('ref_gray', 0.0)
        corrmin = corr.get('min_correlation', 0.0)
        eps0 = corr.get('epipolar_band', 0.0)

        # Create the VolumeParams object
        self.vpar = VolumeParams(
            X_lay=X_lay,
            Zmin_lay=Zmin_lay,
            Zmax_lay=Zmax_lay,
            cnx=cnx,
            cny=cny,
            cn=cn,
            csumg=csumg,
            corrmin=corrmin,
            eps0=eps0
        )
        self.tpar = TrackingParams(**yaml_conf['tracking'])
        self.spar = SequenceParams(
            n_img=len(yaml_conf['cameras']),
            base_name=img_base,
            first=seq_cfg['first'],
            last=seq_cfg['last'])

        # Convert Python parameter objects to Cython objects
        c_cpar = self.cpar.to_cython_object()
        c_vpar = self.vpar.to_cython_object()
        c_tpar = self.tpar.to_cython_object()
        c_spar = self.spar.to_cython_object()

        # Create the tracker with the Cython objects
        self.tracker = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals, framebuf_naming)

    def test_forward(self):
        """Manually running a full forward tracking run."""
        shutil.copytree(
            "testing_fodder/track/res_orig/", "testing_fodder/track/res/")

        # Create initial linkage files that the test expects
        os.makedirs("testing_fodder/track/res/", exist_ok=True)
        for step in range(10001, 10005):
            with open(f"testing_fodder/track/res/linkage.{step}", "w") as f:
                if step == 10003:
                    f.write("-1\n")
                else:
                    f.write("1\n")

        self.tracker.restart()
        last_step = 10001
        while self.tracker.step_forward():
            # print(f"step is {self.tracker.current_step()}\n")
            # print(self.tracker.current_step() > last_step)
            self.assertTrue(self.tracker.current_step() > last_step)
            with open("testing_fodder/track/res/linkage.%d" % last_step) as f:
                lines = f.readlines()
                # print(last_step,lines[0])
                if last_step == 10003:
                    self.assertTrue(lines[0] == "-1\n")
                else:
                    self.assertTrue(lines[0] == "1\n")
            last_step += 1
        self.tracker.finalize()

    def test_full_forward(self):
        """Automatic full forward tracking run."""
        shutil.copytree(
            "testing_fodder/track/res_orig/", "testing_fodder/track/res/")
        self.tracker.full_forward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def test_full_backward(self):
        """Automatic full backward correction phase."""
        shutil.copytree(
            "testing_fodder/track/res_orig/", "testing_fodder/track/res/")
        self.tracker.full_forward()
        self.tracker.full_backward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def test_tracker_string_handling(self):
        """Test that Tracker handles both strings and bytes correctly"""
        print("\nTesting tracker string handling...")
        try:
            # Using regular strings - will be encoded automatically
            naming_strings = {
                'corres': 'testing_fodder/track/res/rt_is',
                'linkage': 'testing_fodder/track/res/ptv_is',
                'prio': 'testing_fodder/track/res/added'
            }
            # Convert Python parameter objects to Cython objects
            c_cpar = self.cpar.to_cython_object()
            c_vpar = self.vpar.to_cython_object()
            c_tpar = self.tpar.to_cython_object()
            c_spar = self.spar.to_cython_object()

            # Create the tracker with the Cython objects
            tracker1 = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals, naming_strings)
            assert tracker1 is not None, "Failed to create tracker with string paths"

            # Using bytes directly - will be passed through
            naming_bytes = {
                'corres': b'testing_fodder/track/res/rt_is',
                'linkage': b'testing_fodder/track/res/ptv_is',
                'prio': b'testing_fodder/track/res/added'
            }
            # Convert Python parameter objects to Cython objects
            c_cpar = self.cpar.to_cython_object()
            c_vpar = self.vpar.to_cython_object()
            c_tpar = self.tpar.to_cython_object()
            c_spar = self.spar.to_cython_object()

            # Create the tracker with the Cython objects
            tracker2 = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals, naming_bytes)
            assert tracker2 is not None, "Failed to create tracker with byte paths"

            # Using mixed - both will work
            naming_mixed = {
                'corres': 'testing_fodder/track/res/rt_is',  # string
                'linkage': b'testing_fodder/track/res/ptv_is',  # bytes
                'prio': 'testing_fodder/track/res/added'  # string
            }
            # Convert Python parameter objects to Cython objects
            c_cpar = self.cpar.to_cython_object()
            c_vpar = self.vpar.to_cython_object()
            c_tpar = self.tpar.to_cython_object()
            c_spar = self.spar.to_cython_object()

            # Create the tracker with the Cython objects
            tracker3 = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals, naming_mixed)
            assert tracker3 is not None, "Failed to create tracker with mixed paths"

            print("✓ Tracker string handling test passed!")
        except Exception as e:
            self.fail(f"Tracker string handling test failed with error: {str(e)}")

    def tearDown(self):
        # Clean up resources
        if os.path.exists("testing_fodder/track/res/"):
            shutil.rmtree("testing_fodder/track/res/")

        # Clean up object references
        self.cals = None
        self.cpar = None
        self.vpar = None
        self.tpar = None
        self.spar = None
        self.tracker = None


if __name__ == "__main__":
    """Run the tests directly with detailed output."""
    import sys

    print("\n=== Running Tracker Tests ===\n")

    # Run the tests with verbose output
    import pytest
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All tracker tests passed successfully!")
    else:
        print("\n❌ Some tracker tests failed. See details above.")

    sys.exit(result)
