"""
Multi-plane parameters for OpenPTV.

This module provides the MultiPlaneParams class for handling multi-plane
calibration parameters.
"""

from pathlib import Path
from typing import List, Optional, Union

from openptv.parameters.base import Parameters
from openptv.parameters.utils import read_line, write_line


class MultiPlaneParams(Parameters):
    """
    Multi-plane parameters for OpenPTV.

    This class handles parameters for multi-plane calibration, which is used
    when calibrating multiple planes in a single calibration.

    Attributes:
        n_planes: Number of planes.
        plane_name: List of plane names.
        path: Path to the parameter directory.
    """

    def __init__(
        self,
        n_planes: int = 0,
        plane_name: Optional[List[str]] = None,
        path: Optional[Union[str, Path]] = None,
    ):
        """
        Initialize MultiPlaneParams.

        Args:
            n_planes: Number of planes.
            plane_name: List of plane names.
            path: Path to the parameter directory.
        """
        super().__init__(path)
        self.set(n_planes, plane_name or [])

    def set(self, n_planes: int = 0, plane_name: Optional[List[str]] = None):
        """
        Set multi-plane parameters.

        Args:
            n_planes: Number of planes.
            plane_name: List of plane names.
        """
        self.n_planes = n_planes
        self.plane_name = plane_name or []

    def filename(self) -> str:
        """
        Get the filename for multi-plane parameters.

        Returns:
            Filename for multi-plane parameters.
        """
        return "multi_planes.par"

    def read(self) -> None:
        """
        Read multi-plane parameters from file.

        Raises:
            FileNotFoundError: If the parameter file is not found.
            ValueError: If the parameter file has invalid format.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.n_planes = int(read_line(f))
                self.plane_name = []
                for _ in range(self.n_planes):
                    self.plane_name.append(read_line(f))
        except FileNotFoundError:
            raise FileNotFoundError(f"Parameter file {self.filepath()} not found")
        except ValueError as e:
            raise ValueError(f"Invalid format in {self.filepath()}: {e}")

    def write(self) -> None:
        """
        Write multi-plane parameters to file.

        Raises:
            IOError: If there is an error writing the parameter file.
        """
        try:
            with open(self.filepath(), "w") as f:
                write_line(f, str(self.n_planes))
                for i in range(self.n_planes):
                    write_line(f, self.plane_name[i])
        except IOError:
            raise IOError(f"Error writing {self.filepath()}")

    def to_c_struct(self) -> dict:
        """
        Convert multi-plane parameters to a dictionary suitable for creating a C struct.

        Returns:
            Dictionary with parameter values.
        """
        return {
            'n_planes': self.n_planes,
            'plane_name': self.plane_name,
        }

    @classmethod
    def from_c_struct(cls, c_struct: dict, path: Optional[Union[str, Path]] = None):
        """
        Create a MultiPlaneParams object from a C struct.

        Args:
            c_struct: Dictionary with parameter values.
            path: Path to the parameter directory.

        Returns:
            MultiPlaneParams object.
        """
        return cls(
            n_planes=c_struct['n_planes'],
            plane_name=c_struct['plane_name'],
            path=path,
        )
