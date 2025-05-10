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
from openptv.parameters import ControlParams, VolumeParams, TrackingParams, \
    SequenceParams
from openptv.parameters.utils import prepare_tracker_paths


class TestTracker(unittest.TestCase):
    def setUp(self):
        # Get the absolute path to the test file directory
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        # Set the working directory to the burgers test folder
        self.working_dir = os.path.join(self.current_dir, "testing_fodder/burgers")

        # Save the original working directory to restore it later
        self.original_cwd = os.getcwd()

        # Change to the working directory
        os.chdir(self.working_dir)

        # Now all paths should be relative to the working directory
        config_path = "conf.yaml"

        with open(config_path) as f:
            yaml_conf = yaml.load(f, Loader=yaml.FullLoader)
        seq_cfg = yaml_conf['sequence']

        self.cals = []
        img_base = []
        print((yaml_conf['cameras']))
        for cix, cam_spec in enumerate(yaml_conf['cameras']):
            cam_spec.setdefault('addpar_file', None)
            cal = Calibration()

            # Fix paths to be relative to the working directory
            # Remove the 'tests/testing_fodder/burgers/' prefix from the paths
            ori_file = cam_spec['ori_file'].replace('tests/testing_fodder/burgers/', '')
            addpar_file = None
            if cam_spec['addpar_file']:
                addpar_file = cam_spec['addpar_file'].replace('tests/testing_fodder/burgers/', '')

            cal.from_file(ori_file, addpar_file)
            self.cals.append(cal)

            # Use a path relative to the working directory
            img_base.append("img/cam{cam:1d}.".format(cam=cix + 1))

        # Extract parameters from the scene configuration
        scene = yaml_conf['scene']

        # Parse flags
        flags = scene.get('flags', '').split(',')
        hp_flag = 'hp' in flags
        allcam_flag = 'allcam' in flags
        tiff_flag = 'headers' in flags

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
        # Extract parameters from the tracking configuration
        track = yaml_conf['tracking']

        # Extract velocity limits
        velocity_lims = track.get('velocity_lims', [[-1.0, 1.0], [-1.0, 1.0], [-1.0, 1.0]])

        # Extract other parameters
        angle_lim = track.get('angle_lim', 0.0)
        accel_lim = track.get('accel_lim', 0.0)
        add_particle = track.get('add_particle', 0)

        # Create the TrackingParams object
        self.tpar = TrackingParams(
            velocity_lims=velocity_lims,
            dangle=angle_lim,
            dacc=accel_lim,
            flagNewParticles=bool(add_particle)
        )
        self.spar = SequenceParams(
            n_img=len(yaml_conf['cameras']),
            base_name=img_base,
            first=seq_cfg['first'],
            last=seq_cfg['last'])

        # Ensure the res directory exists in the working directory
        # The C code is looking for files in a 'res' directory relative to the working directory
        res_path = "res"
        if not os.path.exists(res_path):
            os.makedirs(res_path)

        # Use default paths instead of custom paths
        # The default paths are:
        # 'corres': b'res/rt_is',
        # 'linkage': b'res/ptv_is',
        # 'prio': b'res/added'
        framebuf_naming = None  # This will use the default paths

        # Convert Python parameter objects to Cython objects
        c_cpar = self.cpar.to_cython_object()
        c_vpar = self.vpar.to_cython_object()
        c_tpar = self.tpar.to_cython_object()
        c_spar = self.spar.to_cython_object()

        # Create the tracker with the Cython objects
        self.tracker = Tracker(c_cpar, c_vpar, c_tpar, c_spar, self.cals, framebuf_naming)

    def test_forward(self):
        """Manually running a full forward tracking run."""
        # All paths are now relative to the working directory
        res_path = "res"
        img_path = "img"
        res_orig_path = "res_orig"
        img_orig_path = "img_orig"

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)

        # Create the directories
        os.makedirs(res_path, exist_ok=True)
        os.makedirs(img_path, exist_ok=True)

        # Copy the files
        for file in os.listdir(res_orig_path):
            shutil.copy2(os.path.join(res_orig_path, file), os.path.join(res_path, file))

        for file in os.listdir(img_orig_path):
            shutil.copy2(os.path.join(img_orig_path, file), os.path.join(img_path, file))

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
        # All paths are now relative to the working directory
        res_path = "res"
        img_path = "img"
        res_orig_path = "res_orig"
        img_orig_path = "img_orig"

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)

        # Create the directories
        os.makedirs(res_path, exist_ok=True)
        os.makedirs(img_path, exist_ok=True)

        # Copy the files
        for file in os.listdir(res_orig_path):
            shutil.copy2(os.path.join(res_orig_path, file), os.path.join(res_path, file))

        for file in os.listdir(img_orig_path):
            shutil.copy2(os.path.join(img_orig_path, file), os.path.join(img_path, file))
        self.tracker.full_forward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def test_full_backward(self):
        """Automatic full backward correction phase."""
        # All paths are now relative to the working directory
        res_path = "res"
        img_path = "img"
        res_orig_path = "res_orig"
        img_orig_path = "img_orig"

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)

        # Create the directories
        os.makedirs(res_path, exist_ok=True)
        os.makedirs(img_path, exist_ok=True)

        # Copy the files
        for file in os.listdir(res_orig_path):
            shutil.copy2(os.path.join(res_orig_path, file), os.path.join(res_path, file))

        for file in os.listdir(img_orig_path):
            shutil.copy2(os.path.join(img_orig_path, file), os.path.join(img_path, file))
        self.tracker.full_forward()
        self.tracker.full_backward()
        # if it passes without error, we assume it's ok. The actual test is in
        # the C code.

    def tearDown(self):
        # Clean up file system resources
        # All paths are now relative to the working directory
        res_path = "res"
        img_path = "img"

        if os.path.exists(res_path):
            shutil.rmtree(res_path)
        if os.path.exists(img_path):
            shutil.rmtree(img_path)

        # Restore the original working directory
        os.chdir(self.original_cwd)

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
