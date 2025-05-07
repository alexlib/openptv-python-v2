"""
Shaking parameters for OpenPTV.

This module provides the ShakingParams class for handling shaking parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g, bool_to_int, int_to_bool


class ShakingParams(Parameters):
    """
    Shaking parameters for OpenPTV.
    
    This class handles reading and writing shaking parameters to/from files.
    """
    
    def __init__(self, shaking_first_frame=0, shaking_last_frame=0, 
                 shaking_max_num_points=0, shaking_max_num_frames=0, 
                 shaking_start_points=None, shaking_end_points=None, 
                 path=None):
        """
        Initialize shaking parameters.
        
        Args:
            shaking_first_frame (int): First frame for shaking.
            shaking_last_frame (int): Last frame for shaking.
            shaking_max_num_points (int): Maximum number of points for shaking.
            shaking_max_num_frames (int): Maximum number of frames for shaking.
            shaking_start_points (list): List of start points for shaking.
            shaking_end_points (list): List of end points for shaking.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(shaking_first_frame, shaking_last_frame, 
                 shaking_max_num_points, shaking_max_num_frames, 
                 shaking_start_points, shaking_end_points)
    
    def set(self, shaking_first_frame=0, shaking_last_frame=0, 
            shaking_max_num_points=0, shaking_max_num_frames=0, 
            shaking_start_points=None, shaking_end_points=None):
        """
        Set shaking parameters.
        
        Args:
            shaking_first_frame (int): First frame for shaking.
            shaking_last_frame (int): Last frame for shaking.
            shaking_max_num_points (int): Maximum number of points for shaking.
            shaking_max_num_frames (int): Maximum number of frames for shaking.
            shaking_start_points (list): List of start points for shaking.
            shaking_end_points (list): List of end points for shaking.
        """
        self.shaking_first_frame = shaking_first_frame
        self.shaking_last_frame = shaking_last_frame
        self.shaking_max_num_points = shaking_max_num_points
        self.shaking_max_num_frames = shaking_max_num_frames
        self.shaking_start_points = shaking_start_points or []
        self.shaking_end_points = shaking_end_points or []
    
    def filename(self):
        """
        Get the filename for shaking parameters.
        
        Returns:
            str: The filename for shaking parameters.
        """
        return "shaking.par"
    
    def read(self):
        """
        Read shaking parameters from file.
        
        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.shaking_first_frame = int(g(f))
                self.shaking_last_frame = int(g(f))
                self.shaking_max_num_points = int(g(f))
                self.shaking_max_num_frames = int(g(f))
                
                self.shaking_start_points = []
                self.shaking_end_points = []
                
                for i in range(self.shaking_max_num_points):
                    self.shaking_start_points.append(int(g(f)))
                    self.shaking_end_points.append(int(g(f)))
        except Exception as e:
            raise IOError(f"Error reading shaking parameters: {e}")
    
    def write(self):
        """
        Write shaking parameters to file.
        
        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.shaking_first_frame}\n")
                f.write(f"{self.shaking_last_frame}\n")
                f.write(f"{self.shaking_max_num_points}\n")
                f.write(f"{self.shaking_max_num_frames}\n")
                
                for i in range(self.shaking_max_num_points):
                    if i < len(self.shaking_start_points):
                        f.write(f"{self.shaking_start_points[i]}\n")
                    else:
                        f.write("0\n")
                    
                    if i < len(self.shaking_end_points):
                        f.write(f"{self.shaking_end_points[i]}\n")
                    else:
                        f.write("0\n")
        except Exception as e:
            raise IOError(f"Error writing shaking parameters: {e}")
    
    def to_c_struct(self):
        """
        Convert shaking parameters to a dictionary suitable for creating a C struct.
        
        Returns:
            dict: A dictionary of shaking parameter values.
        """
        return {
            'shaking_first_frame': self.shaking_first_frame,
            'shaking_last_frame': self.shaking_last_frame,
            'shaking_max_num_points': self.shaking_max_num_points,
            'shaking_max_num_frames': self.shaking_max_num_frames,
            'shaking_start_points': self.shaking_start_points,
            'shaking_end_points': self.shaking_end_points,
        }
    
    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a ShakingParams object from a C struct.
        
        Args:
            c_struct: A dictionary of shaking parameter values from a C struct.
            path: Path to the parameter directory.
        
        Returns:
            ShakingParams: A new ShakingParams object.
        """
        return cls(
            shaking_first_frame=c_struct['shaking_first_frame'],
            shaking_last_frame=c_struct['shaking_last_frame'],
            shaking_max_num_points=c_struct['shaking_max_num_points'],
            shaking_max_num_frames=c_struct['shaking_max_num_frames'],
            shaking_start_points=c_struct['shaking_start_points'],
            shaking_end_points=c_struct['shaking_end_points'],
            path=path,
        )
