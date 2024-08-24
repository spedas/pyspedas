import unittest
import importlib.resources

from pyspedas.projects.elfin.epd.calibration_l1 import read_epde_calibration_data

EXPECTED_EPDE_CAL_DATA = [
    {'ch_efficiencies': [0.74, 0.8, 0.85, 0.86, 0.87, 0.87, 0.87, 0.87, 0.82, 0.8, 0.75, 0.6, 0.5, 0.45, 0.25, 0.05],
        'date': 1262390400.0,
        'ebins': [50.0,
                80.0,
                120.0,
                160.0,
                210.0,
                270.0,
                345.0,
                430.0,
                630.0,
                900.0,
                1300.0,
                1800.0,
                2500.0,
                3350.0,
                4150.0,
                5800.0],
        'gf': 0.15,
        'overaccumulation_factors': [1.0, 2.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.15],
        'thresh_factors': [0.0325,
                        0.208,
                        0.156,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13,
                        0.13]},
    {'ch_efficiencies': [0.74, 0.8, 0.85, 0.86, 0.87, 0.87, 0.87, 0.87, 0.82, 0.8, 0.75, 0.6, 0.5, 0.45, 0.25, 0.05],
        'date': 1296705600.0,
        'ebins': [50.0,
                80.0,
                120.0,
                160.0,
                210.0,
                270.0,
                345.0,
                430.0,
                630.0,
                900.0,
                1300.0,
                1800.0,
                2500.0,
                3350.0,
                4150.0,
                5800.0],
        'gf': 3.14,
        'overaccumulation_factors': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.9, 1.0],
        'thresh_factors': [0.13, 0.208, 0.156, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13]}
]

class EPDCalibrationTestCases(unittest.TestCase):

    def test_read_epde_calibration_data(self):
        with importlib.resources.path("pyspedas.projects.elfin.tests", "test_epde_cal_data.txt") as test_file_path:
            self.assertListEqual(read_epde_calibration_data(test_file_path), EXPECTED_EPDE_CAL_DATA)

if __name__ == '__main__':
    unittest.main()
