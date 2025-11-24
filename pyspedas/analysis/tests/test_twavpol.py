"""Tests of twavpol functions."""

import os
import logging
import unittest
import numpy as np
from numpy.testing import assert_allclose
import pyspedas
from pyspedas import get_data, tplot, tplot_rename, tplot_copy, twavpol
from pyspedas.utilities.config_testing import TESTING_CONFIG, test_data_download_file

# Whether to display plots during testing
global_display = TESTING_CONFIG["global_display"]
# Directory to save testing output files
output_dir = TESTING_CONFIG["local_testing_dir"]
# Ensure output directory exists
analysis_dir = "analysis_tools"
save_dir = os.path.join(output_dir, analysis_dir)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
# Directory with IDL SPEDAS validation files
validation_dir = TESTING_CONFIG["remote_validation_dir"]


class TwavpolDataValidation(unittest.TestCase):
    """Compares cotrans results between Python and IDL"""

    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The SPEDAS script that creates the file: general/tools/python_validate/python_wavpol_validate.pro
        """
        # Testing tolerance
        cls.tol = 1e-10

        # Load IDL savefile
        filename = test_data_download_file(
            validation_dir, analysis_dir, "thc_twavpol_validate.tplot", save_dir
        )
        if not filename:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        pyspedas.del_data("*")
        # pyspedas.cdf_to_tplot(filename)
        pyspedas.tplot_restore(filename)
        pyspedas.tplot_names()
        # pyspedas.tplot('thc_scf_fac')
        # pyspedas.tplot('thc_scf_fac_powspec')
        # pyspedas.tplot('thc_scf_fac')
        cls.thc_scf_fac = pyspedas.get_data("thc_scf_fac")
        cls.thc_scf_fac_attr = pyspedas.get_data("thc_scf_fac", metadata=True)
        cls.thc_scf_fac_powspec = pyspedas.get_data("thc_scf_fac_powspec")
        cls.thc_scf_fac_powspec_attr = pyspedas.get_data(
            "thc_scf_fac_powspec", metadata=True
        )
        cls.thc_scf_fac_degpol = pyspedas.get_data("thc_scf_fac_degpol")
        cls.thc_scf_fac_waveangle = pyspedas.get_data("thc_scf_fac_waveangle")
        cls.thc_scf_fac_elliptict = pyspedas.get_data("thc_scf_fac_elliptict")
        cls.thc_scf_fac_helict = pyspedas.get_data("thc_scf_fac_helict")
        cls.thc_scf_fac_pspec3 = pyspedas.get_data("thc_scf_fac_pspec3")

        tplot_copy("thc_scf_fac", "idl_thc_scf_fac")
        tplot_rename("thc_scf_fac_powspec", "idl_thc_scf_fac_powspec")
        tplot_rename("thc_scf_fac_degpol", "idl_thc_scf_fac_degpol")
        tplot_rename("thc_scf_fac_waveangle", "idl_thc_scf_fac_waveangle")
        tplot_rename("thc_scf_fac_elliptict", "idl_thc_scf_fac_elliptict")
        tplot_rename("thc_scf_fac_helict", "idl_thc_scf_fac_helict")
        tplot_rename("thc_scf_fac_pspec3", "idl_thc_scf_fac_pspec3")

        twavpol("thc_scf_fac")

    def setUp(self):
        """We need to clean tplot variables before each run"""
        # pyspedas.del_data('*')

    def test_multiple_twavpol_call(self):
        """Validate twavpol power spectrum output between two calls with the same input"""

        twavpol("thc_scf_fac")
        before_py_powspec = get_data("thc_scf_fac_powspec")
        twavpol("thc_scf_fac")
        after_py_powspec = get_data("thc_scf_fac_powspec")
        assert_allclose(before_py_powspec.y, after_py_powspec.y)
        logging.info(
            "nanmin/nanmax of powspec: %f %f ",
            np.nanmin(after_py_powspec.y),
            np.nanmax(after_py_powspec.y),
        )
        assert_allclose(
            after_py_powspec.times, self.thc_scf_fac_powspec.times, atol=1.0e-06
        )
        assert_allclose(
            after_py_powspec.y, self.thc_scf_fac_powspec.y, atol=1.0e-06, rtol=1.0e-06
        )
        local_png = os.path.join(save_dir, "multiple_twavpol.png")
        tplot(
            ["thc_scf_fac_powspec", "idl_thc_scf_fac_powspec"],
            display=global_display,
            save_png=local_png,
        )

    def test_powspec(self):
        """Validate twavpol power spectrum output"""

        py_powspec = get_data("thc_scf_fac_powspec")
        logging.info(
            "nanmin/nanmax of powspec: %f %f ",
            np.nanmin(py_powspec.y),
            np.nanmax(py_powspec.y),
        )
        assert_allclose(py_powspec.times, self.thc_scf_fac_powspec.times, atol=1.0e-06)
        assert_allclose(
            py_powspec.y, self.thc_scf_fac_powspec.y, atol=1.0e-06, rtol=1.0e-06
        )
        local_png = os.path.join(save_dir, "powspec.png")
        tplot(
            ["thc_scf_fac_powspec", "idl_thc_scf_fac_powspec"],
            display=global_display,
            save_png=local_png,
        )

    def test_degpol(self):
        """Validate twavpol degpol output"""

        py_degpol = pyspedas.get_data("thc_scf_fac_degpol")
        logging.info(
            "nanmin/nanmax of degpol: %f %f ",
            np.nanmin(py_degpol.y),
            np.nanmax(py_degpol.y),
        )
        assert_allclose(py_degpol.times, self.thc_scf_fac_degpol.times, atol=1.0e-06)
        assert_allclose(
            py_degpol.y, self.thc_scf_fac_degpol.y, atol=1.0e-06, rtol=1.0e-06
        )
        local_png = os.path.join(save_dir, "degpol.png")
        tplot(
            ["thc_scf_fac_degpol", "idl_thc_scf_fac_degpol"],
            display=global_display,
            save_png=local_png,
        )

    def test_waveangle(self):
        """Validate twavpol waveangle output"""

        py_waveangle = pyspedas.get_data("thc_scf_fac_waveangle")
        logging.info(
            "nanmin/nanmax of waveangle: %f %f ",
            np.nanmin(py_waveangle.y),
            np.nanmax(py_waveangle.y),
        )
        assert_allclose(
            py_waveangle.times, self.thc_scf_fac_waveangle.times, atol=1.0e-05
        )
        assert_allclose(
            py_waveangle.y, self.thc_scf_fac_waveangle.y, atol=1.0e-05, rtol=1.0e-06
        )
        local_png = os.path.join(save_dir, "waveangle.png")
        tplot(
            ["thc_scf_fac_waveangle", "idl_thc_scf_fac_waveangle"],
            display=global_display,
            save_png=local_png,
        )

    def test_elliptict(self):
        """Validate twavpol elliptict output"""

        py_elliptict = pyspedas.get_data("thc_scf_fac_elliptict")
        logging.info(
            "nanmin/nanmax of elliptict: %f %f ",
            np.nanmin(py_elliptict.y),
            np.nanmax(py_elliptict.y),
        )
        assert_allclose(
            py_elliptict.times, self.thc_scf_fac_elliptict.times, atol=1.0e-06
        )
        assert_allclose(
            py_elliptict.y, self.thc_scf_fac_elliptict.y, atol=1.0e-06, rtol=1.0e-06
        )
        local_png = os.path.join(save_dir, "elliptict.png")
        tplot(
            ["thc_scf_fac_elliptict", "idl_thc_scf_fac_elliptict"],
            display=global_display,
            save_png=local_png,
        )

    def test_helict(self):
        """Validate twavpol helict output"""

        py_helict = pyspedas.get_data("thc_scf_fac_helict")
        logging.info(
            "nanmin/nanmax of helict: %f %f ",
            np.nanmin(py_helict.y),
            np.nanmax(py_helict.y),
        )
        assert_allclose(py_helict.times, self.thc_scf_fac_helict.times, atol=1.0e-06)
        assert_allclose(
            py_helict.y, self.thc_scf_fac_helict.y, atol=1.0e-06, rtol=1.0e-06
        )
        local_png = os.path.join(save_dir, "helict.png")
        tplot(
            ["thc_scf_fac_helict", "idl_thc_scf_fac_helict"],
            display=global_display,
            save_png=local_png,
        )

    def test_pspec3(self):
        """Validate twavpol pspec3 output"""

        py_pspec3 = pyspedas.get_data("thc_scf_fac_pspec3")
        logging.info(
            "nanmin/nanmax of pspec3: %f %f ",
            np.nanmin(py_pspec3.y),
            np.nanmax(py_pspec3.y),
        )
        assert_allclose(py_pspec3.times, self.thc_scf_fac_pspec3.times, atol=1.0e-06)
        assert_allclose(
            py_pspec3.y, self.thc_scf_fac_pspec3.y, atol=1.0e-06, rtol=1.0e-06
        )
        local_png = os.path.join(save_dir, "pspec3.png")
        tplot(
            ["thc_scf_fac_pspec3", "idl_thc_scf_fac_pspec3", "thc_scf_fac_pspec3*"],
            display=global_display,
            save_png=local_png,
        )

    @unittest.skip("skipping, work in progress")
    def test_mms_scm(self):
        # achDate = ['2015-09-19/10:07:00', '2015-09-19/10:07:12']
        achDate = ["2015-09-19/10:06:00", "2015-09-19/10:09:00"]
        SCMbrst_vars = pyspedas.projects.mms.scm(
            probe=4, data_rate="brst", trange=achDate, time_clip=True
        )
        logging.info("SCM burst variables: %s", SCMbrst_vars)
        # SCM burst sampling rate = 8192/inputs as done in example tutorial
        nopfft_input = 8192  # number of points for FFT
        steplength_input = (
            nopfft_input / 2
        )  # number of points for shifting between 2 FFT
        bin_freq_input = 3  # number of bins for frequency averaging
        pyspedas.twavpol(
            "mms4_scm_acb_gse_scb_brst_l2",
            nopfft=nopfft_input,
            steplength=steplength_input,
            bin_freq=bin_freq_input,
        )

        local_png = os.path.join(save_dir, "mms_scm_burst.png")
        tplot(
            [
                "mms4*scb_brst_l2",
                "mms4*powspec*",
                "mms4*degpol*",
                "mms4*elliptc",
                "mms4*helict",
                "mms4*angle",
            ],
            display=global_display,
            save_png=local_png,
        )


if __name__ == "__main__":
    unittest.main()
