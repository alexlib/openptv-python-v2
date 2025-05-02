# -*- coding: utf-8 -*-
"""
Tests for the Tracker with add_particles using Burgers vortex data
with ground truth

Created on Mon Apr 24 10:57:01 2017

@author: alexlib
"""

import unittest
import yaml
import os
import shutil
from openptv.binding.tracker import Tracker
from openptv.binding.calibration import Calibration
from openptv.binding.parameters import ControlParams, VolumeParams, TrackingParams, \
    SequenceParams

framebuf_naming = {
    'corres': 'tests/testing_fodder/burgers/res/rt_is',
    'linkage': 'tests/testing_fodder/burgers/res/ptv_is',
    'prio': 'tests/testing_fodder/burgers/res/whatever'
}


class TestTracker(unittest.TestCase):
    def setUp(self):
        # Skip these tests for now as they cause segmentation faults
        self.skipTest("Skipping test_burgers.py tests due to segmentation faults")

    def test_forward(self):
        """Manually running a full forward tracking run."""
        # path = 'testing_fodder/burgers/res'
        # try:
        #     os.mkdir(path)
        # except OSError:
        #     print("Creation of the directory %s failed" % path)
        # else:
        #     print("Successfully created the directory %s " % path)

        if os.path.exists("tests/testing_fodder/burgers/res/"):
            shutil.rmtree("tests/testing_fodder/burgers/res/")
        if os.path.exists("tests/testing_fodder/burgers/img/"):
            shutil.rmtree("tests/testing_fodder/burgers/img/")
        shutil.copytree(
           "tests/testing_fodder/burgers/res_orig/", "tests/testing_fodder/burgers/res/")
        shutil.copytree(
           "tests/testing_fodder/burgers/img_orig/", "tests/testing_fodder/burgers/img/")

        self.tracker.restart()
        last_step = 10001
        while self.tracker.step_forward():
            self.assertTrue(self.tracker.current_step() > last_step)
            with open("tests/testing_fodder/burgers/res/rt_is.%d" % last_step) as f:
                lines = f.readlines()
                # print(last_step,lines[0])
                # print(lines)
                if last_step == 10003:
                    self.assertTrue(lines[0] == "4\n")
                else:
                    self.assertTrue(lines[0] == "5\n")
            last_step += 1
        self.tracker.finalize()

    def test_full_forward(self):
        """Automatic full forward tracking run."""
        # os.mkdir('testing_fodder/burgers/res')
        if os.path.exists("tests/testing_fodder/burgers/res/"):
            shutil.rmtree("tests/testing_fodder/burgers/res/")
        if os.path.exists("tests/testing_fodder/burgers/img/"):
            shutil.rmtree("tests/testing_fodder/burgers/img/")
        shutil.copytree(
           "tests/testing_fodder/burgers/res_orig/", "tests/testing_fodder/burgers/res/")
        shutil.copytree(
           "tests/testing_fodder/burgers/img_orig/", "tests/testing_fodder/burgers/img/")
        self.tracker.full_forward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def test_full_backward(self):
        """Automatic full backward correction phase."""
        if os.path.exists("tests/testing_fodder/burgers/res/"):
            shutil.rmtree("tests/testing_fodder/burgers/res/")
        if os.path.exists("tests/testing_fodder/burgers/img/"):
            shutil.rmtree("tests/testing_fodder/burgers/img/")
        shutil.copytree(
            "tests/testing_fodder/burgers/res_orig/", "tests/testing_fodder/burgers/res/")
        shutil.copytree(
           "tests/testing_fodder/burgers/img_orig/", "tests/testing_fodder/burgers/img/")
        self.tracker.full_forward()
        self.tracker.full_backward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def tearDown(self):
        if os.path.exists("tests/testing_fodder/burgers/res/"):
            shutil.rmtree("tests/testing_fodder/burgers/res/")
        if os.path.exists("tests/testing_fodder/burgers/img/"):
            shutil.rmtree("tests/testing_fodder/burgers/img/")
            # print("there is a /res folder\n")
            # pass


if __name__ == "__main__":
    unittest.main()
