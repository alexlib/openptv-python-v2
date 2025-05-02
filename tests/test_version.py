import pytest
import openptv

def test_version_available():
    """Test that version is available and properly formatted."""
    assert hasattr(openptv, '__version__')
    assert isinstance(openptv.__version__, str)
    # Check version format (x.y.z)
    parts = openptv.__version__.split('.')
    assert len(parts) == 3
    assert all(part.isdigit() for part in parts)

if __name__ == '__main__':
    pytest.main(["-v", __file__])