"""Offline regression tests for ERG server routing and file versions."""
import importlib
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

import cdflib
from cdflib import cdfwrite
import numpy as np
import pyspedas
from pyspedas.tplot_tools import del_data, get_data
from pyspedas.projects.erg.config import CONFIG

load_module = importlib.import_module('pyspedas.projects.erg.satellite.erg.load')


class LoadRoutingTests(unittest.TestCase):
    def setUp(self):
        config_patch = patch.dict(CONFIG, {
            'ground_remote_data_dir': 'https://ground.example/data/',
            'satellite_remote_data_dir': 'https://satellite.example/arase/',
            'local_data_dir': '/cache/erg', 'no_download': False,
        })
        config_patch.start()
        self.addCleanup(config_patch.stop)

    def test_data_family_urls_and_cache_root(self):
        for prefix, url in [('ground/', 'https://ground.example/data/'),
                            ('satellite/erg/', 'https://satellite.example/arase/')]:
            with self.subTest(prefix=prefix), patch.object(load_module, 'download', return_value=[]) as download:
                load_module.load(pathformat=prefix + 'mgf/%Y/file_%Y%m%d_v01.cdf',
                                 downloadonly=True, no_update=True, force_download=True,
                                 uname='user', passwd='password')
                kwargs = download.call_args.kwargs
                self.assertEqual(kwargs['remote_path'], url)
                self.assertEqual(kwargs['remote_file'], ['mgf/2017/file_20170327_v01.cdf'])
                self.assertEqual(kwargs['local_path'], '/cache/erg')
                self.assertFalse(kwargs['last_version'])
                self.assertTrue(kwargs['no_download'])
                self.assertTrue(kwargs['force_download'])
                self.assertEqual(kwargs['username'], 'user')
                self.assertEqual(kwargs['password'], 'password')

    def test_wildcard_versions(self):
        for version, expected in [('v01_02', False), ('v??_??', True), ('v*', True)]:
            with self.subTest(version=version), patch.object(load_module, 'download', return_value=[]) as download:
                load_module.load(pathformat='satellite/erg/mepe/%Y/file_%Y%m%d_' + version + '.cdf', downloadonly=True)
                self.assertEqual(download.call_args.kwargs['last_version'], expected)

    def test_satellite_wrappers_honor_versions(self):
        cases = [
            ('att', {}, 'v03'), ('hep', {}, 'v03_01'),
            ('hep', {'datatype': '3dflux'}, 'v04_00'), ('hep', {'level': 'l3'}, 'v01_01'),
            ('lepe', {}, 'v04_01'), ('lepi', {}, 'v03_00'),
            ('mepe', {}, 'v01_02'), ('mepi_nml', {}, 'v01_02'),
            ('mepi_tof', {}, 'v01_02'), ('mgf', {}, 'v03.03'),
            ('mgf', {'datatype': '64hz'}, 'v03.03'),
            ('orb', {}, 'v05'), ('orb', {'level': 'l3'}, 'v03'),
            ('xep', {}, 'v01_00'), ('pwe_efd', {}, 'v01_02'),
            ('pwe_efd', {'datatype': 'E64Hz'}, 'v01_02'),
            ('pwe_hfa', {}, 'v01_02'), ('pwe_hfa', {'level': 'l3'}, 'v01_02'),
            ('pwe_ofa', {}, 'v01_02'), ('pwe_wfc', {}, 'v01_02'),
            ('pwe_wfc', {'datatype': 'spec'}, 'v01_02'),
        ]
        for instrument, args, version in cases:
            for selected in [version, None]:
                with self.subTest(instrument=instrument, args=args, version=selected), patch.object(load_module, 'download', return_value=[]) as download:
                    extra = {} if instrument == 'att' else {'ror': False}
                    getattr(pyspedas.projects.erg, instrument)(downloadonly=True, version=selected, **args, **extra)
                    self.assertTrue(download.called)
                    for call in download.call_args_list:
                        kwargs = call.kwargs
                        self.assertEqual(kwargs['remote_path'], 'https://satellite.example/arase/')
                        self.assertEqual(kwargs['last_version'], selected is None)
                        for filename in kwargs['remote_file']:
                            self.assertFalse(filename.startswith('satellite/erg/'))
                            if selected is not None:
                                self.assertIn('_' + selected + '.', filename)

    def test_spdf_product_layouts(self):
        base = 'https://spdf.gsfc.nasa.gov/pub/data/arase/'
        cases = [
            ('mepe', {}, 'mepe/l2/omniflux/2017/'),
            ('orb', {}, 'orb/l2/def/2017/'),
            ('orb', {'level': 'l3'}, 'orb/l3/opq/2017/'),
            ('mgf', {'datatype': '64hz'}, 'mgf/l2/64hz_dsi/2017/'),
            ('mepi_tof', {}, 'mepi/l2/tofflux/2017/'),
            ('pwe_efd', {}, 'pwe/efd/l2/e_spin/2017/'),
            ('pwe_efd', {'datatype': 'E64Hz'}, 'pwe/efd/l2/e64hz_dsi/2017/'),
            ('pwe_hfa', {}, 'pwe/hfa/l2/spec_low/2017/'),
            ('pwe_hfa', {'level': 'l3'}, 'pwe/hfa/l3/1min/2017/'),
            ('pwe_wfc', {'component': 'e'}, 'pwe/wfc/l2/elect/wave/65khz_sgi/2017/'),
            ('pwe_wfc', {'component': 'b', 'datatype': 'spec'}, 'pwe/wfc/l2/mag/spec/65khz/2017/'),
        ]
        with patch.dict(CONFIG, {'satellite_remote_data_dir': base}):
            for instrument, args, directory in cases:
                with self.subTest(instrument=instrument, args=args), patch.object(load_module, 'download', return_value=[]) as download:
                    getattr(pyspedas.projects.erg, instrument)(downloadonly=True, ror=False, **args)
                    for call in download.call_args_list:
                        kwargs = call.kwargs
                        self.assertEqual(kwargs['remote_path'], base)
                        self.assertEqual(kwargs['local_path'], '/cache/erg')
                        self.assertTrue(all(filename.startswith(directory) for filename in kwargs['remote_file']))
                        if instrument == 'pwe_efd':
                            self.assertTrue(all(filename == filename.lower() for filename in kwargs['remote_file']))

    def test_server_filesystem_layout_without_network(self):
        cases = [
            ('satellite_remote_data_dir', 'https://spdf.gsfc.nasa.gov/pub/data/arase/',
             'satellite/erg/mepe/l2/omniflux/%Y/%m/erg_mepe_l2_omniflux_%Y%m%d_v??_??.cdf',
             'mepe/l2/omniflux/2017/erg_mepe_l2_omniflux_20170327_'),
            ('satellite_remote_data_dir', 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/',
             'satellite/erg/mepe/l2/omniflux/%Y/%m/erg_mepe_l2_omniflux_%Y%m%d_v??_??.cdf',
             'mepe/l2/omniflux/2017/03/erg_mepe_l2_omniflux_20170327_'),
            ('ground_remote_data_dir', 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/ground/',
             'ground/geomag/isee/fluxgate/1min/ktb/%Y/isee_fluxgate_1min_ktb_%Y%m%d_v??.cdf',
             'geomag/isee/fluxgate/1min/ktb/2017/isee_fluxgate_1min_ktb_20170327_'),
        ]
        for key, url, template, relative in cases:
            for no_update in [False, True]:
                with self.subTest(url=url, no_update=no_update), tempfile.TemporaryDirectory() as cache, patch.dict(CONFIG, {
                        'local_data_dir': cache, key: url, 'no_download': not no_update}), patch('requests.Session.request', side_effect=AssertionError('Unexpected HTTP request')):
                    versions = ['v01', 'v02'] if key == 'ground_remote_data_dir' else ['v01_01', 'v01_02']
                    for version in versions:
                        filename = Path(cache) / (relative + version + '.cdf')
                        filename.parent.mkdir(parents=True, exist_ok=True)
                        filename.touch()
                    files = load_module.load(pathformat=template, downloadonly=True, no_update=no_update)
                    self.assertEqual(files, [str(filename)])

    def test_spdf_lowercase_efd_filesystem(self):
        with tempfile.TemporaryDirectory() as cache, patch.dict(CONFIG, {
                'local_data_dir': cache, 'no_download': True,
                'satellite_remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/arase/'}), patch('requests.Session.request', side_effect=AssertionError('Unexpected HTTP request')):
            filename = Path(cache) / 'pwe/efd/l2/e_spin/2017/erg_pwe_efd_l2_e_spin_20170401_v05_03.cdf'
            filename.parent.mkdir(parents=True)
            filename.touch()
            files = pyspedas.projects.erg.pwe_efd(downloadonly=True, ror=False, version='v05_03')
            self.assertEqual(files, [str(filename)])

    def test_spdf_reads_cdf_from_filesystem(self):
        with tempfile.TemporaryDirectory() as cache, patch.dict(CONFIG, {
                'local_data_dir': cache, 'no_download': True,
                'satellite_remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/arase/'}), patch('requests.Session.request', side_effect=AssertionError('Unexpected HTTP request')):
            filename = Path(cache) / 'mepe/l2/omniflux/2017/erg_mepe_l2_omniflux_20170327_v01_02.cdf'
            filename.parent.mkdir(parents=True)
            with cdfwrite.CDF(filename) as cdf:
                cdf.write_var({'Variable': 'Epoch', 'Data_Type': cdfwrite.CDF.CDF_EPOCH,
                               'Num_Elements': 1, 'Rec_Vary': True, 'Dim_Sizes': []},
                              var_attrs={'VAR_TYPE': 'support_data'},
                              var_data=cdflib.cdfepoch.compute_epoch([
                                  [2017, 3, 27, 0, 0, 0, 0], [2017, 3, 27, 0, 0, 1, 0]]))
                cdf.write_var({'Variable': 'cache_test', 'Data_Type': cdfwrite.CDF.CDF_DOUBLE,
                               'Num_Elements': 1, 'Rec_Vary': True, 'Dim_Sizes': []},
                              var_attrs={'VAR_TYPE': 'data', 'DEPEND_0': 'Epoch'},
                              var_data=np.array([1.0, 2.0]))
            self.addCleanup(del_data, 'erg_cache_test')
            names = load_module.load(pathformat='satellite/erg/mepe/l2/omniflux/%Y/%m/erg_mepe_l2_omniflux_%Y%m%d_v??_??.cdf', prefix='erg_')
            self.assertIn('erg_cache_test', names)
            np.testing.assert_array_equal(get_data('erg_cache_test').y, [1.0, 2.0])

    def test_config_url_overrides(self):
        config_file = Path(load_module.__file__).parents[2] / 'config.py'
        def apply_preferences(config, mission):
            config['remote_data_dir'] = 'https://legacy.example/root/'
            config['satellite_remote_data_dir'] = 'https://mirror.example/arase/'
        with patch.dict(os.environ, {}, clear=True), patch('pyspedas.preferences.apply_mission_preferences', side_effect=apply_preferences):
            config = runpy.run_path(str(config_file))['CONFIG']
            self.assertEqual(config['ground_remote_data_dir'], 'https://legacy.example/root/ground/')
            self.assertEqual(config['satellite_remote_data_dir'], 'https://mirror.example/arase/')
        with patch.dict(os.environ, {'ERG_REMOTE_DATA_DIR': 'https://env.example/root',
                                     'ERG_SATELLITE_REMOTE_DATA_DIR': 'https://spdf.example/arase/'}, clear=True), patch('pyspedas.preferences.apply_mission_preferences'):
            config = runpy.run_path(str(config_file))['CONFIG']
            self.assertEqual(config['ground_remote_data_dir'], 'https://env.example/root/ground/')
            self.assertEqual(config['satellite_remote_data_dir'], 'https://spdf.example/arase/')


if __name__ == '__main__':
    unittest.main()
