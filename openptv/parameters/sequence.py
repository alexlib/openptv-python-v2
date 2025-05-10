"""
Sequence parameters for OpenPTV.

This module provides the SequenceParams class for handling sequence parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g


class SequenceParams(Parameters):
    """
    Sequence parameters for OpenPTV.

    This class handles reading and writing sequence parameters to/from files,
    and converting between Python and C representations.
    """

    def __init__(self, n_img=0, base_name=None, first=0, last=0, path=None):
        """
        Initialize sequence parameters.

        Args:
            n_img (int): Number of cameras.
            base_name (list): List of base names for image sequences.
            first (int): First frame number.
            last (int): Last frame number.
            path (str or Path): Path to the parameter directory.
        """
        super().__init__(path)
        self.set(n_img, base_name, first, last)

    def set(self, n_img=0, base_name=None, first=0, last=0):
        """
        Set sequence parameters.

        Args:
            n_img (int): Number of cameras.
            base_name (list): List of base names for image sequences.
            first (int): First frame number.
            last (int): Last frame number.
        """
        if n_img == 0:
            raise ValueError("Number of cameras must be greater than 0")
        
        self.n_img = n_img
        self.base_name = base_name or []
        # Ensure base_name has n_img elements
        if len(self.base_name) < self.n_img:
            self.base_name.extend([''] * (self.n_img - len(self.base_name)))
        self.first = first
        self.last = last

    def filename(self):
        """
        Get the filename for sequence parameters.

        Returns:
            str: The filename for sequence parameters.
        """
        return "sequence.par"

    def read(self):
        """
        Read sequence parameters from file.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.base_name = []
                for i in range(self.n_img):
                    self.base_name.append(g(f))
                self.first = int(g(f))
                self.last = int(g(f))
        except Exception as e:
            raise IOError(f"Error reading sequence parameters: {e}")

    def write(self):
        """
        Write sequence parameters to file.

        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                for i in range(self.n_img):
                    f.write(f"{self.base_name[i]}\n")
                f.write(f"{self.first}\n")
                f.write(f"{self.last}\n")
        except Exception as e:
            raise IOError(f"Error writing sequence parameters: {e}")

    def to_c_struct(self):
        """
        Convert sequence parameters to a dictionary suitable for creating a C struct.

        Returns:
            dict: A dictionary of sequence parameter values.
        """
        return {
            'num_cams': self.n_img,
            'img_base_name': self.base_name,
            'first': self.first,
            'last': self.last,
        }

    def to_cython_object(self):
        """
        Convert to a Cython SequenceParams object.

        Returns:
            openptv.binding.parameters.SequenceParams: A Cython SequenceParams object.
        """
        from openptv.binding.parameters import SequenceParams as CythonSequenceParams

        # Create a Cython SequenceParams object with the appropriate arguments
        cy_params = CythonSequenceParams(
            image_base=self.base_name,
            frame_range=(self.first, self.last)
        )

        return cy_params

    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a SequenceParams object from a C struct.

        Args:
            c_struct: A dictionary of sequence parameter values from a C struct.
            path: Path to the parameter directory.

        Returns:
            SequenceParams: A new SequenceParams object.
        """
        return cls(
            n_img=c_struct['num_cams'],
            base_name=c_struct['img_base_name'],
            first=c_struct['first'],
            last=c_struct['last'],
            path=path,
        )

    def get_first(self):
        """
        Get the first frame number.

        Returns:
            int: The first frame number.
        """
        return self.first

    def set_first(self, first):
        """
        Set the first frame number.

        Args:
            first (int): The first frame number.
        """
        self.first = first

    def get_last(self):
        """
        Get the last frame number.

        Returns:
            int: The last frame number.
        """
        return self.last

    def set_last(self, last):
        """
        Set the last frame number.

        Args:
            last (int): The last frame number.
        """
        self.last = last

    def get_img_base_name(self, cam):
        """
        Get the image base name for a camera.

        Args:
            cam (int): Camera index.

        Returns:
            str: The image base name.
        """
        if cam < 0 or cam >= self.n_img:
            raise ValueError(f"Camera index {cam} out of range (0-{self.n_img-1})")
        return self.base_name[cam]

    def set_img_base_name(self, cam, name):
        """
        Set the image base name for a camera.

        Args:
            cam (int): Camera index.
            name (str): The image base name.
        """
        if cam < 0 or cam >= self.n_img:
            raise ValueError(f"Camera index {cam} out of range (0-{self.n_img-1})")
        self.base_name[cam] = name
