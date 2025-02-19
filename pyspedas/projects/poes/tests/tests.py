import os
import unittest
from pytplot import data_exists
from pytplot import get_data
import pyspedas
from pyspedas.projects.poes.load import load


class LoadTestCases(unittest.TestCase):
    def test_load_notplot(self):
        sem_vars = pyspedas.projects.poes.sem(notplot=True)
        self.assertTrue('ted_ele_tel0_low_eflux' in sem_vars)

    def test_load_sem_data(self):
        sem_vars = pyspedas.projects.poes.sem(time_clip=True)
        self.assertTrue(data_exists('ted_ele_tel0_low_eflux'))

    def test_load_probe_regression(self):
        sem_vars = pyspedas.projects.poes.sem(probe='metop1', time_clip=True)
        self.assertTrue(data_exists('ted_ele_tel0_low_eflux'))
        m = get_data('ted_ele_tel0_low_eflux', metadata=True)
        # Workaround for cdflib globalattsget bug
        md_sn = m['CDF']['GATT']['Source_name']
        if isinstance(md_sn,list):
            md_sn = md_sn[0]
        self.assertTrue(md_sn == 'MetOp1')
        sem_vars = pyspedas.projects.poes.sem(probe='metop2', time_clip=True)
        m = get_data('ted_ele_tel0_low_eflux', metadata=True)
        # workaround for cdflib globalattsget bug
        md_sn = m['CDF']['GATT']['Source_name']
        if isinstance(md_sn,list):
            md_sn = md_sn[0]
        self.assertTrue(md_sn == 'MetOp2')

    def test_downloadonly(self):
        files = pyspedas.projects.poes.sem(downloadonly=True, probe='noaa19')
        self.assertTrue(os.path.exists(files[0]))

    def test_ncei_server(self):
        vars = load(trange=['1999-01-03', '1999-01-04'], probe=['noaa15'], ncei_server=True, time_clip=True)
        self.assertTrue('geogLL' in vars)


if __name__ == '__main__':
    unittest.main()
