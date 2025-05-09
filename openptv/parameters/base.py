"""
Base parameter class for OpenPTV.

This module provides the base Parameter class that all parameter classes inherit from.
"""

from pathlib import Path
import os
import yaml

# Import from our own utils module
from openptv.parameters.utils import par_dir_prefix


class Parameters:
    """
    Base class for all parameter types.

    This class provides common functionality for all parameter types, such as
    reading and writing parameter files.
    """

    # Default path for parameter files
    default_path = Path(par_dir_prefix())

    def __init__(self, path=None):
        """
        Initialize a Parameters object.

        Args:
            path: Path to the parameter directory. If None, uses the default path.
        """
        if path is None:
            path = self.default_path

        # Convert string to Path if needed
        if isinstance(path, str):
            path = Path(path)

        self.path = path.resolve()
        self.exp_path = self.path.parent

    def filename(self):
        """
        Get the filename for this parameter type.

        Returns:
            str: The filename for this parameter type.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement filename()")

    def filepath(self):
        """
        Get the full path to the parameter file.

        Returns:
            Path: The full path to the parameter file.
        """
        return self.path.joinpath(self.filename())

    def set(self, *args, **kwargs):
        """
        Set parameter values.

        Args:
            *args: Positional arguments to set parameter values.
            **kwargs: Keyword arguments to set parameter values.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement set()")

    def read(self):
        """
        Read parameter values from file.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement read()")

    def write(self):
        """
        Write parameter values to file.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement write()")

    def to_c_struct(self):
        """
        Convert parameter values to a dictionary suitable for creating a C struct.

        Returns:
            dict: A dictionary of parameter values.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement to_c_struct()")

    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a Parameters object from a C struct.

        Args:
            c_struct: A dictionary of parameter values from a C struct.
            path: Path to the parameter directory. If None, uses the default path.

        Returns:
            Parameters: A new Parameters object.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement from_c_struct()")

    @classmethod
    def from_dict(cls, d):
        """
        Create an instance from a dictionary, setting attributes that match the constructor or are public fields.

        Args:
            d: A dictionary with parameter values.

        Returns:
            Parameters: A new Parameters object.
        """
        obj = cls()
        for k, v in d.items():
            setattr(obj, k, v)
        return obj

    def istherefile(self, filename):
        """
        Check if a file exists.

        Args:
            filename: The filename to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        if filename is None or filename == "":
            return False

        # Check if the file exists relative to the experiment path
        filepath = self.exp_path / filename
        return filepath.exists()

    def to_yaml(self):
        """
        Write the parameter values to a YAML file with the same base name as the parameter file.
        Converts Path objects to str to ensure YAML is safe-loadable.
        """
        import yaml
        yaml_file = self.filepath().with_suffix('.yaml')
        def _to_primitive(val):
            if isinstance(val, Path):
                return str(val)
            elif isinstance(val, (list, tuple)):
                return [_to_primitive(v) for v in val]
            elif isinstance(val, dict):
                return {k: _to_primitive(v) for k, v in val.items()}
            else:
                return val
        data = {k: _to_primitive(v) for k, v in self.__dict__.items() if not k.startswith('_') and not callable(v)}
        with open(yaml_file, "w") as outfile:
            yaml.safe_dump(data, outfile, default_flow_style=False)

    def to_dict(self):
        """
        Convert all public attributes to a dictionary, recursively handling Path, list, and dict types.
        """
        def _to_primitive(val):
            if isinstance(val, Path):
                return str(val)
            elif isinstance(val, (list, tuple)):
                return [_to_primitive(v) for v in val]
            elif isinstance(val, dict):
                return {k: _to_primitive(v) for k, v in val.items()}
            else:
                return val
        return {k: _to_primitive(v) for k, v in self.__dict__.items() if not k.startswith('_') and not callable(v)}
