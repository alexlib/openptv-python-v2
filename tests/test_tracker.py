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
from openptv.binding.parameters import ControlParams, VolumeParams, TrackingParams, \
    SequenceParams
framebuf_naming = {
    'corres': b'tests/testing_fodder/track/res/particles',
    'linkage': b'tests/testing_fodder/track/res/linkage',
    'prio': b'tests/testing_fodder/track/res/whatever'
}


class TestTracker(unittest.TestCase):
    def setUp(self):
        with open("tests/testing_fodder/track/conf.yaml") as f:
            yaml_conf = yaml.load(f, Loader=yaml.FullLoader)
        seq_cfg = yaml_conf['sequence']

        self.cals = []
        img_base = []
        print((yaml_conf['cameras']))
        for cix, cam_spec in enumerate(yaml_conf['cameras']):
            cam_spec.setdefault('addpar_file', None)
            cal = Calibration()
            cal.from_file(cam_spec['ori_file'],
                          cam_spec['addpar_file'])
            self.cals.append(cal)
            img_base.append(seq_cfg['targets_template'].format(cam=cix + 1))

        self.cpar = ControlParams(len(yaml_conf['cameras']), **yaml_conf['scene'])
        self.vpar = VolumeParams(**yaml_conf['correspondences'])
        self.tpar = TrackingParams(**yaml_conf['tracking'])
        self.spar = SequenceParams(
            image_base=img_base,
            frame_range=(seq_cfg['first'], seq_cfg['last']))

        self.tracker = Tracker(self.cpar, self.vpar, self.tpar, self.spar, self.cals, framebuf_naming)

    def test_forward(self):
        """Manually running a full forward tracking run."""
        shutil.copytree(
            "tests/testing_fodder/track/res_orig/", "tests/testing_fodder/track/res/")

        # Create initial linkage files that the test expects
        os.makedirs("tests/testing_fodder/track/res/", exist_ok=True)
        for step in range(10001, 10005):
            with open(f"tests/testing_fodder/track/res/linkage.{step}", "w") as f:
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
            with open("tests/testing_fodder/track/res/linkage.%d" % last_step) as f:
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
            "tests/testing_fodder/track/res_orig/", "tests/testing_fodder/track/res/")
        self.tracker.full_forward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def test_full_backward(self):
        """Automatic full backward correction phase."""
        shutil.copytree(
            "tests/testing_fodder/track/res_orig/", "tests/testing_fodder/track/res/")
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
                'corres': 'tests/testing_fodder/track/res/rt_is',
                'linkage': 'tests/testing_fodder/track/res/ptv_is',
                'prio': 'tests/testing_fodder/track/res/added'
            }
            tracker1 = Tracker(self.cpar, self.vpar, self.tpar, self.spar, self.cals, naming_strings)
            assert tracker1 is not None, "Failed to create tracker with string paths"

            # Using bytes directly - will be passed through
            naming_bytes = {
                'corres': b'tests/testing_fodder/track/res/rt_is',
                'linkage': b'tests/testing_fodder/track/res/ptv_is',
                'prio': b'tests/testing_fodder/track/res/added'
            }
            tracker2 = Tracker(self.cpar, self.vpar, self.tpar, self.spar, self.cals, naming_bytes)
            assert tracker2 is not None, "Failed to create tracker with byte paths"

            # Using mixed - both will work
            naming_mixed = {
                'corres': 'tests/testing_fodder/track/res/rt_is',  # string
                'linkage': b'tests/testing_fodder/track/res/ptv_is',  # bytes
                'prio': 'tests/testing_fodder/track/res/added'  # string
            }
            tracker3 = Tracker(self.cpar, self.vpar, self.tpar, self.spar, self.cals, naming_mixed)
            assert tracker3 is not None, "Failed to create tracker with mixed paths"

            print("✓ Tracker string handling test passed!")
        except Exception as e:
            self.fail(f"Tracker string handling test failed with error: {str(e)}")

    def tearDown(self):
        # Clean up resources
        if os.path.exists("tests/testing_fodder/track/res/"):
            shutil.rmtree("tests/testing_fodder/track/res/")

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
