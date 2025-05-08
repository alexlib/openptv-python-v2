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

# Will be set in setUp
framebuf_naming = {
    'corres': b'',
    'linkage': b'',
    'prio': b''
}


class TestTracker(unittest.TestCase):
    def setUp(self):
        import os
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "testing_fodder/burgers/conf.yaml")

        with open(config_path) as f:
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

        # Update framebuf_naming with correct paths
        global framebuf_naming
        framebuf_naming = {
            'corres': os.path.join(current_dir, "testing_fodder/burgers/res/rt_is").encode(),
            'linkage': os.path.join(current_dir, "testing_fodder/burgers/res/ptv_is").encode(),
            'prio': os.path.join(current_dir, "testing_fodder/burgers/res/whatever").encode()
        }

        self.tracker = Tracker(self.cpar, self.vpar, self.tpar, self.spar, self.cals, framebuf_naming)

    def test_forward(self):
        """Manually running a full forward tracking run."""
        # path = 'testing_fodder/burgers/res'
        # try:
        #     os.mkdir(path)
        # except OSError:
        #     print("Creation of the directory %s failed" % path)
        # else:
        #     print("Successfully created the directory %s " % path)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        res_path = os.path.join(current_dir, "testing_fodder/burgers/res/")
        img_path = os.path.join(current_dir, "testing_fodder/burgers/img/")
        res_orig_path = os.path.join(current_dir, "testing_fodder/burgers/res_orig/")
        img_orig_path = os.path.join(current_dir, "testing_fodder/burgers/img_orig/")

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)
        shutil.copytree(res_orig_path, res_path)
        shutil.copytree(img_orig_path, img_path)

        self.tracker.restart()
        last_step = 10001
        while self.tracker.step_forward():
            self.assertTrue(self.tracker.current_step() > last_step)
            with open(os.path.join(res_path, f"rt_is.{last_step}")) as f:
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        res_path = os.path.join(current_dir, "testing_fodder/burgers/res/")
        img_path = os.path.join(current_dir, "testing_fodder/burgers/img/")
        res_orig_path = os.path.join(current_dir, "testing_fodder/burgers/res_orig/")
        img_orig_path = os.path.join(current_dir, "testing_fodder/burgers/img_orig/")

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)
        shutil.copytree(res_orig_path, res_path)
        shutil.copytree(img_orig_path, img_path)
        self.tracker.full_forward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def test_full_backward(self):
        """Automatic full backward correction phase."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        res_path = os.path.join(current_dir, "testing_fodder/burgers/res/")
        img_path = os.path.join(current_dir, "testing_fodder/burgers/img/")
        res_orig_path = os.path.join(current_dir, "testing_fodder/burgers/res_orig/")
        img_orig_path = os.path.join(current_dir, "testing_fodder/burgers/img_orig/")

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)
        shutil.copytree(res_orig_path, res_path)
        shutil.copytree(img_orig_path, img_path)
        self.tracker.full_forward()
        self.tracker.full_backward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def tearDown(self):
        # Clean up file system resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        res_path = os.path.join(current_dir, "testing_fodder/burgers/res/")
        img_path = os.path.join(current_dir, "testing_fodder/burgers/img/")

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)

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

    print("\n=== Running Burgers Vortex Tracker Tests ===\n")

    # Run the tests with verbose output
    import pytest
    result = pytest.main(["-v", __file__])

    if result == 0:
        print("\n✅ All Burgers vortex tracker tests passed successfully!")
    else:
        print("\n❌ Some Burgers vortex tracker tests failed. See details above.")

    sys.exit(result)
