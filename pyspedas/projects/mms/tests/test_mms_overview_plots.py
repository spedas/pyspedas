import unittest
import os
from pyspedas import mms_overview_plot
from pyspedas.config import CONFIG

global_display = CONFIG["testing"]["global_display"]
save_dir = os.path.join(CONFIG["testing"]["output_dir"], "mms")
os.makedirs(save_dir, exist_ok=True)


class TestMMSOverviewPlot(unittest.TestCase):
    def test_default_overview_plot(self):
        save_png = os.path.join(save_dir, "mms_default_overview")
        mms_overview_plot(display=global_display, save_png=save_png)
        self.assertTrue(os.path.exists(save_png + ".png"))


if __name__ == '__main__':
    unittest.main()
