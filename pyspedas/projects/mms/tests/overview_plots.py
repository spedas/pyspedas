import unittest
import os
from pyspedas import mms_overview_plot

global_display = False  # Set to False for Github testing

class TestMMSOverviewPlot(unittest.TestCase):
    def test_default_overview_plot(self):
        save_png='mms_default_overview'
        mms_overview_plot(display=global_display,save_png=save_png)
        self.assertTrue(os.path.exists(save_png + '.png'))

if __name__ == '__main__':
    unittest.main()
