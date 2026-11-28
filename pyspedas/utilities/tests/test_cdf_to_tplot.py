"""Tests for pyspedas.tplot_tools.importers.cdf_to_tplot."""

import importlib
import os
import tempfile
import unittest
from unittest.mock import patch

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

    def test_supported_cdflib_metadata_without_version_check(self):
        """Read real CDF metadata without inspecting cdflib's version string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "metadata.cdf")
            self._write_centered_cdf(path)
            # Version metadata is not needed to choose an API: the dependency
            # already requires cdflib >= 1.3.12. A non-string sentinel catches
            # accidental reintroduction of lexicographic version comparisons.
            with patch.object(cdflib, "__version__", object()):
                values = pyspedas.cdf_to_tplot(path, mastercdf=path, notplot=True)
            for name in ("a", "b"):
                np.testing.assert_array_equal(values[name]["y"], np.arange(3.0))

    def test_psp_rfs_supported_cdflib_metadata(self):
        """Select RFS variables from a real modern cdflib CDFInfo object."""
        rfs = importlib.import_module("pyspedas.projects.psp.rfs")
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "rfs.cdf")
            with CDFWriter(path) as cdf:
                for name in ("psp_fld_test", "unrelated"):
                    cdf.write_var(
                        {"Variable": name, "Data_Type": 45, "Num_Elements": 1,
                         "Rec_Vary": True, "Dim_Sizes": []},
                        var_data=np.array([1.0, 2.0]),
                    )
            with patch.object(cdflib, "__version__", object()):
                self.assertEqual(rfs.rfs_variables_to_load([path]), ["psp_fld_test"])
                self.assertEqual(rfs.rfs_variables_to_load([]), [])

    def test_erg_notplot_supported_cdflib_metadata(self):
        """Preserve ERG notplot attributes using the supported CDFInfo API."""
        erg = importlib.import_module("pyspedas.projects.erg.satellite.erg.load")
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "erg.cdf")
            self._write_centered_cdf(path)
            with patch.object(erg, "download", return_value=[path]), patch.object(
                cdflib, "__version__", object()
            ):
                values = erg.load(
                    notplot=True, prefix="erg_", suffix="_test",
                    remote_data_dir="https://example.invalid/erg/",
                    remote_data_layout="ergsc", pathformat="erg_%Y%m%d.cdf",
                )
            np.testing.assert_array_equal(values["erg_a_test"]["y"], np.arange(3.0))
            metadata = values["erg_a_test"]["CDF"]
            self.assertEqual(metadata["FILENAME"], [path])
            self.assertEqual(metadata["VATT"]["DEPEND_0"], "Epoch")
            self.assertEqual(metadata["GATT"]["Project"], ["center_measurement test"])

    def test_erg_induction_supported_cdflib_metadata(self):
        """Read calibration record counts through modern VDRInfo attributes."""
        induction = importlib.import_module(
            "pyspedas.projects.erg.ground.geomag.gmag_isee_induction"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "induction.cdf")
            with CDFWriter(path) as cdf:
                for name, dimensions, values in (
                    ("frequency", [], np.array([1.0, 2.0])),
                    ("sensitivity", [3], np.arange(6.0).reshape(2, 3)),
                    ("phase_difference", [3], np.arange(6.0).reshape(2, 3)),
                ):
                    cdf.write_var(
                        {"Variable": name, "Data_Type": 45, "Num_Elements": 1,
                         "Rec_Vary": True, "Dim_Sizes": dimensions},
                        var_data=values,
                    )
            name = "isee_induction_db_dt_msr"
            pyspedas.store_data(
                name, data={"x": [0.0, 1.0], "y": [[1., 2., 3.], [4., 5., 6.]]},
                attr_dict={"CDF": {"FILENAME": path}},
            )
            with patch.object(induction, "load", return_value=[name]), patch.object(
                cdflib, "__version__", object()
            ):
                result = induction.gmag_isee_induction(
                    site="msr", frequency_dependent=True, ror=False
                )["msr"]
            self.assertEqual(result["nfreq"], 2)
            np.testing.assert_array_equal(result["frequency"][:2], [1., 2.])
            np.testing.assert_array_equal(
                result["sensitivity"][:2], np.arange(6.0).reshape(2, 3)
            )

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
