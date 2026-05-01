import unittest
import pyspedas
from pyspedas.tplot_tools import data_exists, del_data, get_data, tplot_names, time_string, time_double
import numpy as np
from pyspedas import tplot



class LoadTestCases(unittest.TestCase):
    def test_load_dst_data(self):
        # final
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2015-10-15", "2015-10-16"])
        self.assertTrue(data_exists("kyoto_dst"))
        # provisional
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2019-10-15", "2019-10-16"])
        self.assertTrue(data_exists("kyoto_dst"))
        # real time
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2022-07-15", "2022-07-16"])
        self.assertTrue(data_exists("kyoto_dst"))

    def test_load_ae_data(self):
        # provsional before Y2K, ensure that timestamps are correctly interpreted as in the 1900s
        # The data files only contain 2-digit years(!) and we rely on strptime to do the right thing.
        del_data('*')
        ae_vars = pyspedas.projects.kyoto.load_ae(trange=["1996-01-01", "1996-01-05"])
        self.assertTrue(data_exists("kyoto_ae"))
        ae_data = get_data('kyoto_ae')
        self.assertTrue(int(ae_data.times[0]) == int(time_double('1996-01-01')))
        # provisional
        del_data('*')
        ae_vars = pyspedas.projects.kyoto.load_ae(trange=["2019-10-15", "2019-10-16"], datatypes=["ae", "al", "ao", "au", "ax"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("kyoto_al"))
        self.assertTrue(data_exists("kyoto_ao"))
        self.assertTrue(data_exists("kyoto_au"))
        self.assertTrue(data_exists("kyoto_ax"))
        # realtime
        del_data('*')
        ae_vars = pyspedas.projects.kyoto.load_ae(trange=["2025-10-15", "2025-10-16"], datatypes=["ae", "al", "ao", "au", "ax"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("kyoto_al"))
        self.assertTrue(data_exists("kyoto_ao"))
        self.assertTrue(data_exists("kyoto_au"))
        # Apparently the realtime AX index is not available yet
        #self.assertTrue(data_exists("kyoto_ax"))
        del_data('*')
        # Check a time range that straddles the provisionsl/realtime cutoff date
        ae_vars = pyspedas.projects.kyoto.load_ae(trange=["2020-12-31", "2021-01-01:23:59:59.9"], datatypes=["ae", "al", "ao", "au", "ax"])
        # AE index, should be present for both
        start_date_dbl = time_double('2020-12-31/00:00:00')
        end_date_dbl = time_double('2021-01-01/23:59:00.0')
        prov_start_date_dbl = time_double('2021-01-01/00:00:00')
        ae_data = get_data("kyoto_ae")
        self.assertTrue(ae_data.times[0] == start_date_dbl)
        self.assertTrue(ae_data.times[-1] == end_date_dbl)
        ax_data = get_data("kyoto_ax")
        # AX index, only provisional
        self.assertTrue(ax_data.times[0] == start_date_dbl)
        self.assertFalse(ax_data.times[-1] >= prov_start_date_dbl)

    def test_kyoto_ae_y2k(self):
        # Test the sort order for data files across the Y2K boundary
        # The 2-digit year rolls over from 99 to 00, so we want
        # to be sure that the data files are loaded in the right order
        # and the timestamps are monotonic
        trange=['1999-12-30','2000-01-03']
        pyspedas.projects.kyoto.load_ae(trange=trange)
        ae_data = get_data("kyoto_ae")
        dt=ae_data.times[1:]-ae_data.times[0:-1]
        dtmin=np.min(dt)
        dtmax=np.max(dt)
        print(dtmin,dtmax)
        self.assertTrue(dtmin > 0.0)

    def test_kyoto_ae_may2024(self):
        # This tests a small range that has provisional AE data for a specific event, but only
        # realtime on each side.
        del_data('*')
        trange1=['2024-05-07', '2024-05-12']
        trange2=['2024-05-12', '2024-05-21']
        trange3=['2024-05-07', '2024-05-21']

        pyspedas.projects.kyoto.load_ae(trange=trange1,datatypes=["ae"],time_clip=True,prefix='tr1_')
        #tplot('tr1_kyoto_ae')
        pyspedas.projects.kyoto.load_ae(trange=trange2,datatypes=["ae"],time_clip=True,prefix='tr2_')
        #tplot('tr2_kyoto_ae')
        pyspedas.projects.kyoto.load_ae(trange=trange3,datatypes=["ae"],time_clip=True,prefix='tr3_')
        #tplot('tr3_kyoto_ae')
        ae1 = get_data('tr1_kyoto_ae')
        ae2 = get_data('tr2_kyoto_ae')
        ae3 = get_data('tr3_kyoto_ae')
        print(time_string(ae1.times[0]))
        print(time_string(ae1.times[-1]))
        self.assertTrue(ae1.times[0] == time_double(trange1[0]))
        self.assertTrue(ae1.times[-1] > (time_double(trange1[1]) - 5*60))
        self.assertEqual(len(ae1.times) + len(ae2.times), len(ae3.times))

    def test_load_dst_3digit(self):
        # Test a time interval with 3-digit Dst values, which can run together in the data file
        del_data('*')
        dst_vars = pyspedas.projects.kyoto.dst(trange=["2015-03-16", "2015-03-19"])
        self.assertTrue(data_exists("kyoto_dst"))
        kd = get_data("kyoto_dst")
        dst_min=np.min(kd.y)
        self.assertTrue(dst_min < -100.0)

    def test_load_geomagnetic_indices(self):
        del_data('*')
        geom_ind_vars = pyspedas.projects.kyoto.load_geomagnetic_indices(trange=["2015-03-16", "2015-03-19"])
        self.assertTrue(data_exists("kyoto_ae"))
        self.assertTrue(data_exists("thg_idx_al"))
        self.assertTrue(data_exists("noaa_Kp"))
        self.assertTrue(data_exists("gfz_Kp"))
        self.assertTrue(data_exists("omni_Pressure"))
        self.assertTrue("kyoto_ae" in geom_ind_vars)
        self.assertTrue("thg_idx_al" in geom_ind_vars)
        self.assertTrue("noaa_Kp" in geom_ind_vars)
        self.assertTrue("gfz_Kp" in geom_ind_vars)
        self.assertTrue("omni_Pressure" in geom_ind_vars)

    def test_load_geomagnetic_indices_omni_load_all(self):
        del_data('*')
        geom_ind_vars = pyspedas.projects.kyoto.load_geomagnetic_indices(missions=["omni"], omni_load_all=True,trange=["2015-03-16", "2015-03-19"])
        self.assertTrue(data_exists("omni_BY_GSE"))
        self.assertTrue("omni_BY_GSE" in geom_ind_vars)

    def test_load_geomagnetic_indices_datatype(self):
        del_data('*')
        geom_ind_vars = pyspedas.projects.kyoto.load_geomagnetic_indices(trange=["2015-03-16", "2015-03-19"], datatypes=['dst'])
        self.assertTrue(data_exists("kyoto_dst"))
        self.assertTrue("kyoto_dst" in geom_ind_vars)

    def test_errors(self):
        pyspedas.projects.kyoto.dst(trange=None)
        pyspedas.projects.kyoto.dst(trange=["2020-04-01","2020-03-01"])
        pyspedas.projects.kyoto.dst(trange=["1015-10-15", "1015-10-16"])
        pyspedas.projects.kyoto.load_ae(trange=None)
        pyspedas.projects.kyoto.load_ae(trange=["2020-04-01","2020-03-01"])
        pyspedas.projects.kyoto.load_ae(trange=["1015-10-15", "1015-10-16"])


if __name__ == "__main__":
    unittest.main()
