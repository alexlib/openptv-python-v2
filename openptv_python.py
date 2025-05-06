"""
Dummy module to fix import issues.
"""

# This module is imported by openptv/__init__.py
# We're creating it as a dummy module to fix the import error

# Import the real openptv module
import openptv

# Re-export everything from openptv
from openptv import *

# Define any missing symbols
__version__ = openptv.__version__
