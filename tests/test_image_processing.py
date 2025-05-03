import unittest
from openptv.binding.parameters import ControlParams
from openptv.binding.image_processing import preprocess_image
import numpy as np, os
import tempfile

class Test_image_processing(unittest.TestCase):

    def setUp(self):
        self.input_img = np.array([[ 0, 0, 0, 0, 0],
                               [ 0, 255, 255, 255, 0],
                               [ 0, 255, 255, 255, 0],
                               [ 0, 255, 255, 255, 0],
                               [ 0, 0, 0, 0, 0]], dtype=np.uint8)
        self.filter_hp = 0
        self.control = ControlParams(4)
        self.control.set_image_size((5, 5))

    def test_arguments(self):
        with self.assertRaises(ValueError):
            preprocess_image(self.input_img, self.filter_hp, self.control,
                             lowpass_dim=1, output_img=np.empty((5, 4), dtype=np.uint8))

        with self.assertRaises(ValueError):
            preprocess_image(self.input_img.astype(np.float32), self.filter_hp, self.control,
                             lowpass_dim=1)

        with self.assertRaises(ValueError):
            # 3d output
            preprocess_image(self.input_img, self.filter_hp, self.control,
                             lowpass_dim=1, output_img=np.empty((5, 5, 5), dtype=np.uint8))

        # Test filter_hp=2 with filter_file=None
        with self.assertRaises(Exception):
            preprocess_image(self.input_img, 2, self.control, filter_file=None)

        # Test filter_hp=2 with valid filter_file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("0.1 0.1 0.1\n0.1 0.2 0.1\n0.1 0.1 0.1")
            filter_file = f.name

        try:
            # This should work now
            result = preprocess_image(self.input_img, 2, self.control, filter_file=filter_file)
            self.assertIsNotNone(result)
        finally:
            os.unlink(filter_file)

    def test_preprocess_image(self):
        correct_res = np.array([[ 0, 0, 0, 0, 0],
                                [ 0, 142, 85, 142, 0],
                                [ 0, 85, 0, 85, 0],
                                [ 0, 142, 85, 142, 0],
                                [ 0, 0, 0, 0, 0]],
                               dtype=np.uint8)

        res = preprocess_image(self.input_img,
                               self.filter_hp,
                               self.control,
                               lowpass_dim=1,
                               filter_file=None,
                               output_img=None)

        np.testing.assert_array_equal(res, correct_res)

if __name__ == "__main__":
    unittest.main()
