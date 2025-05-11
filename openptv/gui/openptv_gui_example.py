# This is an example of how to use the interface in the calibration GUI
# filepath: openptv/calibration_gui.py (partial)

from openptv.factory import get_ptv_implementation

class CalibrationGUI:
    def __init__(self, prefer_c=True):
        # Get implementation based on availability
        self.ptv = get_ptv_implementation(prefer_c=prefer_c)
        
        # Other initialization...
        
    def _button_orient_fired(self):
        """Handle orientation button click"""
        # Same API regardless of implementation
        self.ptv.calibration_ori(
            self.cals[self.current_camera], 
            self.cal_points["pos"], 
            self.selected_points, 
            self.cpar
        )
        self.update_plots()
        
    def _button_fine_orient_fired(self):
        """Handle fine orientation button click"""
        # Same API regardless of implementation
        residuals, targ_ix, err_est = self.ptv.full_calibration(
            self.cals[self.current_camera],
            self.cal_points["pos"],
            self.selected_points,
            self.cpar,
            self.flags
        )
        self.update_plots()
        self.update_results(residuals, err_est)