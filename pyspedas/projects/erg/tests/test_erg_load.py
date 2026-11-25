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
from pyspedas.tplot_tools import del_data, get_data, store_data, time_float
from pyspedas.projects.erg.config import CONFIG, resolve_source

load_module = importlib.import_module('pyspedas.projects.erg.satellite.erg.load')


class LoadRoutingTests(unittest.TestCase):
    def setUp(self):
        config_patch = patch.dict(CONFIG, {
            'satellite_remote_data_layout': 'ergsc',
            'att_remote_data_layout': 'ergsc',
            'ground_remote_data_layout': 'ergsc',
            'att_remote_data_dir': 'https://att.example/arase/',
            'ground_remote_data_dir': 'https://ground.example/data/',
            'satellite_remote_data_dir': 'https://satellite.example/arase/',
            'local_data_dir': '/cache/erg', 'no_download': False,
        })
        config_patch.start()
        self.addCleanup(config_patch.stop)

    def test_data_family_urls_and_cache_root(self):
        for family, url in [('ground', 'https://ground.example/data/'),
                            ('satellite', 'https://satellite.example/arase/'),
                            ('att', 'https://att.example/arase/')]:
            with self.subTest(family=family), patch.object(load_module, 'download', return_value=[]) as download:
                load_module.load(**resolve_source(family), pathformat= 'mgf/%Y/file_%Y%m%d_v01.cdf',
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
                load_module.load(**resolve_source('satellite'), pathformat='mepe/%Y/file_%Y%m%d_' + version + '.cdf', downloadonly=True)
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
                        self.assertEqual(kwargs['remote_path'], 'https://att.example/arase/' if instrument == 'att' else 'https://satellite.example/arase/')
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
        with patch.dict(CONFIG, {'satellite_remote_data_dir': base, 'satellite_remote_data_layout': 'spdf'}):
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
             'mepe/l2/omniflux/%Y/%m/erg_mepe_l2_omniflux_%Y%m%d_v??_??.cdf',
             'mepe/l2/omniflux/2017/erg_mepe_l2_omniflux_20170327_'),
            ('satellite_remote_data_dir', 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/',
             'mepe/l2/omniflux/%Y/%m/erg_mepe_l2_omniflux_%Y%m%d_v??_??.cdf',
             'mepe/l2/omniflux/2017/03/erg_mepe_l2_omniflux_20170327_'),
            ('ground_remote_data_dir', 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/ground/',
             'geomag/isee/fluxgate/1min/ktb/%Y/isee_fluxgate_1min_ktb_%Y%m%d_v??.cdf',
             'geomag/isee/fluxgate/1min/ktb/2017/isee_fluxgate_1min_ktb_20170327_'),
        ]
        for key, url, template, relative in cases:
            for no_update in [False, True]:
                with self.subTest(url=url, no_update=no_update), tempfile.TemporaryDirectory() as cache, patch.dict(CONFIG, {
                        'local_data_dir': cache, key: url, 'no_download': not no_update,
                        key.replace('_dir', '_layout'): 'spdf' if 'spdf.gsfc' in url else 'ergsc'}), patch('requests.Session.request', side_effect=AssertionError('Unexpected HTTP request')):
                    versions = ['v01', 'v02'] if key == 'ground_remote_data_dir' else ['v01_01', 'v01_02']
                    for version in versions:
                        filename = Path(cache) / (relative + version + '.cdf')
                        filename.parent.mkdir(parents=True, exist_ok=True)
                        filename.touch()
                    files = load_module.load(**resolve_source(key.split('_')[0]), pathformat=template, downloadonly=True, no_update=no_update)
                    self.assertEqual(files, [str(filename)])

    def test_spdf_lowercase_efd_filesystem(self):
        with tempfile.TemporaryDirectory() as cache, patch.dict(CONFIG, {
                'local_data_dir': cache, 'no_download': True,
                'satellite_remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/arase/',
                'satellite_remote_data_layout': 'spdf'}), patch('requests.Session.request', side_effect=AssertionError('Unexpected HTTP request')):
            filename = Path(cache) / 'pwe/efd/l2/e_spin/2017/erg_pwe_efd_l2_e_spin_20170401_v05_03.cdf'
            filename.parent.mkdir(parents=True)
            filename.touch()
            files = pyspedas.projects.erg.pwe_efd(downloadonly=True, ror=False, version='v05_03')
            self.assertEqual(files, [str(filename)])

    def test_spdf_reads_cdf_from_filesystem(self):
        with tempfile.TemporaryDirectory() as cache, patch.dict(CONFIG, {
                'local_data_dir': cache, 'no_download': True,
                'satellite_remote_data_dir': 'https://spdf.gsfc.nasa.gov/pub/data/arase/',
                'satellite_remote_data_layout': 'spdf'}), patch('requests.Session.request', side_effect=AssertionError('Unexpected HTTP request')):
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
            names = load_module.load(**resolve_source('satellite'), pathformat='mepe/l2/omniflux/%Y/%m/erg_mepe_l2_omniflux_%Y%m%d_v??_??.cdf', prefix='erg_')
            self.assertIn('erg_cache_test', names)
            np.testing.assert_array_equal(get_data('erg_cache_test').y, [1.0, 2.0])

    def test_config_url_overrides(self):
        config_file = Path(load_module.__file__).parents[2] / 'config.py'
        def apply_preferences(config, mission):
            config['remote_data_dir'] = 'https://legacy.example/root/'
            config['satellite_remote_data_dir'] = 'https://mirror.example/arase/'
        with patch.dict(os.environ, {}, clear=True), patch('pyspedas.preferences.apply_mission_preferences', side_effect=apply_preferences), self.assertLogs(level='WARNING') as logs:
            config = runpy.run_path(str(config_file))['CONFIG']
            self.assertIn('deprecated', logs.output[0])
            self.assertEqual(config['att_remote_data_dir'], 'https://legacy.example/root/satellite/erg/')
            self.assertEqual(config['ground_remote_data_dir'], 'https://legacy.example/root/ground/')
            self.assertEqual(config['satellite_remote_data_dir'], 'https://mirror.example/arase/')
        with patch.dict(os.environ, {'ERG_REMOTE_DATA_DIR': 'https://env.example/root',
                                     'ERG_SATELLITE_REMOTE_DATA_DIR': 'https://spdf.example/arase/'}, clear=True), patch('pyspedas.preferences.apply_mission_preferences'), self.assertLogs(level='WARNING') as logs:
            config = runpy.run_path(str(config_file))['CONFIG']
            self.assertIn('deprecated', logs.output[0])
            self.assertEqual(config['att_remote_data_dir'], 'https://env.example/root/satellite/erg/')
            self.assertEqual(config['ground_remote_data_dir'], 'https://env.example/root/ground/')
            self.assertEqual(config['satellite_remote_data_dir'], 'https://spdf.example/arase/')


    def test_layout_is_independent_of_url(self):
        for url in ('https://mirror.example/erg/',
                    's3://other-bucket/arase/',
                    'https://spdf.gsfc.nasa.gov/pub/data/arase/'):
            for layout, directory in [('spdf', 'mepe/l2/omniflux/2017/'),
                                      ('ergsc', 'mepe/l2/omniflux/2017/03/')]:
                with self.subTest(url=url, layout=layout), patch.dict(CONFIG, {
                        'satellite_remote_data_dir': url,
                        'satellite_remote_data_layout': layout}), patch.object(load_module, 'download', return_value=[]) as download:
                    pyspedas.projects.erg.mepe(downloadonly=True, ror=False)
                    self.assertEqual(download.call_args.kwargs['remote_path'], url)
                    self.assertTrue(download.call_args.kwargs['remote_file'][0].startswith(directory))

    def test_mixed_sources_and_failure_without_fallback(self):
        with patch.dict(CONFIG, {
                'satellite_remote_data_dir': 's3://science/erg/',
                'satellite_remote_data_layout': 'spdf',
                'att_remote_data_dir': 'https://att.example/arase/',
                'att_remote_data_layout': 'spdf'}), patch.object(load_module, 'download', return_value=[]) as download:
            calls = [
                (pyspedas.projects.erg.mepe, {'ror': False}, 's3://science/erg/', 'mepe/'),
                (pyspedas.projects.erg.att, {}, 'https://att.example/arase/', 'att/txt/'),
                (pyspedas.projects.erg.gmag_isee_fluxgate, {'site': 'ktb', 'datatype': '1min', 'ror': False},
                 'https://ground.example/data/', 'geomag/'),
            ]
            for wrapper, args, url, directory in calls:
                with self.subTest(wrapper=wrapper.__name__):
                    download.reset_mock()
                    wrapper(downloadonly=True, **args)
                    self.assertEqual(download.call_count, 1)
                    self.assertEqual(download.call_args.kwargs['remote_path'], url)
                    self.assertTrue(download.call_args.kwargs['remote_file'][0].startswith(directory))
            download.reset_mock()
            download.side_effect = RuntimeError('source unavailable')
            with self.assertRaisesRegex(RuntimeError, 'source unavailable'):
                pyspedas.projects.erg.mepe(downloadonly=True, ror=False)
            self.assertEqual(download.call_count, 1)

    def test_all_ground_wrappers_select_ground_source(self):
        cases = [('gmag_isee_fluxgate', {'site': 'ktb'}),
                 ('gmag_isee_induction', {'site': 'ath'}),
                 ('gmag_magdas_1sec', {'site': 'ama'}),
                 ('gmag_mm210', {'site': 'adl'}),
                 ('camera_omti_asi', {'site': 'ath'}),
                 ('isee_brio', {'site': 'ath'}),
                 ('isee_vlf', {'site': 'ath'}),
                 ('sd_fit', {'site': 'ade'})]
        for name, args in cases:
            with self.subTest(name=name), patch.object(load_module, 'download', return_value=[]) as download:
                getattr(pyspedas.projects.erg, name)(downloadonly=True, ror=False, **args)
                self.assertTrue(download.called)
                for call in download.call_args_list:
                    self.assertEqual(call.kwargs['remote_path'], 'https://ground.example/data/')
                    self.assertFalse(call.kwargs['remote_file'][0].startswith('ground/'))

    def test_invalid_source_configuration(self):
        with self.assertRaisesRegex(ValueError, 'Unknown ERG data family'):
            resolve_source('unknown')
        for family, layout in [('satellite', 'typo'), ('att', 'heliocloud'), ('ground', 'spdf'),
                               ('satellite', 'jaxa'), ('att', 'jaxa')]:
            with self.subTest(family=family), patch.dict(CONFIG, {family + '_remote_data_layout': layout}), patch.object(load_module, 'download') as download:
                with self.assertRaisesRegex(ValueError, 'Unsupported ERG'):
                    resolve_source(family)
                download.assert_not_called()
        with patch.dict(CONFIG, {'att_remote_data_dir': ''}):
            with self.assertRaisesRegex(ValueError, 'nonempty URL'):
                resolve_source('att')

    def test_source_preferences_and_environment(self):
        config_file = Path(load_module.__file__).parents[2] / 'config.py'
        def apply_preferences(config, mission):
            config.update({
                'satellite_remote_data_dir': 's3://preferences/erg/',
                'satellite_remote_data_layout': 'spdf',
                'att_remote_data_dir': 'https://preferences.example/arase/',
                'att_remote_data_layout': 'spdf',
                'ground_remote_data_dir': 'https://preferences.example/ground/',
            })
        with patch.dict(os.environ, {}, clear=True), patch('pyspedas.preferences.apply_mission_preferences', side_effect=apply_preferences):
            config = runpy.run_path(str(config_file))['CONFIG']
            self.assertEqual(config['satellite_remote_data_layout'], 'spdf')
            self.assertEqual(config['att_remote_data_layout'], 'spdf')
            self.assertEqual(config['ground_remote_data_layout'], 'ergsc')
            self.assertEqual(config['att_remote_data_dir'], 'https://preferences.example/arase/')
        env = {f'ERG_{family.upper()}_REMOTE_DATA_{suffix}': value
               for family in ('satellite', 'att', 'ground')
               for suffix, value in [('DIR', f'https://env.example/{family}/'), ('LAYOUT', 'ergsc')]}
        with patch.dict(os.environ, env, clear=True), patch('pyspedas.preferences.apply_mission_preferences', side_effect=apply_preferences):
            config = runpy.run_path(str(config_file))['CONFIG']
            for family in ('satellite', 'att', 'ground'):
                self.assertEqual(config[family + '_remote_data_dir'], f'https://env.example/{family}/')
                self.assertEqual(config[family + '_remote_data_layout'], 'ergsc')



    def test_automatic_attitude_load_uses_separate_source_and_cache(self):
        interpolate_att = importlib.import_module(
            'pyspedas.projects.erg.satellite.erg.common.cotrans.erg_interpolate_att')
        self.addCleanup(del_data, 'erg_att_*')
        self.addCleanup(del_data, 'erg_routing_test')
        # Minimal ASCII attitude fixture, including the header rows skipped by att().
        rows = ['header'] * 11
        for second in range(0, 33, 8):
            rows.append(f'2017-04-01T00:00:{second:02d} 8 0 90 0 0 0 0 0 0 0 0 0 90')
        for layout in ('ergsc', 'spdf'):
            with self.subTest(layout=layout), tempfile.TemporaryDirectory() as cache, patch.dict(CONFIG, {
                    'local_data_dir': cache, 'no_download': True,
                    'satellite_remote_data_dir': 's3://science/erg/',
                    'satellite_remote_data_layout': 'spdf',
                    'att_remote_data_dir': 'https://att.example/arase/',
                    'att_remote_data_layout': layout}), patch('requests.Session.request', side_effect=AssertionError('Unexpected HTTP request')):
                filename = Path(cache) / 'att/txt/erg_att_l2_20170401_v03.txt'
                filename.parent.mkdir(parents=True)
                filename.write_text('\n'.join(rows) + '\n')
                times = time_float(['2017-04-01T00:00:08', '2017-04-01T00:00:16'])
                attitude = pyspedas.projects.erg.att(notplot=True)
                np.testing.assert_array_equal(attitude['erg_att_sprate']['y'], [8.] * 5)
                del_data('erg_att_*')
                store_data('erg_routing_test', data={'x': times, 'y': np.ones((2, 3))})
                # Wrap the real downloader to verify the indirect att() call's URL.
                with patch.object(load_module, 'download', wraps=load_module.download) as download:
                    output = interpolate_att.erg_interpolate_att('erg_routing_test')
                self.assertTrue(download.called)
                self.assertEqual(download.call_args.kwargs['remote_path'], 'https://att.example/arase/')
                np.testing.assert_allclose(output['spinperiod']['y'], [7.5, 7.5])
                np.testing.assert_allclose(output['sgiz_j2000']['y'], [[0., 0., 1.]] * 2, atol=1e-15)
                del_data('erg_att_*')

    def test_persistent_family_preferences(self):
        from pyspedas import preferences
        config_file = Path(load_module.__file__).parents[2] / 'config.py'
        values = {
            'satellite_remote_data_dir': 's3://science/erg/',
            'satellite_remote_data_layout': 'spdf',
            'att_remote_data_dir': 'https://att.example/arase/',
            'att_remote_data_layout': 'spdf',
            'ground_remote_data_dir': 'https://ground.example/data/',
            'ground_remote_data_layout': 'ergsc',
        }
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {
                'PYSPEDAS_CONFIG_FILE': str(Path(directory) / 'preferences.toml')}, clear=True):
            self.addCleanup(preferences._read_file.cache_clear)
            preferences.save_preferences('erg', values)
            config = runpy.run_path(str(config_file))['CONFIG']
            for key, value in values.items():
                self.assertEqual(config[key], value)




class SourceSwitcherTests(unittest.TestCase):
    def setUp(self):
        self.config = importlib.import_module('pyspedas.projects.erg.config')
        config_patch = patch.dict(self.config.CONFIG)
        config_patch.start()
        self.addCleanup(config_patch.stop)
        self.families = [
            ('satellite', self.config.SATELLITE_SOURCES),
            ('attitude', self.config.ATTITUDE_SOURCES),
            ('ground', self.config.GROUND_SOURCES),
        ]

    def test_presets_update_only_their_family_and_log_settings(self):
        with patch('pyspedas.preferences.save_preferences', side_effect=AssertionError('Unexpected preference write')), patch(
                'requests.Session.request', side_effect=AssertionError('Unexpected network request')):
            for family, table in self.families:
                for tag, settings in table.items():
                    with self.subTest(family=family, tag=tag):
                        before = self.config.CONFIG.copy()
                        with self.assertLogs(level='INFO') as logs:
                            getattr(self.config, 'set_' + family + '_source')(tag)
                        expected = before.copy()
                        expected.update(settings)
                        self.assertEqual(self.config.CONFIG, expected)
                        self.assertEqual(getattr(self.config, 'get_' + family + '_source')(), tag)
                        self.assertEqual(len(logs.output), 1)
                        self.assertIn(tag, logs.output[0])
                        for value in settings.values():
                            self.assertIn(value, logs.output[0])

    def test_invalid_tags_leave_entire_configuration_unchanged(self):
        for family, table in self.families:
            invalid = ['unknown', 'SPDF', '', None, [], {}]
            invalid += [tag for tag in ('ergsc', 'jaxa', 'berkeley', 'ucla', 'sdc', 'spdf', 'heliocloud')
                        if tag not in table]
            for tag in invalid:
                with self.subTest(family=family, tag=tag):
                    before = self.config.CONFIG.copy()
                    with self.assertRaises(ValueError) as error:
                        getattr(self.config, 'set_' + family + '_source')(tag)
                    self.assertIn('valid choices: ' + ', '.join(sorted(table)), str(error.exception))
                    self.assertEqual(self.config.CONFIG, before)

    def test_getters_follow_direct_edits_and_recognize_custom_settings(self):
        for family, table in self.families:
            getter = getattr(self.config, 'get_' + family + '_source')
            for tag, settings in table.items():
                with self.subTest(family=family, tag=tag):
                    self.config.CONFIG.update(settings)
                    self.assertEqual(getter(), tag)
                    for key in settings:
                        self.config.CONFIG[key] = 'custom-setting'
                        self.assertIsNone(getter())
                        self.config.CONFIG.update(settings)
                    key = next(iter(settings))
                    del self.config.CONFIG[key]
                    self.assertIsNone(getter())
                    self.config.CONFIG.update(settings)

    def test_mixed_presets_route_existing_loaders(self):
        self.config.set_satellite_source('heliocloud')
        self.config.set_attitude_source('spdf')
        self.config.set_ground_source('ergsc')
        cases = [
            (pyspedas.projects.erg.mepe, {'ror': False},
             's3://gov-nasa-hdrl-data1/spdf/cdaweb/data/erg/', 'mepe/l2/omniflux/2017/'),
            (pyspedas.projects.erg.att, {},
             'https://spdf.gsfc.nasa.gov/pub/data/arase/', 'att/txt/'),
            (pyspedas.projects.erg.gmag_isee_fluxgate, {'site': 'ktb', 'datatype': '1min', 'ror': False},
             'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/ground/', 'geomag/'),
        ]
        for wrapper, kwargs, url, directory in cases:
            with self.subTest(wrapper=wrapper.__name__), patch.object(load_module, 'download', return_value=[]) as download:
                wrapper(downloadonly=True, **kwargs)
                self.assertEqual(download.call_args.kwargs['remote_path'], url)
                self.assertTrue(download.call_args.kwargs['remote_file'][0].startswith(directory))

    def test_jaxa_presets_route_satellite_and_attitude_with_ergsc_layout(self):
        self.config.set_satellite_source('jaxa')
        self.config.set_attitude_source('jaxa')
        url = 'https://data.darts.isas.jaxa.jp/pub/erg/'
        for family in ('satellite', 'att'):
            self.assertEqual(self.config.resolve_source(family), {
                'remote_data_dir': url, 'remote_data_layout': 'ergsc'})
        cases = [
            (pyspedas.projects.erg.mepe, {'ror': False},
             'mepe/l2/omniflux/2017/03/erg_mepe_l2_omniflux_20170327_', 'v01_02'),
            (pyspedas.projects.erg.att, {}, 'att/txt/erg_att_l2_20170327_', 'v03'),
        ]
        for wrapper, kwargs, filename_prefix, version in cases:
            for selected in (None, version):
                with self.subTest(wrapper=wrapper.__name__, version=selected), patch.object(
                        load_module, 'download', return_value=[]) as download:
                    wrapper(trange=['2017-03-27', '2017-03-28'], downloadonly=True,
                            version=selected, **kwargs)
                    self.assertTrue(download.called)
                    for call in download.call_args_list:
                        self.assertEqual(call.kwargs['remote_path'], url)
                        self.assertEqual(call.kwargs['last_version'], selected is None)
                        self.assertTrue(all(name.startswith(filename_prefix)
                                            for name in call.kwargs['remote_file']))
                        if selected is not None:
                            self.assertTrue(all('_' + selected + '.' in name
                                                for name in call.kwargs['remote_file']))

    def test_defaults_are_still_recognized(self):
        config_file = Path(self.config.__file__)
        with patch.dict(os.environ, {}, clear=True), patch('pyspedas.preferences.apply_mission_preferences'):
            defaults = runpy.run_path(str(config_file))
        self.assertEqual(defaults['get_satellite_source'](), 'ergsc')
        self.assertEqual(defaults['get_attitude_source'](), 'ergsc')
        self.assertEqual(defaults['get_ground_source'](), 'ergsc')


if __name__ == '__main__':
    unittest.main()
