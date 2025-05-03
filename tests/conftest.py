import os
import pytest

# Set GUI backend before any imports
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyside6'

# Skip GUI tests when running headless
@pytest.fixture(scope="session", autouse=True)
def check_display():
    if "DISPLAY" not in os.environ and "WAYLAND_DISPLAY" not in os.environ:
        pytest.skip("GUI tests require a display")
