"""
Test that all parameter classes support to_dict and produce a valid dictionary.
"""
import pytest
from openptv.parameters import (
    TrackingParams, SequenceParams, VolumeParams, ControlParams, TargetParams, OrientParams
)

@pytest.mark.parametrize("cls,kwargs", [
    (TrackingParams, dict(dvxmin=1, dvxmax=2, dvymin=3, dvymax=4, dvzmin=5, dvzmax=6, dangle=0.1, dacc=0.2)),
    (SequenceParams, dict(n_img=2, base_name=["img1", "img2"], first=0, last=10)),
    (VolumeParams, dict()),
    (ControlParams, dict()),
    (TargetParams, dict()),
    (OrientParams, dict()),
])
def test_to_dict_on_all_parameters(cls, kwargs):
    obj = cls(**kwargs)
    d = obj.to_dict()
    assert isinstance(d, dict)
    # Check that all values are serializable (no Path, no callable)
    for v in d.values():
        assert not callable(v)
        # Path objects should be converted to str
        if hasattr(v, "__class__"):
            assert v.__class__.__name__ != "Path"

@pytest.mark.parametrize("cls,kwargs", [
    (TrackingParams, dict(dvxmin=1, dvxmax=2, dvymin=3, dvymax=4, dvzmin=5, dvzmax=6, dangle=0.1, dacc=0.2)),
    (SequenceParams, dict(n_img=2, base_name=["img1", "img2"], first=0, last=10)),
    (VolumeParams, dict()),
    (ControlParams, dict()),
    (TargetParams, dict()),
    (OrientParams, dict()),
])
def test_to_dict_and_from_dict_on_all_parameters(cls, kwargs):
    obj = cls(**kwargs)
    d = obj.to_dict()
    obj2 = cls.from_dict(d)
    d2 = obj2.to_dict()
    assert d == d2
    assert isinstance(obj2, cls)
