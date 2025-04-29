"""
Unit Tests for lmn transformations.
"""

import numpy as np
import unittest
import pyspedas
from pytplot import del_data, get_data, tnames, tplot, data_exists, tplot_restore
from pyspedas.projects.omni.omni_solarwind_load import omni_solarwind_load
from pyspedas.cotrans_tools.lmn_matrix_make import lmn_matrix_make
from pyspedas.projects.themis import fgm, state
from pyspedas.utilities.download import download


def _test_compare(tname1, tname2, center=False, approximate=False):
    """Compare two tplot variables."""
    try:
        data1 = get_data(tname1)
        t1 = data1.times
        y1 = data1.y
        data2 = get_data(tname2)
        t2 = data2.times
        y2 = data2.y

        if center:
            # Cut out the 10% of the edges of the data
            edge_cut = int(len(t1) * 0.1) - 1
            if edge_cut > 0 and 2 * edge_cut < len(t1):
                t1 = t1[edge_cut:-edge_cut]
                y1 = y1[edge_cut:-edge_cut]
                # find min and max of t1
                t1_min = np.min(t1)
                t1_max = np.max(t1)
                # for t2, find the indices of the values that are within t1_min and t1_max
                t2_indices = np.where((t2 >= t1_min) & (t2 <= t1_max))[0]
                t2 = t2[t2_indices]
                y2 = y2[t2_indices]

        do_match1 = np.allclose(t1, t2, rtol=1e-5, atol=1e-8)
        if approximate:
            do_match2 = np.allclose(y1, y2, rtol=1e-2, atol=1e-2)
        else:
            do_match2 = np.allclose(y1, y2, rtol=1e-5, atol=1e-8)
        do_match = do_match1 and do_match2
        if not do_match:
            print(f"Data for {tname1} and {tname2} do not match.")
            print(f"Data1: {data1.y}")
            print(f"Data2: {data2.y}")
    except Exception as e:
        print(f"Error comparing {tname1} and {tname2}: {e}")
        do_match = False
    return do_match


class TestLMNTransform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Find the test data files to restore."""
        # Set to true when running locally
        localfile = False  
        # Set to your local directory, if running locally
        localdir = "C:/work/idl_working/"  
        
        # Github files
        remote_server = "https://github.com/spedas/test_data/raw/refs/heads/main/"
        filename_solarwind = "solarwind_python_validate.tplot"
        filename_lmn = "lmn_python_validate.tplot"

        if localfile:
            cls.filename_sw = localdir + filename_solarwind
            cls.filename_lmn = localdir + filename_lmn
        else:
            remote_name = "cotrans_tools/" + filename_solarwind
            datafile = download(
                remote_file=remote_name,
                remote_path=remote_server,
                local_path="testdata",
                no_download=False,
            )
            if not datafile:
                # Skip tests
                raise unittest.SkipTest(
                    "Cannot download solarwind data validation file"
                )

            cls.filename_sw = datafile[0]

            remote_name = "cotrans_tools/" + filename_lmn
            datafile1 = download(
                remote_file=remote_name,
                remote_path=remote_server,
                local_path="testdata",
                no_download=False,
            )
            if not datafile1:
                # Skip tests
                raise unittest.SkipTest("Cannot download LMN data validation file")

            cls.filename_lmn = datafile1[0]

    # @unittest.skip("Skipping LMN tests")
    def test_lmn_1omni(self):
        """Test of OMNI variables."""
        # Load IDL variables from the test file
        del_data("*")
        tplot_restore(self.filename_sw)

        # Check if the IDL variables have been loaded
        tn = tnames()
        print(tn)
        idl_bz_def = "omni_BZ_idl_default"
        idl_p_def = "omni_P_idl_default"
        idl_bz_hro = "omni_BZ_idl_2020"
        idl_p_hro = "omni_P_idl_2020"
        idl_bz_hro2 = "omni_BZ_idl_2021"
        idl_p_hro2 = "omni_P_idl_2021"
        omni_names = [
            idl_bz_def,
            idl_p_def,
            idl_bz_hro,
            idl_p_hro,
            idl_bz_hro2,
            idl_p_hro2,
        ]
        for name in omni_names:
            self.assertTrue(data_exists(name), f"Data variable {name} does not exist.")

        # Load pyspedas data (default values) and compare
        # OMNI default values (constants)
        trange = ["2050-01-01", "2050-01-01 23:59:59"]
        omni_solarwind_load(trange=trange, level="hro", suffix="_py_default")
        t1 = _test_compare(idl_bz_def, "omni_solarwind_BZ_py_default")
        self.assertTrue(t1, f"Data for default BZ values do not match.")
        t2 = _test_compare(idl_p_def, "omni_solarwind_P_py_default")
        self.assertTrue(t2, f"Data for default P values do not match.")

        # OMNI HRO
        trange = ["2020-01-01", "2020-01-01 23:59:59"]
        omni_solarwind_load(trange=trange, level="hro", suffix="_py_2020")
        t3 = _test_compare(idl_bz_hro, "omni_solarwind_BZ_py_2020")
        self.assertTrue(t3, f"Data for 2020 HRO BZ values do not match.")
        t4 = _test_compare(idl_p_hro, "omni_solarwind_P_py_2020")
        self.assertTrue(t4, f"Data for 2020 HRO P values do not match.")

        # OMNI HRO2
        trange = ["2021-01-01", "2021-01-01 06:00:00"]
        omni_solarwind_load(trange=trange, level="hro2", suffix="_py_2021")
        t5 = _test_compare(idl_bz_hro2, "omni_solarwind_BZ_py_2021")
        self.assertTrue(t5, f"Data for 2021 HRO2 BZ values do not match.")
        t6 = _test_compare(idl_p_hro2, "omni_solarwind_P_py_2021")
        self.assertTrue(t6, f"Data for 2021 HRO2 P values do not match.")

    # @unittest.skip("Skipping LMN tests")
    def test_lmn_2lmn(self):
        """Test of LMN transform."""
        # Load LMN data
        del_data("*")
        tplot_restore(self.filename_lmn)

        # Check if the IDL LMN variables exist in tplot
        idl_pos = "tha_state_pos_gsm_idl"
        idl_b = "tha_fgl_gsm_idl"
        idl_hro = "tha_fgl_gsm_lmn_mat_hro_idl"
        idl_p = "OMNI_solarwind_P_idl"
        idl_bz = "OMNI_solarwind_BZ_idl"
        idl_names = [idl_pos, idl_b, idl_hro, idl_p, idl_bz]
        for name in idl_names:
            self.assertTrue(data_exists(name), f"Data variable does not exist: " + name)

        # Optionally plot the IDL data
        # tplot(idl_names)

        # Load pyspedas data
        trange = ["2022-01-01", "2022-01-01 06:00:00"]
        fgm(
            probe="a",
            level="l2",
            trange=trange,
            suffix="_py",
            time_clip=True,
            coord="gsm",
            get_support_data=True,
        )
        state(
            probe="a",
            trange=trange,
            suffix="_py",
            time_clip=True,
            get_support_data=True,
        )
        py_pos = "tha_pos_gsm_py"
        py_pos_i = py_pos + "_interpol"
        py_b = "tha_fgl_gsm_py"
        py_hro = "tha_fgl_gsm_lmn_mat_hro_py"
        py_p = "omni_solarwind_P"
        py_p_i = py_p + "_interpol"
        py_bz = "omni_solarwind_BZ"
        py_bz_i = py_bz + "_interpol"
        py_names = [py_pos, py_pos_i, py_b, py_hro, py_p, py_p_i, py_bz, py_bz_i]

        # Compute LMN
        lmn_matrix_make(py_pos, py_b, trange=trange, newname=py_hro)

        # Verify rotation matrix input and output coordinates
        in_coords, out_coords = pyspedas.rotmat_get_coords(py_hro)
        self.assertEqual(in_coords.upper(), "GSM")
        self.assertEqual(out_coords.upper(), "LMN")

        for name in py_names:
            self.assertTrue(data_exists(name), f"Data variable does not exist: " + name)
        # tplot(py_names)

        # Verify that position and B field as the same as in IDL
        t1 = _test_compare(idl_b, py_b, center=True)
        self.assertTrue(t1, f"B field data does not match.")
        t2 = _test_compare(idl_pos, py_pos, center=True)
        self.assertTrue(t2, f"Position data does not match.")

        # Verify that the interpolated data matches
        t3 = _test_compare(idl_p, py_p, center=True)
        self.assertTrue(t3, f"OMNI P data does not match.")
        t4 = _test_compare(idl_bz, py_bz, center=True)
        self.assertTrue(t4, f"OMNI Bz data does not match.")

        # Verify that the LMN matrices match
        t5 = _test_compare(idl_hro, py_hro, approximate=True)
        self.assertTrue(t5, f"LMN matrices do not match for HRO data.")
        
        print("test_lmn finished.")


if __name__ == "__main__":
    unittest.main()
