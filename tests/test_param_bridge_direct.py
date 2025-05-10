"""
Test the direct parameter bridge between Python and Cython parameter objects.
"""

from openptv.parameters import TrackingParams
from openptv.parameters.param_bridge_direct import tracking_params_to_c

def test_tracking_params_bridge():
    """Test the tracking parameters bridge functions."""
    # Create a Python TrackingParams object
    params = TrackingParams(
        dvxmin=-10.0,
        dvxmax=10.0,
        dvymin=-10.0,
        dvymax=10.0,
        dvzmin=-10.0,
        dvzmax=10.0,
        dangle=0.5,
        dacc=0.5,
        flagNewParticles=True
    )
    
    print("Original Python parameters:")
    print(f"dvxmin: {params.dvxmin}")
    print(f"dvxmax: {params.dvxmax}")
    print(f"dvymin: {params.dvymin}")
    print(f"dvymax: {params.dvymax}")
    print(f"dvzmin: {params.dvzmin}")
    print(f"dvzmax: {params.dvzmax}")
    print(f"dangle: {params.dangle}")
    print(f"dacc: {params.dacc}")
    print(f"flagNewParticles: {params.flagNewParticles}")
    
    # Convert to Cython TrackingParams object
    cython_params = tracking_params_to_c(params)
    
    print("\nCython parameters:")
    print(f"dvxmin: {cython_params.dvxmin}")
    print(f"dvxmax: {cython_params.dvxmax}")
    print(f"dvymin: {cython_params.dvymin}")
    print(f"dvymax: {cython_params.dvymax}")
    print(f"dvzmin: {cython_params.dvzmin}")
    print(f"dvzmax: {cython_params.dvzmax}")
    print(f"dangle: {cython_params.dangle}")
    print(f"dacc: {cython_params.dacc}")
    print(f"add: {cython_params.add}")
    
    # Check that the values are preserved
    assert cython_params.dvxmin == params.dvxmin, f"dvxmin mismatch: {cython_params.dvxmin} != {params.dvxmin}"
    assert cython_params.dvxmax == params.dvxmax, f"dvxmax mismatch: {cython_params.dvxmax} != {params.dvxmax}"
    assert cython_params.dvymin == params.dvymin, f"dvymin mismatch: {cython_params.dvymin} != {params.dvymin}"
    assert cython_params.dvymax == params.dvymax, f"dvymax mismatch: {cython_params.dvymax} != {params.dvymax}"
    assert cython_params.dvzmin == params.dvzmin, f"dvzmin mismatch: {cython_params.dvzmin} != {params.dvzmin}"
    assert cython_params.dvzmax == params.dvzmax, f"dvzmax mismatch: {cython_params.dvzmax} != {params.dvzmax}"
    assert cython_params.dangle == params.dangle, f"dangle mismatch: {cython_params.dangle} != {params.dangle}"
    assert cython_params.dacc == params.dacc, f"dacc mismatch: {cython_params.dacc} != {params.dacc}"
    assert cython_params.add == (1 if params.flagNewParticles else 0), f"add mismatch: {cython_params.add} != {1 if params.flagNewParticles else 0}"
    
    print("\nAll assertions passed! The parameter conversion is working correctly.")

if __name__ == "__main__":
    test_tracking_params_bridge()
