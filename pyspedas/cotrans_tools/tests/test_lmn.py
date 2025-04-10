"""
Unit Tests for lmn_matrix_make.
"""

import unittest
import numpy as np
from pytplot import tnames, get_data, del_data, time_string
from pyspedas import tplot_restore, download
from pyspedas.projects.themis import fgm, state
from pyspedas.cotrans_tools.lmn_matrix_make import lmn_matrix_make


class TestLmnMatrixMake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the IDL data from savefile
        del_data("*")
        remote_server = "https://github.com/spedas/test_data/raw/refs/heads/main/"
        remote_name = "cotrans_tools/lmn_python_validate.tplot"

        #remote_server = "https://github.com/nickssl/pyspedas_vs_spedas/tree/main/"
        #remote_name = "pyspedas_vs_spedas/cotrans/data_files/lmn_python_validate.tplot"
        datafile = download(
            remote_file=remote_name,
            remote_path=remote_server,
            local_path="testdata",
            no_download=True,
        )
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        filename = datafile[0]
        filename = "C:/work/github/pyspedas/testdata/cotrans_tools/load_test.tplot"
        tplot_restore(filename)

        # Load IDL data from the savefile into test variables
        pos = "tha_state_pos"
        b = "tha_fgl_gsm"
        out = "tha_fgl_gsm_lmn_mat"
        idl_vars = [pos + "_tclip", b + "_tclip", out + "_tclip"]

        # Save IDL test variables
        cls.idl_vars = idl_vars
        cls.idl_pos = get_data(idl_vars[0])
        cls.idl_b = get_data(idl_vars[1])
        cls.idl_out = get_data(idl_vars[2])

        # Load python data using pyspedas
        pos = "tha_pos_gsm"
        trange = ["2022-01-01", "2022-01-02"]
        #pyth = state(trange=trange, probe="a", get_support_data=True)
        #bpyth = fgm(trange=trange, probe="a", get_support_data=True)
        #lmn_matrix_make(pos, b, newname=out, loadsolarwind=True, swlevel="hro")

        # Save python test variables
        python_vars = [pos, b, out]
        cls.python_vars = python_vars
        cls.python_pos = get_data(python_vars[0])
        cls.python_b = get_data(python_vars[1])
        cls.python_out = get_data(python_vars[2])

        return


    def test_lmn__basic(self):
        """Verify that the data was loaded"""

        # Verify that the IDL data and python data was loaded
        tpnames = tnames()
        self.assertTrue(len(self.idl_vars) == len(self.python_vars))

        # IDL vars
        for var in self.idl_vars:
            self.assertTrue(var in tpnames)
        # Python vars
        for var in self.python_vars:
            self.assertTrue(var in tpnames)

    @unittest.skip("This test is skipped.")
    def test_lmn_compare(self):
        """Compare the output of the IDL and Python versions of the LMN matrix"""

        # Find the IDL out values at the test times
        idl_out_times = np.array(self.idl_out.times)
        idl_out_b = np.array(self.idl_out.y)
        step = int(len(idl_out_times) / 1000)
        test_times = idl_out_times[::step]
        idl_b_indices = np.searchsorted(idl_out_times, test_times, side="left")
        idl_out_compare = idl_out_b[idl_b_indices]
        
        print("IDL b field indices: ", idl_b_indices)
        print("IDL b field times compared: ", time_string(test_times))
        print("IDL b field number of points: ", len(idl_out_b))
        print("IDL b field number of points compared: ", len(idl_out_compare))
        print("IDL b field:", idl_out_compare)

        # Find the python out values at the test times
        python_out_times = np.array(self.python_out.times)
        python_out_b = np.array(self.python_out.y)
        python_b_indices = np.searchsorted(python_out_times, test_times, side="left")
        python_out_compare = python_out_b[python_b_indices]

        print("Python b field indices: ", python_b_indices)
        print("Python b field times compared: ", time_string(python_out_times[python_b_indices]))
        print("Python b field number of points: ", len(python_out_b))
        print("Python b field number of points compared: ", len(python_out_compare))
        print("Python b field:", python_out_compare)

        # Compare the IDL and python out values
        tol = 0.5  # Set tolerance        
        are_close = np.allclose(idl_out_compare, python_out_compare, rtol=tol)

        if not are_close:
            # Print the IDL and python out values for debugging
            print("IDL out values:")
            print(idl_out_compare)
            print("Python out values:")
            print(python_out_compare)
            print("Difference:")
            print(idl_out_compare - python_out_compare)

        print("IDL b field number of points: ", len(idl_out_b))
        print("IDL b field number of points compared: ", len(idl_out_compare))
        print("Python b field number of points: ", len(python_out_b))
        print("Python b field number of points compared: ", len(python_out_compare))
        print(self.idl_vars)
        print(self.python_vars)

        self.assertTrue(are_close)


if __name__ == "__main__":
    unittest.main()
