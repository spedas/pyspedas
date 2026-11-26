"""Tests for pyspedas.tplot_tools.importers.cdf_to_tplot."""

import os
import tempfile
import unittest

import cdflib
import numpy as np
from cdflib.cdfwrite import CDF as CDFWriter

import pyspedas


class CDFToTplotTestCases(unittest.TestCase):
    """Tests for the CDF importer."""

    def setUp(self):
        pyspedas.del_data("*")

    def tearDown(self):
        pyspedas.del_data("*")

    def _write_centered_cdf(self, path):
        """Write a minimal CDF whose DEPEND_0 asks for centered times.

        3 TT2000 records, DELTA_PLUS_VAR = 2 s and DELTA_MINUS_VAR = 0 s, so
        centered times are 1 s later. Two data variables 'a' and 'b' share the
        same Epoch.
        """
        start = cdflib.cdfepoch.compute_tt2000([2015, 10, 16, 8, 0, 0, 0, 0, 0])
        epoch = start + np.arange(3, dtype=np.int64) * 4_000_000_000
        cdf = CDFWriter(path, cdf_spec={"Majority": "Row_major"})
        cdf.write_globalattrs({"Project": {0: "center_measurement test"}})
        cdf.write_var(
            {
                "Variable": "Epoch",
                "Data_Type": 33,
                "Num_Elements": 1,
                "Rec_Vary": True,
                "Dim_Sizes": [],
            },
            var_attrs={
                "VAR_TYPE": "support_data",
                "DELTA_PLUS_VAR": "Epoch_plus",
                "DELTA_MINUS_VAR": "Epoch_minus",
            },
            var_data=epoch,
        )
        for name, seconds in (("Epoch_plus", 2.0), ("Epoch_minus", 0.0)):
            cdf.write_var(
                {
                    "Variable": name,
                    "Data_Type": 45,
                    "Num_Elements": 1,
                    "Rec_Vary": False,
                    "Dim_Sizes": [],
                },
                var_attrs={"VAR_TYPE": "support_data", "UNITS": "s"},
                var_data=np.array([seconds]),
            )
        for name in ("a", "b"):
            cdf.write_var(
                {
                    "Variable": name,
                    "Data_Type": 44,
                    "Num_Elements": 1,
                    "Rec_Vary": True,
                    "Dim_Sizes": [],
                },
                var_attrs={"VAR_TYPE": "data", "DEPEND_0": "Epoch"},
                var_data=np.arange(3.0),
            )
        cdf.close()
        return epoch

    def test_center_measurement_all_variables(self):
        """Regression test for spedas/pyspedas issue #1584.

        With center_measurement=True the shifted times were stored in the
        epoch cache but not assigned back to xdata, so the first variable
        read for each DEPEND_0 kept uncentered times and the result depended
        on the order the variables were loaded.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "center_measurement_test.cdf")
            epoch = self._write_centered_cdf(path)
            raw = np.array(cdflib.cdfepoch.to_datetime(epoch))
            for order in (["a", "b"], ["b", "a"]):
                pyspedas.del_data("*")
                pyspedas.cdf_to_tplot(path, varnames=order, center_measurement=True)
                for name in order:
                    times = np.asarray(pyspedas.get_data(name, dt=True).times)
                    np.testing.assert_array_equal(
                        times,
                        raw + np.timedelta64(1, "s"),
                        err_msg=f"varnames={order}: {name} timestamps should all shift by 1 s",
                    )


if __name__ == "__main__":
    unittest.main()
