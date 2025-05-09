"""
Unit tests for the parameters module
"""
import pytest
import os
import tempfile
from pathlib import Path
import yaml
import shutil

from openptv.parameters import Parameters, ControlParams, SequenceParams

@pytest.fixture
def temp_params_dir():
    """Create a temporary directory for parameter files"""
    temp_dir = tempfile.mkdtemp()
    params_dir = Path(temp_dir) / "parameters"
    params_dir.mkdir(exist_ok=True)
    yield params_dir
    shutil.rmtree(temp_dir)

def test_parameters_base_class():
    """Test the base Parameters class"""
    # Test initialization
    params = Parameters()
    assert params.path.name == "parameters"

    # Test with custom path
    custom_path = Path("/tmp/custom_params")
    params = Parameters(custom_path)
    assert params.path == custom_path.resolve()

    # Test filepath method
    with pytest.raises(NotImplementedError):
        params.filename()

    # Test set method
    with pytest.raises(NotImplementedError):
        params.set("var1", "var2")

    # Test read method
    with pytest.raises(NotImplementedError):
        params.read()

def test_ptv_params(temp_params_dir):
    """Test the ControlParams class"""
    params_dir = temp_params_dir  # Use only one 'parameters' directory

    # Create a test ptv.par file
    ptv_par_path = params_dir / "ptv.par"
    with open(ptv_par_path, "w") as f:
        f.write("4\n")  # num_cams
        f.write("img/cam1.%d\n")
        f.write("cal/cam1.tif\n")
        f.write("img/cam2.%d\n")
        f.write("cal/cam2.tif\n")
        f.write("img/cam3.%d\n")
        f.write("cal/cam3.tif\n")
        f.write("img/cam4.%d\n")
        f.write("cal/cam4.tif\n")
        f.write("1\n")  # hp_flag
        f.write("1\n")  # allCam_flag
        f.write("1\n")  # tiff_flag
        f.write("1280\n")  # imx
        f.write("1024\n")  # imy
        f.write("0.012\n")  # pix_x
        f.write("0.012\n")  # pix_y
        f.write("0\n")  # chfield
        f.write("1.0\n")  # mmp_n1
        f.write("1.33\n")  # mmp_n2
        f.write("1.46\n")  # mmp_n3
        f.write("5.0\n")  # mmp_d

    # Create a test ptv.yaml file
    ptv_yaml_path = params_dir / "ptv.yaml"
    ptv_yaml_data = {
        "n_img": 4,
        "img_name": ["img/cam1.%d", "img/cam2.%d", "img/cam3.%d", "img/cam4.%d"],
        "img_cal": ["cal/cam1.tif", "cal/cam2.tif", "cal/cam3.tif", "cal/cam4.tif"],
        "hp_flag": True,
        "allcam_flag": True,
        "tiff_flag": True,
        "imx": 1280,
        "imy": 1024,
        "pix_x": 0.012,
        "pix_y": 0.012,
        "chfield": 0,
        "mmp_n1": 1.0,
        "mmp_n2": 1.33,
        "mmp_n3": 1.46,
        "mmp_d": 5.0
    }
    with open(ptv_yaml_path, "w") as f:
        yaml.dump(ptv_yaml_data, f)

    # Test reading from .par file
    original_dir = Path.cwd()
    os.chdir(params_dir)

    try:
        cparams = ControlParams(path=params_dir)
        cparams.read()
        assert cparams.n_img == 4
        assert cparams.img_name[0] == "img/cam1.%d"
        assert cparams.img_cal[0] == "cal/cam1.tif"
        assert cparams.hp_flag is True
        assert cparams.allcam_flag is True
        assert cparams.tiff_flag is True
        assert cparams.imx == 1280
        assert cparams.imy == 1024
        assert cparams.pix_x == 0.012
        assert cparams.pix_y == 0.012
        assert cparams.chfield == 0
        assert cparams.mmp_n1 == 1.0
        assert cparams.mmp_n2 == 1.33
        assert cparams.mmp_n3 == 1.46
        assert cparams.mmp_d == 5.0

        # Test writing to file
        cparams.n_img = 3
        cparams.write()

        # Read back and verify
        cparams2 = ControlParams(path=params_dir)
        cparams2.read()
        assert cparams2.n_img == 3

        # Remove the .par file and test that YAML is used
        ptv_par_path.unlink()
        cparams3 = ControlParams(path=params_dir)
        cparams3.read()
        assert cparams3.n_img == 3
        # Remove the .yaml file and test fallback to .par
        ptv_yaml_path.unlink()
        with open(ptv_par_path, "w") as f:
            f.write("4\n")
            f.write("img/cam1.%d\n")
            f.write("cal/cam1.tif\n")
            f.write("img/cam2.%d\n")
            f.write("cal/cam2.tif\n")
            f.write("img/cam3.%d\n")
            f.write("cal/cam3.tif\n")
            f.write("img/cam4.%d\n")
            f.write("cal/cam4.tif\n")
            f.write("1\n")
            f.write("1\n")
            f.write("1\n")
            f.write("1280\n")
            f.write("1024\n")
            f.write("0.012\n")
            f.write("0.012\n")
            f.write("0\n")
            f.write("1.0\n")
            f.write("1.33\n")
            f.write("1.46\n")
            f.write("5.0\n")
        cparams4 = ControlParams(path=params_dir)
        cparams4.read()
        assert cparams4.n_img == 4
        ptv_par_path.unlink(missing_ok=True)
        ptv_yaml_path.unlink(missing_ok=True)
    finally:
        os.chdir(original_dir)

def test_sequence_params(temp_params_dir):
    """Test the SequenceParams class"""
    params_dir = temp_params_dir

    # Create a test sequence.par file
    seq_par_path = params_dir / "sequence.par"
    with open(seq_par_path, "w") as f:
        f.write("img/cam1.%d\n")
        f.write("img/cam2.%d\n")
        f.write("img/cam3.%d\n")
        f.write("img/cam4.%d\n")
        f.write("10000\n")  # first
        f.write("10010\n")  # last

    original_dir = Path.cwd()
    os.chdir(params_dir)

    try:
        sparams = SequenceParams(n_img=4, base_name=[], first=0, last=0, path=params_dir)
        sparams.read()
        assert sparams.first == 10000
        assert sparams.last == 10010
        assert len(sparams.base_name) == 4
        assert sparams.base_name[0] == "img/cam1.%d"

        sparams.first = 10001
        sparams.last = 10009
        sparams.write()

        sparams2 = SequenceParams(n_img=4, base_name=[], first=0, last=0, path=params_dir)
        sparams2.read()
        assert sparams2.first == 10001
        assert sparams2.last == 10009
    finally:
        os.chdir(original_dir)

def test_convert_par_to_yaml_script(tmp_path):
    """Test the migration script for converting .par to .yaml"""
    import subprocess
    import os
    param_dir = tmp_path / "parameters"
    param_dir.mkdir()
    ptv_par = param_dir / "ptv.par"
    with open(ptv_par, "w") as f:
        f.write("4\nimg/cam1.%d\ncal/cam1.tif\nimg/cam2.%d\ncal/cam2.tif\nimg/cam3.%d\ncal/cam3.tif\nimg/cam4.%d\ncal/cam4.tif\n1\n1\n1\n1280\n1024\n0.012\n0.012\n0\n1.0\n1.33\n1.46\n5.0\n")
    # Run from project root so script path is correct
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([
        "python", "examples/convert_par_to_yaml.py", str(param_dir)
    ], check=True, cwd=project_root)
    ptv_yaml = param_dir / "ptv.yaml"
    assert ptv_yaml.exists()
    with open(ptv_yaml) as f:
        data = yaml.safe_load(f)
    assert data["n_img"] == 4
