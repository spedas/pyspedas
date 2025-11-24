import unittest
import numpy as np
from numpy.testing import assert_array_equal
from pyspedas import hapi, data_exists, del_data
from pyspedas.hapi_tools.replace_fillvals import replace_fillvals


class HAPITests(unittest.TestCase):
    def test_replace_fillvals(self):
        da1_dbl = np.array([1.0, 2.0, 3.0, 4.0])
        fv1_dbl = 3.0
        replace_fillvals(da1_dbl, fv1_dbl, "da1_dbl_scalarfill", "double")
        assert_array_equal(da1_dbl, [1.0, 2.0, np.nan, 4.0])
        da2_dbl = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 2.0]])
        fv2_dbl = [1.0, 2.0]
        replace_fillvals(da2_dbl, fv2_dbl, "da2_dbl_arrayfill", "double")
        assert_array_equal(
            da2_dbl, np.array([[np.nan, np.nan], [3.0, 4.0], [5.0, 6.0], [7.0, np.nan]])
        )
        # Repeat after replacement, should be nothing to replace, and output array same as before
        fv2_dbl = [1.0, 2.0]
        replace_fillvals(da2_dbl, fv2_dbl, "da2_dbl_arrayfill", "double")
        assert_array_equal(
            da2_dbl, np.array([[np.nan, np.nan], [3.0, 4.0], [5.0, 6.0], [7.0, np.nan]])
        )
        da2_int = np.array([[0, 1], [2, 3], [4, 5], [6, 2]])
        da2_fvint = 2
        replace_fillvals(da2_int, da2_fvint, "da2_int_scalarfill", "integer")
        assert_array_equal(da2_int, np.array([[0, 1], [0, 3], [4, 5], [6, 0]]))

    def test_print_servers(self):
        with self.assertLogs(level="ERROR") as log:
            hapi(trange=["2003-10-20", "2003-11-30"])
            self.assertIn(
                "No server specified; example servers include:", log.output[0]
            )

    def test_return_catalog(self):
        id_list = hapi(
            server="https://cdaweb.gsfc.nasa.gov/hapi", catalog=True, quiet=True
        )
        self.assertTrue("MMS1_EDI_BRST_L2_EFIELD" in id_list)

    def test_dataset_not_specified(self):
        # dataset not specified
        with self.assertLogs(level="ERROR") as log:
            h_vars = hapi(
                trange=["2003-10-20", "2003-11-30"],
                server="https://cdaweb.gsfc.nasa.gov/hapi",
            )
            self.assertIsNone(h_vars)
            self.assertIn(
                "Error, no dataset specified; please see the catalog for a list of available data sets.",
                log.output[0],
            )

    def test_trange_not_specified(self):
        # trange not specified
        with self.assertLogs(level="ERROR") as log:
            h_vars = hapi(
                dataset="OMNI_HRO2_1MIN", server="https://cdaweb.gsfc.nasa.gov/hapi"
            )
            self.assertIsNone(h_vars)
            self.assertIn("Error, no trange specified", log.output[0])

    def test_cdaweb_mms_spec(self):
        h_vars = hapi(
            trange=["2019-10-16", "2019-10-17"],
            server="https://cdaweb.gsfc.nasa.gov/hapi",
            dataset="MMS4_EDP_SRVY_L2_HFESP",
        )
        self.assertTrue(h_vars)

    def test_cdaweb_omni(self):
        del_data()
        h_vars = hapi(
            trange=["2003-10-20", "2003-11-30"],
            server="https://cdaweb.gsfc.nasa.gov/hapi",
            dataset="OMNI_HRO2_1MIN",
        )
        self.assertTrue(h_vars)
        self.assertTrue(data_exists("BX_GSE"))
        self.assertTrue(data_exists("BY_GSE"))
        self.assertTrue(data_exists("BZ_GSE"))

    def test_string_time(self):
        del_data()
        server = "https://supermag.jhuapl.edu/hapi"
        dataset = "ttb/baseline_all/PT1M/XYZ"
        start = "2020-05-10T00:00Z"
        stop = "2020-05-14T00:00Z"
        parameters = ""
        param_list = hapi(
            trange=[start, stop], server=server, dataset=dataset, parameters=parameters
        )
        self.assertTrue("mlt" in param_list)
        self.assertTrue(data_exists("mlt"))


if __name__ == "__main__":
    unittest.main()
