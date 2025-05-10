"""
Control parameters for OpenPTV.

This module provides the ControlParams and PtvParams classes for handling control parameters.
"""

from pathlib import Path
import numpy as np

from openptv.parameters.base import Parameters
from openptv.parameters.utils import g, bool_to_int, int_to_bool





class ControlParams(Parameters):
    """
    Control parameters for OpenPTV.

    This class handles reading and writing control parameters to/from files,
    and converting between Python and C representations.
    """

    def __init__(self, n_img=0, img_base_name=None, cal_img_base_name=None,
                 hp_flag=False, allcam_flag=False, tiff_flag=False,
                 imx=0, imy=0, pix_x=0.0, pix_y=0.0, chfield=0,
                 mm_np=None, path=None, mmp_n1=1.0, mmp_n2=1.0, mmp_n3=1.0, mmp_d=1.0):
        """
        Initialize control parameters.

        Args:
            n_img (int): Number of cameras.
            img_base_name (list): List of base names for images.
            cal_img_base_name (list): List of base names for calibration images.
            hp_flag (bool): High-pass filter flag.
            allcam_flag (bool): All cameras flag.
            tiff_flag (bool): TIFF flag.
            imx (int): Image width.
            imy (int): Image height.
            pix_x (float): Pixel width.
            pix_y (float): Pixel height.
            chfield (int): Camera field (0=frame, 1=odd, 2=even).
            mm_np (dict): Multimedia parameters.
            path (str or Path): Path to the parameter directory.
            mmp_n1 (float): Refractive index of air.
            mmp_n2 (float): Refractive index of glass.
            mmp_n3 (float): Refractive index of water.
            mmp_d (float): Thickness of glass.
        """
        super().__init__(path)
        self.set(n_img, img_base_name, cal_img_base_name, hp_flag, allcam_flag,
                 tiff_flag, imx, imy, pix_x, pix_y, chfield, mm_np,
                 mmp_n1, mmp_n2, mmp_n3, mmp_d)

    def set(self, n_img=0, img_base_name=None, cal_img_base_name=None,
            hp_flag=False, allcam_flag=False, tiff_flag=False,
            imx=0, imy=0, pix_x=0.0, pix_y=0.0, chfield=0, mm_np=None,
            mmp_n1=1.0, mmp_n2=1.0, mmp_n3=1.0, mmp_d=1.0):
        """
        Set control parameters.

        Args:
            n_img (int): Number of cameras.
            img_base_name (list): List of base names for images.
            cal_img_base_name (list): List of base names for calibration images.
            hp_flag (bool): High-pass filter flag.
            allcam_flag (bool): All cameras flag.
            tiff_flag (bool): TIFF flag.
            imx (int): Image width.
            imy (int): Image height.
            pix_x (float): Pixel width.
            pix_y (float): Pixel height.
            chfield (int): Camera field (0=frame, 1=odd, 2=even).
            mm_np (dict): Multimedia parameters.
            mmp_n1 (float): Refractive index of air.
            mmp_n2 (float): Refractive index of glass.
            mmp_n3 (float): Refractive index of water.
            mmp_d (float): Thickness of glass.
        """
        if n_img == 0:
            raise ValueError("Number of cameras must be greater than 0")

        self.n_img = n_img
        self.img_base_name = img_base_name or []
        self.cal_img_base_name = cal_img_base_name or []

        # Ensure img_base_name and cal_img_base_name have n_img elements
        if len(self.img_base_name) < self.n_img:
            self.img_base_name.extend([''] * (self.n_img - len(self.img_base_name)))
        if len(self.cal_img_base_name) < self.n_img:
            self.cal_img_base_name.extend([''] * (self.n_img - len(self.cal_img_base_name)))

        # Add aliases for backward compatibility with GUI code
        # self.img_name = self.img_base_name
        # self.img_cal = self.cal_img_base_name

        # Store multimedia parameters
        self.mmp_n1 = mmp_n1
        self.mmp_n2 = mmp_n2
        self.mmp_n3 = mmp_n3
        self.mmp_d = mmp_d

        self.hp_flag = hp_flag
        self.allcam_flag = allcam_flag
        self.tiff_flag = tiff_flag
        self.imx = imx
        self.imy = imy
        self.pix_x = pix_x
        self.pix_y = pix_y
        self.chfield = chfield

        # Default multimedia parameters
        if mm_np is None:
            self.mm_np = {
                'nlay': 1,
                'n1': 1.0,
                'n2': [1.0, 1.0, 1.0],
                'd': [1.0, 1.0, 1.0],
                'n3': 1.0,
            }
        else:
            self.mm_np = mm_np

    def filename(self):
        """
        Get the filename for control parameters.

        Returns:
            str: The filename for control parameters.
        """
        return "ptv.par"

    def read(self):
        """
        Read control parameters from file.

        Raises:
            IOError: If the file cannot be read.
        """
        try:
            with open(self.filepath(), "r") as f:
                self.n_img = int(g(f))

                self.img_base_name = []
                self.cal_img_base_name = []
                for i in range(self.n_img):
                    self.img_base_name.append(g(f))
                    self.cal_img_base_name.append(g(f))

                # Set aliases for backward compatibility
                # self.img_name = self.img_base_name
                # self.img_cal = self.cal_img_base_name

                self.hp_flag = int_to_bool(int(g(f)))
                self.allcam_flag = int_to_bool(int(g(f)))
                self.tiff_flag = int_to_bool(int(g(f)))
                self.imx = int(g(f))
                self.imy = int(g(f))
                self.pix_x = float(g(f))
                self.pix_y = float(g(f))
                self.chfield = int(g(f))

                # Read multimedia parameters
                self.mm_np = {
                    'nlay': 1,
                    'n1': float(g(f)),
                    'n2': [float(g(f)), 0.0, 0.0],
                    'n3': float(g(f)),
                    'd': [float(g(f)), 0.0, 0.0],
                }
        except Exception as e:
            raise IOError(f"Error reading control parameters: {e}")

    def write(self):
        """
        Write control parameters to file.

        Raises:
            IOError: If the file cannot be written.
        """
        try:
            with open(self.filepath(), "w") as f:
                f.write(f"{self.n_img}\n")

                for i in range(self.n_img):
                    f.write(f"{self.img_base_name[i]}\n")
                    f.write(f"{self.cal_img_base_name[i]}\n")

                f.write(f"{bool_to_int(self.hp_flag)}\n")
                f.write(f"{bool_to_int(self.allcam_flag)}\n")
                f.write(f"{bool_to_int(self.tiff_flag)}\n")
                f.write(f"{self.imx}\n")
                f.write(f"{self.imy}\n")
                f.write(f"{self.pix_x}\n")
                f.write(f"{self.pix_y}\n")
                f.write(f"{self.chfield}\n")

                # Write multimedia parameters
                f.write(f"{self.mm_np['n1']}\n")
                f.write(f"{self.mm_np['n2'][0]}\n")
                f.write(f"{self.mm_np['n3']}\n")
                f.write(f"{self.mm_np['d'][0]}\n")
        except Exception as e:
            raise IOError(f"Error writing control parameters: {e}")

    def to_c_struct(self):
        """
        Convert control parameters to a dictionary suitable for creating a C struct.

        Returns:
            dict: A dictionary of control parameter values.
        """
        return {
            'num_cams': self.n_img,
            'img_base_name': self.img_base_name,
            'cal_img_base_name': self.cal_img_base_name,
            'hp_flag': bool_to_int(self.hp_flag),
            'allCam_flag': bool_to_int(self.allcam_flag),
            'tiff_flag': bool_to_int(self.tiff_flag),
            'imx': self.imx,
            'imy': self.imy,
            'pix_x': self.pix_x,
            'pix_y': self.pix_y,
            'chfield': self.chfield,
            'mm': self.mm_np,
        }

    def to_cython_object(self):
        """
        Convert to a Cython ControlParams object.

        Returns:
            openptv.binding.parameters.ControlParams: A Cython ControlParams object.
        """
        from openptv.binding.parameters import ControlParams as CythonControlParams

        # Create flags list
        flags = []
        if self.hp_flag:
            flags.append('hp')
        if self.allcam_flag:
            flags.append('allcam')
        if self.tiff_flag:
            flags.append('headers')

        # Note: The Cython ControlParams constructor doesn't take img_name or cal_img_name directly,
        # but we'll need to set them after creation if we want to use them

        # Create a Cython ControlParams object with the appropriate arguments
        return CythonControlParams(
            num_cams=self.n_img,
            flags=flags,
            image_size=(self.imx, self.imy),
            pixel_size=(self.pix_x, self.pix_y),
            cam_side_n=self.mmp_n1,
            wall_ns=[self.mmp_n2],
            wall_thicks=[self.mmp_d],
            object_side_n=self.mmp_n3
        )

    @classmethod
    def from_c_struct(cls, c_struct, path=None):
        """
        Create a ControlParams object from a C struct.

        Args:
            c_struct: A dictionary of control parameter values from a C struct.
            path: Path to the parameter directory.

        Returns:
            ControlParams: A new ControlParams object.
        """
        return cls(
            n_img=c_struct['num_cams'],
            img_base_name=c_struct['img_base_name'],
            cal_img_base_name=c_struct['cal_img_base_name'],
            hp_flag=int_to_bool(c_struct['hp_flag']),
            allcam_flag=int_to_bool(c_struct['allCam_flag']),
            tiff_flag=int_to_bool(c_struct['tiff_flag']),
            imx=c_struct['imx'],
            imy=c_struct['imy'],
            pix_x=c_struct['pix_x'],
            pix_y=c_struct['pix_y'],
            chfield=c_struct['chfield'],
            mm_np=c_struct['mm'],
            path=path,
        )

    def get_num_cams(self):
        """
        Get the number of cameras.

        Returns:
            int: The number of cameras.
        """
        return self.n_img

    def get_cal_img_base_name(self, cam):
        """
        Get the calibration image base name for a camera.

        Args:
            cam (int): Camera index.

        Returns:
            str: The calibration image base name.
        """
        if cam < 0 or cam >= self.n_img:
            raise ValueError(f"Camera index {cam} out of range (0-{self.n_img-1})")
        return self.cal_img_base_name[cam]


# PtvParams is an alias for ControlParams for backward compatibility
PtvParams = ControlParams
