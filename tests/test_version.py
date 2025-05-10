import pytest
import openptv
import openptv.gui
import openptv.pyoptv

def test_version_available():
    """Test that version is available and properly formatted."""
    assert hasattr(openptv, '__version__')
    assert isinstance(openptv.__version__, str)
    # Check version format (x.y.z)
    parts = openptv.__version__.split('.')
    assert len(parts) >= 2
    assert all(part.replace('.', '').isdigit() for part in parts)

def test_version_consistency():
    """Test that all modules use the same version."""
    assert hasattr(openptv.gui, '__version__')
    assert hasattr(openptv.pyoptv, '__version__')
    assert openptv.__version__ == openptv.gui.__version__
    assert openptv.__version__ == openptv.pyoptv.__version__

if __name__ == '__main__':
    pytest.main(["-v", __file__])