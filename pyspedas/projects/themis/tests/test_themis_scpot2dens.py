import unittest

import pyspedas

import pyspedas
from pyspedas.projects.themis.analysis.scpot2dens import dens_pot
from pyspedas.projects.themis.analysis import scpot2dens
from pyspedas import get_data, tplot_copy
import numpy as np
from numpy.testing import assert_allclose
global_display=False


class TestScpo2densValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        IDL Data has to be downloaded to perform these tests
        The IDL script that creates data file: general/tools/python_validate/thm_state_validate.pro
        """
        from pyspedas.utilities.download import download
        from pyspedas.projects.themis.config import CONFIG
        from pyspedas import tplot_restore, del_data,options

        # Testing time range
        cls.t = ['2008-03-23', '2008-03-28']


        # Download validation file
        remote_server = 'https://github.com/spedas/test_data/raw/refs/heads/main/'
        remote_name = 'themis/thm_scpot_validate.tplot'
        datafile = download(remote_file=remote_name,
                           remote_path=remote_server,
                           local_path=CONFIG['local_data_dir'],
                           no_download=False)
        if not datafile:
            # Skip tests
            raise unittest.SkipTest("Cannot download data validation file")

        # Load validation variables from the test file
        del_data('*')
        filename = datafile[0]
        tplot_restore(filename)
        for probe in ['tha', 'thb', 'thc','thd','the']:
            tplot_copy(probe+'_scpot2dens',new_name=probe+'_idl_scpot2dens')
            tplot_copy(probe+'_peer_density_npot',new_name=probe+'_idl_scpot2dens_n')
            options(probe+'_idl_scpot2dens','labels',probe+' IDL scpot2dens')
            options(probe+'_idl_scpot2dens','ylog',1)
            options(probe+'_idl_scpot2dens_n', 'labels',probe+' IDL nishi scpot2dens')


    def test_dens_pot_values(self):
        """ Test supporting function dens_pot for initial values"""
        d1 = dens_pot(-1, 0)
        d2 = dens_pot(-1, 1)

        idl_d1 = 3048.9753
        idl_d2 = 34381.586

        self.assertAlmostEqual(d1, idl_d1, delta=0.1)
        self.assertAlmostEqual(d2, idl_d2, delta=0.1)

    def test_dens_pot_pder_values(self):
        """ Test supporting function dens_pot for derivative values"""
        _, d1 = dens_pot(-1, 0, True)
        _, d2 = dens_pot(-1, 1, True)

        idl_d1 = 6278.0029
        idl_d2 = 95702.727

        self.assertAlmostEqual(d1, idl_d1, delta=0.1)
        self.assertAlmostEqual(d2, idl_d2, delta=0.1)

    def test_dens_pot_list_values(self):
        """ Test supporting function dens_pot for tuple of values and derivative"""
        r1, d1 = dens_pot(np.array([0, -1]), 1, True)

        idl_r1 = np.array([3048.9753, 34381.586])
        idl_d1 = np.array([6278.0029, 95702.727])

        for p, idl in zip(r1, idl_r1):
            self.assertAlmostEqual(p, idl, delta=0.1)

        for p, idl in zip(d1, idl_d1):
            self.assertAlmostEqual(p, idl, delta=0.1)

    def test_scpot2dens_c(self):
        """
        Test satellite case of retrieving density with the change of the spacecraft potential offset.
        The offset if setup for probe c on (2007-7-20/17:24)
        """

        trange = ['2007-7-20/17:23:55', '2007-7-20/17:24:05']

        idl_Npot = np.array([19.2729, 53.6906, 53.0732])

        self.helper_scpot2dens('c', trange, idl_Npot)

    def test_scpot2dens_a(self):
        """
        Test satellite case of retrieving density using data from another spacecraft
        """

        trange = ['2012-01-01/18:10:05', '2012-01-01/18:10:10']

        idl_Npot = np.array([8.74609, 11.7515])

        self.helper_scpot2dens('a', trange, idl_Npot)

    def helper_scpot2dens(self, probe, trange, idl_Npot):
        """
        Helper function that evaluates scpot2dens for diffrent probes and tranges

        Parameters
        ----------
        probe: str
            THEMIS probe
        trange: list[str]
            trange string of the time tange
        idl_Npot: ndarray
            IDL values for the exact same call

        Returns
        -------
        None

        Notes
        -----
        The code that should be executed in IDL to obtain the  idl_Npot values is this:
        ```IDL
        trange = ['2012-01-01/18:10:05']
        probe = 'a'
        thm_load_esa,trange=trange, probe=probe, datat=' peer_avgtemp pe?r_density peer_sc_pot ', level=2
        ; Extract data:
        get_data,'th'+probe+'_peer_density',data=d
        dens_e= d.y
        dens_e_time= d.x
        ;
        get_data,'th'+probe+'_peir_density',data=d
        dens_i= d.y
        dens_i_time= d.x
        ;
        get_data,'th'+probe+'_peer_sc_pot',data=d
        sc_pot = d.y
        sc_pot_time = d.x
        ;
        get_data,'th'+probe+'_peer_avgtemp',data=d
        Te = d.y
        Te_time = d.x

        Npot = thm_scpot2dens(sc_pot, sc_pot_time, Te, Te_time, dens_e, dens_e_time, dens_i, dens_i_time, probe)
        print, Npot
        ```
        """

        pyspedas.projects.themis.esa(trange=trange, probe=probe,
                            varnames=[f'th{probe}_peer_density',
                                      f'th{probe}_peir_density',
                                      f'th{probe}_peer_sc_pot',
                                      f'th{probe}_peer_avgtemp'],
                            level='l2', time_clip=True)

        dens_e_time, dens_e = get_data(f'th{probe}_peer_density')
        dens_i_time, dens_i = get_data(f'th{probe}_peir_density')
        sc_pot_time, sc_pot = get_data(f'th{probe}_peer_sc_pot')
        Te_time, Te = get_data(f'th{probe}_peer_avgtemp')

        Npot = scpot2dens(sc_pot, sc_pot_time, Te, Te_time, dens_e, dens_e_time, dens_i, dens_i_time, probe=probe)

        for p, idl in zip(Npot, idl_Npot):
            self.assertAlmostEqual(p, idl, delta=0.1)

    def test_scpot2dens_idl_a(self):

        trange = ['2014-09-22', '2014-09-23']
        # Set a trange where data is well-behaved enough to make a good test
        nice_trange = ['2014-09-22/08:00', '2014-09-22/19:00']

        probe = 'a'
        self.calc_scpot2dens_single_probe(nice_trange, probe, trange)

        idl_std=get_data('th' + probe + '_idl_scpot2dens-tclip')
        py_std= get_data('th' + probe + '_Npot-tclip')
        idl_nishi = get_data('th' + probe + '_idl_scpot2dens_n-tclip')
        py_nishi = get_data('th' + probe + '_Npot_N-tclip')
        assert_allclose(idl_std.y, py_std.y)
        assert_allclose(idl_nishi.y, py_nishi.y)

    def test_scpot2dens_idl_b(self):

        trange = ['2014-09-22', '2014-09-23']
        # Set a trange where data is well-behaved enough to make a good test
        nice_trange = ['2014-09-22/08:00', '2014-09-22/19:00']
        probe = 'b'
        get_data = self.calc_scpot2dens_single_probe(nice_trange, probe, trange)

        idl_std=get_data('th' + probe + '_idl_scpot2dens-tclip')
        py_std= get_data('th' + probe + '_Npot-tclip')
        idl_nishi = get_data('th' + probe + '_idl_scpot2dens_n-tclip')
        py_nishi = get_data('th' + probe + '_Npot_N-tclip')
        assert_allclose(idl_std.y, py_std.y)
        assert_allclose(idl_nishi.y, py_nishi.y)

    def test_scpot2dens_idl_c(self):

        trange = ['2014-09-22', '2014-09-23']
        # Set a trange where data is well-behaved enough to make a good test
        nice_trange = ['2014-09-22/08:00', '2014-09-22/19:00']

        probe = 'c'
        get_data = self.calc_scpot2dens_single_probe(nice_trange, probe, trange)

        idl_std=get_data('th' + probe + '_idl_scpot2dens-tclip')
        py_std= get_data('th' + probe + '_Npot-tclip')
        idl_nishi = get_data('th' + probe + '_idl_scpot2dens_n-tclip')
        py_nishi = get_data('th' + probe + '_Npot_N-tclip')
        assert_allclose(idl_std.y, py_std.y)
        assert_allclose(idl_nishi.y, py_nishi.y)

    def test_scpot2dens_idl_d(self):

        trange = ['2014-09-22', '2014-09-23']
        # Set a trange where data is well-behaved enough to make a good test
        nice_trange = ['2014-09-22/13:00', '2014-09-22/23:00']

        probe = 'd'
        get_data = self.calc_scpot2dens_single_probe(nice_trange, probe, trange)

        idl_std=get_data('th' + probe + '_idl_scpot2dens-tclip')
        py_std= get_data('th' + probe + '_Npot-tclip')
        idl_nishi = get_data('th' + probe + '_idl_scpot2dens_n-tclip')
        py_nishi = get_data('th' + probe + '_Npot_N-tclip')
        assert_allclose(idl_std.y, py_std.y)
        assert_allclose(idl_nishi.y, py_nishi.y)

    def test_scpot2dens_idl_e(self):

        trange = ['2014-09-22', '2014-09-23']
        # Set a trange where data is well-behaved enough to make a good test
        nice_trange = ['2014-09-22/11:00', '2014-09-22/23:00']

        probe = 'e'
        get_data = self.calc_scpot2dens_single_probe(nice_trange, probe, trange)

        idl_std=get_data('th' + probe + '_idl_scpot2dens-tclip')
        py_std= get_data('th' + probe + '_Npot-tclip')
        idl_nishi = get_data('th' + probe + '_idl_scpot2dens_n-tclip')
        py_nishi = get_data('th' + probe + '_Npot_N-tclip')
        assert_allclose(idl_std.y, py_std.y)
        assert_allclose(idl_nishi.y, py_nishi.y)

    def calc_scpot2dens_single_probe(self, nice_trange, probe, trange):
        from pyspedas.projects.themis.analysis import scpot2dens_nishimura
        from pyspedas.projects.themis.analysis import scpot2dens
        from pyspedas.tplot_tools import get_data
        from pyspedas.tplot_tools import store_data
        from pyspedas.tplot_tools import options
        from pyspedas.tplot_tools import tplot
        import numpy as np

        # get ESA data
        pyspedas.projects.themis.esa(trange=trange, probe=probe,
                                     varnames=['th' + probe + '_peir_density',
                                               'th' + probe + '_peer_sc_pot',
                                               'th' + probe + '_peer_vthermal',
                                               'th' + probe + '_peer_density',
                                               'th' + probe + '_peer_avgtemp',
                                               'th' + probe + '_peer_data_quality'], level='l2')
        # State data
        pyspedas.projects.themis.state(probe=probe, trange=trange)
        pos_data = get_data('th' + probe + '_pos_gsm')
        pos_gsm_time = pos_data.times
        pos_gsm = pos_data.y

        # FGM data
        pyspedas.projects.themis.fgm(trange=trange, probe=probe,
                                     varnames=['th' + probe + '_fgs_gsm'], level='l2')

        # Densities
        dens_i_time, dens_i = get_data('th' + probe + '_peir_density')
        dens_e_time, dens_e = get_data('th' + probe + '_peer_density')
        # SC Potential
        sc_pot_time, sc_pot = get_data('th' + probe + '_peer_sc_pot')
        # Electron Thermal Velocity
        vth_time, vth = get_data('th' + probe + '_peer_vthermal')
        # Average Electron Temperature
        Te_time, Te = get_data('th' + probe + '_peer_avgtemp')
        # Npot Nishimura, no_interp should usually be true if all of the data have the same mode (All ESA data used here are reduced mode).
        Npot_N = scpot2dens_nishimura(sc_pot, sc_pot_time, vth, vth_time, dens_i, dens_i_time, pos_gsm, pos_gsm_time,
                                      probe=probe, no_interp=True)
        # Npot scpot2dens
        Npot = scpot2dens(sc_pot, sc_pot_time, Te, Te_time, dens_e, dens_e_time, dens_i, dens_i_time, probe)

        store_data('th' + probe + '_Npot', {"x": sc_pot_time, "y": Npot})
        store_data('th' + probe + '_Npot_N', {"x": sc_pot_time, "y": Npot_N})
        Npot = 'th' + probe + '_Npot'
        Npot_N = 'th' + probe + '_Npot_N'
        options('th' + probe + '_Npot', 'ylog', 1)
        options('th' + probe + '_Npot_N', 'ylog', 1)
        options('th' + probe + '_Npot', 'yrange', [0.001, 10000.0])
        options('th' + probe + '_Npot_N', 'yrange', [0.001, 10000.0])
        options('th' + probe + '_peer_density', 'yrange', [0.001, 10000.0])
        options('th' + probe + '_peir_density', 'yrange', [0.001, 10000.0])
        options('th' + probe + '_Npot', 'color', 'green')
        options('th' + probe + '_Npot_N', 'color', 'red')
        options('th' + probe + '_peer_density', 'color', 'blue')
        options('th' + probe + '_peir_density', 'color', 'orange')
        options('th' + probe + '_Npot', 'labels', 'N_{scpot}')
        options('th' + probe + '_Npot_N', 'labels', 'N_{scpot}_N')
        options('th' + probe + '_peer_density', 'labels', 'N_e')
        options('th' + probe + '_peir_density', 'labels', 'N_i')

        # Make a multi-tplot variable
        store_data('th' + probe + '_N_comp', ['th' + probe + '_Npot',
                                              'th' + probe + '_Npot_N',
                                              'th' + probe + '_peer_density',
                                              'th' + probe + '_peir_density'])

        # other plots, first L value
        R_E = 6371.0
        pos_l = np.linalg.norm(pos_gsm / R_E, 2, 1)
        store_data('th' + probe + '_Lval', {"x": pos_gsm_time, "y": pos_l})
        options('th' + probe + '_Lval', 'labels', 'L')
        # scpot
        options('th' + probe + '_peer_sc_pot', 'labels', 'SC_POT')
        # Electron Temperature
        options('th' + probe + '_peer_avgtemp', 'labels', 'Elec_Temp')
        options('th' + probe + '_peer_avgtemp', 'ylog', 0)
        # Quality flags
        options('th' + probe + '_peer_data_quality', 'labels', 'DQ')
        # FGM
        options('th' + probe + '_fgs_gsm', 'labels', ['FGS_x', 'FGS_y', 'FGS_z'])
        options('th' + probe + '_fgs_gsm', 'yrange', [-100.0, 100.0])

        if isinstance(trange[0], str):
            fname = 'scpot2dens_test_' + probe + '_' + trange[0]
        else:
            fname = 'scpot2dens_test_' + probe + '_' + pyspedas.time_string(trange[0])

        npdat = get_data('th' + probe + '_Npot')
        np_n_dat = get_data('th' + probe + '_Npot_N')
        idl_npdat = get_data('th' + probe + '_idl_scpot2dens')
        idl_np_n_dat = get_data('th' + probe + '_idl_scpot2dens_n')
        store_data('th' + probe + '_comp_std', ['th' + probe + '_Npot', 'th' + probe + '_idl_scpot2dens'])
        options('th' + probe + '_comp_std', 'color', ['b', 'r'])
        options('th' + probe + '_comp_std', 'ylog', 1)
        store_data('th' + probe + '_comp_nishi', ['th' + probe + '_Npot_N', 'th' + probe + '_idl_scpot2dens_n'])
        options('th' + probe + '_comp_nishi', 'color', ['b', 'r'])

        tplot(['th' + probe + '_Lval',
               'th' + probe + '_peer_sc_pot',
               'th' + probe + '_peer_avgtemp',
               'th' + probe + '_N_comp',
               'th' + probe + '_peer_data_quality',
               'th' + probe + '_fgs_gsm',
               'th' + probe + '_idl_scpot2dens',
               'th' + probe + '_idl_scpot2dens_n',
               'th' + probe + '_comp_std',
               'th' + probe + '_comp_nishi'],
              save_png=fname, display=global_display)

        # Time clip outputs to nice range
        pyspedas.time_clip(
            ['th' + probe + '_idl_scpot2dens', 'th' + probe + '_idl_scpot2dens_n', 'th' + probe + '_Npot',
             'th' + probe + '_Npot_N'], nice_trange[0], nice_trange[1])
        return get_data


if __name__ == '__main__':
    unittest.main()
