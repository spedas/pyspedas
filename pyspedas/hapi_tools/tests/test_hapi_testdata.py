"""End-to-end HAPI specification coverage using the public TestData servers.

Run with python -m pyspedas.hapi_tools.tests.test_hapi_testdata.
"""
import unittest
from unittest.mock import patch

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from hapiclient import hapi as client
from pyspedas import del_data, get_data, hapi, tplot
from pyspedas.hapi_tools.replace_fillvals import replace_fillvals

VERSIONS = ("2.0", "2.1", "3.0", "3.1", "3.2", "3.3")


class HAPITestDataTests(unittest.TestCase):
    def tearDown(self):
        del_data()
        plt.close("all")

    def test_single_record_and_empty_response(self):
        metadata = {"parameters": [
            {"name": "Time", "type": "isotime"},
            {"name": "scalar", "type": "double"},
            {"name": "matrix", "type": "double", "size": [2, 3]},
        ]}
        raw = np.zeros(1, dtype=[("Time", "S24"), ("scalar", "f8"),
                                 ("matrix", "f8", (2, 3))])
        raw["Time"] = b"1970-01-01T00:00:00Z"
        raw["matrix"] = np.arange(6).reshape(2, 3)
        with patch("pyspedas.hapi_tools.hapi.load_hapi", return_value=(raw, metadata)):
            self.assertEqual(hapi(server="test", dataset="test", trange=[0, 1]),
                             ["scalar", "matrix"])
        self.assertEqual(get_data("scalar").y.shape, (1,))
        np.testing.assert_array_equal(get_data("matrix").y, raw["matrix"])
        with patch("pyspedas.hapi_tools.hapi.load_hapi", return_value=(raw[:0], metadata)):
            self.assertEqual(hapi(server="test", dataset="test", trange=[0, 1]), [])

    def test_conversion(self):
        for version in VERSIONS:
            server = f"https://hapi-server.org/servers/TestData{version}/hapi"
            catalog = client(server, logging=False)
            for entry in catalog["catalog"]:
                dataset = entry["id"]
                with self.subTest(version=version, dataset=dataset):
                    info = client(server, dataset, logging=False)
                    trange = [info.get("sampleStartDate", "1970-01-01T00:00:00"),
                              info.get("sampleStopDate", "1970-01-01T00:01:00")]
                    raw, meta = client(server, dataset, "", *trange, logging=False)
                    del_data()
                    names = hapi(server=server, dataset=dataset, trange=trange)
                    self.assertEqual(names, [p["name"] for p in meta["parameters"][1:]])
                    for index, param in enumerate(meta["parameters"][1:], 1):
                        with self.subTest(parameter=param["name"]):
                            actual = get_data(param["name"]).y
                            expected = np.array(raw[raw.dtype.names[index]], copy=True)
                            if param["type"] in ("string", "isotime"):
                                if expected.dtype.kind == "S":
                                    expected = np.char.decode(expected, "utf-8")
                                else:
                                    expected = expected.astype(str)
                            else:
                                if param["type"] == "double":
                                    expected = expected.astype(float)
                                if param.get("fill") is not None:
                                    replace_fillvals(expected, param["fill"], param["name"], param["type"])
                            np.testing.assert_array_equal(actual, expected)

    def test_plotting(self):
        for version in VERSIONS:
            server = f"https://hapi-server.org/servers/TestData{version}/hapi"
            for entry in client(server, logging=False)["catalog"]:
                dataset = entry["id"]
                info = client(server, dataset, logging=False)
                trange = [info.get("sampleStartDate", "1970-01-01T00:00:00"),
                          info.get("sampleStopDate", "1970-01-01T00:01:00")]
                del_data()
                with self.subTest(version=version, dataset=dataset):
                    names = hapi(server=server, dataset=dataset, trange=trange)
                    for name in names:
                        with self.subTest(parameter=name):
                            try:
                                fig, axes = tplot([name], display=False, return_plot_objects=True)
                                plot_axes = np.asarray(axes).reshape(-1)
                                self.assertGreater(len(plot_axes), 0)
                                self.assertTrue(any(ax.lines or ax.collections for ax in plot_axes))
                            finally:
                                plt.close("all")


if __name__ == "__main__":
    unittest.main()
