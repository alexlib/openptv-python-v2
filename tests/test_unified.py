import os
import tempfile
import yaml
import pytest
from openptv.parameters.unified import UnifiedParameters
from openptv.parameters.control import ControlParams
from openptv.parameters.sequence import SequenceParams
from openptv.parameters.volume import VolumeParams
from openptv.parameters.tracking import TrackingParams
from openptv.parameters.target import TargetParams
from openptv.parameters.examine import ExamineParams
from openptv.parameters.calibration import CalOriParams
from openptv.parameters.man_ori import ManOriParams
from openptv.parameters.multi_plane import MultiPlaneParams
from openptv.parameters.pft_version import PftVersionParams
from openptv.parameters.shaking import ShakingParams
from openptv.parameters.dumbbell import DumbbellParams


def make_minimal_params():
    cpar = ControlParams(n_img=2, img_name=["img1", "img2"], img_cal=["cal1", "cal2"], hp_flag=True, allcam_flag=True, tiff_flag=True, imx=100, imy=100, pix_x=0.01, pix_y=0.01, chfield=0, mmp_n1=1.0, mmp_n2=1.33, mmp_n3=1.46, mmp_d=5.0)
    sequence = SequenceParams(base_name=["seq1", "seq2"], first=1, last=2)
    volume = VolumeParams(cn=1, cnx=2, cny=3)
    tracking = TrackingParams(dvxmin=0.1, dvxmax=0.2, dvymin=0.3, dvymax=0.4, dvzmin=0.5, dvzmax=0.6, angle=0.7, dacc=0.8, add_particle=1)
    target = TargetParams(discont=1, gvthresh=[2, 3, 4, 5], pixel_count_bounds=(10, 100), xsize_bounds=(20, 200), ysize_bounds=(30, 300), min_sum_grey=60, cross_size=3)
    detect_plate = TargetParams()
    targ_rec = TargetParams()
    criteria = VolumeParams()
    examine = ExamineParams()
    cal_ori = CalOriParams()
    man_ori = ManOriParams()
    multi_plane = MultiPlaneParams()
    pft_version = PftVersionParams()
    shaking = ShakingParams()
    dumbbell = DumbbellParams()
    return (cpar, sequence, volume, tracking, target, detect_plate, targ_rec, criteria, examine, cal_ori, man_ori, multi_plane, pft_version, shaking, dumbbell)


def test_unifiedparameters_write_and_read(tmp_path):
    # Create minimal parameter objects
    params = make_minimal_params()
    up = UnifiedParameters(tmp_path / "params.yaml")
    up.from_classes(*params)
    up.write()
    # Read back
    up2 = UnifiedParameters(tmp_path / "params.yaml")
    up2.read()
    cpar2, sequence2, volume2, tracking2, *_ = up2.to_classes()
    assert cpar2.n_img == 2
    assert sequence2.base_name[0] == "seq1"
    assert volume2.cn == 1
    assert tracking2.dvxmin == 0.1


def test_unifiedparameters_set_and_get_section():
    up = UnifiedParameters()
    cpar = ControlParams(n_img=3)
    up.set_section("control", cpar)
    section = up.get_section("control")
    assert isinstance(section, ControlParams)
    assert section.n_img == 3


def test_unifiedparameters_get_num_cams():
    up = UnifiedParameters()
    up.data = {"control": {"n_img": 5}}
    assert up.get_num_cams() == 5
    up.data = {}
    assert up.get_num_cams() == 0


def test_unifiedparameters_pprint():
    up = UnifiedParameters()
    up.data = {"foo": {"bar": 1}}
    s = up.pprint()
    assert "foo" in s and "bar" in s


def test_unifiedparameters_set_path():
    up = UnifiedParameters()
    up.set_path("/tmp/test.yaml")
    assert str(up.path) == "/tmp/test.yaml"


def test_unifiedparameters_get_gui_param():
    up = UnifiedParameters()
    up.data = {"gui": {"theme": "dark"}}
    assert up.get_gui_param("theme") == "dark"
    assert up.get_gui_param("missing") is None
