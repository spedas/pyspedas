"""Offline tests using representative NOAA netCDF structures."""
import gzip
import importlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock

from netCDF4 import Dataset
import numpy as np
import pyspedas
from pyspedas.tplot_tools import get_data, del_data, time_double

loader = importlib.import_module("pyspedas.projects.swfo.load")


class TestSWFO(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config = patch.dict(loader.CONFIG, local_data_dir=self.tmp.name, no_download=False)
        self.config.start()
        self.addCleanup(self.config.stop)
        self.addCleanup(lambda: del_data("swfo_*"))
        self.start = time_double("2026-10-01")

    def fixture(self, instrument="MAG", level="l2", day="01", processing="03"):
        directory = Path(self.tmp.name) / f"SWFO/SOLAR-1/{instrument}/{instrument.lower()}-{level}/2026/10"
        directory.mkdir(parents=True, exist_ok=True)
        filename = directory / (f"oe_{instrument.lower()}-{level}_solar1_s202610{day}T000000Z_"
                                f"e202610{day}T235959Z_p202610{processing}T000000Z_pub.nc")
        with Dataset(filename, "w") as ds:
            ds.createDimension("sweep" if instrument == "SWIPS" else "time", 3)
            ds.createDimension("comp", 3)
            dim = "sweep" if instrument == "SWIPS" else "time"
            clock = ds.createVariable("sweep_mid_time" if instrument == "SWIPS" else "time", "f8", (dim,))
            clock.units = "microseconds since 1958-01-01T00:00:00" + (", corrected for leap seconds" if instrument == "SWIPS" else "")
            clock[:] = (self.start + (int(day)-1)*86400 + np.arange(3)*60 + 378691200)*1e6
            y = ds.createVariable("b_gse" if instrument == "MAG" else "proton_n_corr", "f4", (dim,"comp"), fill_value=-9999)
            y.units = "nT"
            y[:] = [[1,2,3],[-9999,5,6],[7,8,9]]
            if instrument == "STIS":
                energy = ds.createVariable("electron_energy_epam_weighted_GdE", "f4", (dim,"comp"))
                energy[:] = [[1,2,3]]*3
                flux = ds.createVariable("electron_flux_epam_weighted_GdE", "f4", (dim,"comp"))
                flux[:] = [[4,5,6]]*3
            if instrument == "MAG":
                ds.createDimension("time_min", 2)
                t = ds.createVariable("time_min", "f8", ("time_min",))
                t.units = "seconds since 1970-01-01"
                t[:] = [self.start, self.start+120]
                ds.createVariable("b_min", "f4", ("time_min",))[:] = [10,20]
        compressed = Path(str(filename)+".gz")
        with filename.open("rb") as source, gzip.open(compressed,"wb") as target:
            target.write(source.read())
        filename.unlink()
        return str(compressed)

    def test_cache_only_clip_and_fill(self):
        self.fixture()
        self.fixture(processing="04")
        with patch.object(loader, "_remote_keys", side_effect=AssertionError("network")):
            files = pyspedas.projects.swfo.mag(trange=[self.start,self.start+120], no_update=True, downloadonly=True)
            self.assertEqual(len(files),1)
            self.assertIn("p20261004",files[0])
            data = pyspedas.projects.swfo.mag(trange=[self.start+60,self.start+120], no_update=True, notplot=True, time_clip=True)
        self.assertEqual(data["swfo_mag_l2_b_gse"]["x"].tolist(),[self.start+60,self.start+120])
        self.assertTrue(np.isnan(data["swfo_mag_l2_b_gse"]["y"][0,0]))
        self.assertEqual(len(data["swfo_mag_l2_b_min"]["x"]),1)

    def test_sweep_time_tplot_and_selection(self):
        self.fixture("SWIPS")
        names = pyspedas.projects.swfo.swips(trange=[self.start,self.start+120],no_update=True,varformat="proton_*",suffix="_test")
        self.assertEqual(names,["swfo_swips_l2_proton_n_corr_test"])
        actual = get_data(names[0])
        np.testing.assert_allclose(actual.times,[self.start,self.start+60,self.start+120])
        self.assertTrue(np.isnan(actual.y[1,0]))

    def test_multifile_sort_and_duplicate_removal(self):
        first=self.fixture()
        second=self.fixture(day="02")
        data=loader._read([second,first,first],"","",None,["b_gse"],[0,1e20],False)
        self.assertEqual(len(data["b_gse"]["x"]),6)
        self.assertTrue(np.all(np.diff(data["b_gse"]["x"])>0))

    def test_archive_pagination_and_latest(self):
        prefix="SWFO/SOLAR-1/MAG/mag-l2/2026/10/"
        old=prefix+"oe_mag-l2_solar1_s20261001T000000Z_e20261001T235959Z_p20261003T000000Z_pub.nc.gz"
        new=old.replace("p20261003","p20261004")
        response1=Mock(content=f'<ListBucketResult xmlns="urn:s3"><Contents><Key>{old}</Key></Contents><NextContinuationToken>next</NextContinuationToken></ListBucketResult>'.encode())
        response2=Mock(content=f'<ListBucketResult xmlns="urn:s3"><Contents><Key>{new}</Key></Contents><Contents><Key>other.nc.gz</Key></Contents></ListBucketResult>'.encode())
        with patch.object(loader,"configure_retry_session") as factory:
            session=factory.return_value.__enter__.return_value
            session.get.side_effect=[response1,response2]
            self.assertEqual(loader._remote_keys("SWFO/SOLAR-1/MAG/mag-l2",["20261001"]),[new])
            self.assertEqual(session.get.call_count,2)

    def test_stis_energy_and_science_product(self):
        self.fixture("STIS")
        data=pyspedas.projects.swfo.stis(trange=[self.start,self.start+60],no_update=True,
                                       notplot=True,time_clip=True,varformat="*flux*")
        item=data["swfo_stis_l2_electron_flux_epam_weighted_GdE"]
        self.assertEqual(item["v"].shape,(2,3))
        np.testing.assert_allclose(item["v"][0],[1,2,3])
        with patch.object(loader,"_remote_keys",return_value=[]) as listing:
            pyspedas.projects.swfo.stis(science=True,level="l3")
            self.assertEqual(listing.call_args.args[0],
                             "SWFO/SOLAR-1/STIS/stis-l3-avg1m-nt-bc_science")

    def test_download_options(self):
        filename=self.fixture()
        key=Path(filename).relative_to(self.tmp.name).as_posix()
        with patch.object(loader,"_remote_keys",return_value=[key]), \
             patch.object(loader,"download",return_value=[filename]) as downloader:
            self.assertEqual(pyspedas.projects.swfo.mag(downloadonly=True,force_download=True),[filename])
            self.assertTrue(downloader.call_args.kwargs["force_download"])

    def test_empty_cache_and_invalid_inputs(self):
        self.assertEqual(pyspedas.projects.swfo.mag(no_update=True),[])
        self.assertEqual(pyspedas.projects.swfo.mag(no_update=True,notplot=True),{})
        for kwargs in ({"instrument":"ccor"},{"level":"bogus"},{"trange":[2,1]},{"trange":None}):
            with self.assertRaises(ValueError):
                loader.load(**kwargs)


if __name__ == "__main__":
    unittest.main()
