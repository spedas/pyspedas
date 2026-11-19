"""Offline regression tests for THEMIS source routing and version selection."""

import importlib
import os
from pathlib import Path
import runpy
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from pyspedas.projects.themis.load import load


LOAD_MODULE = 'pyspedas.projects.themis.load'
TRANGE = ['2007-03-23', '2007-03-24']


class TestThemisVersions(unittest.TestCase):
    def download_calls(self, **kwargs):
        with patch(LOAD_MODULE + '.download', return_value=[]) as download:
            self.assertEqual(load(trange=TRANGE, downloadonly=True, **kwargs), [])
        return [call.kwargs for call in download.call_args_list]

    def test_state_servers(self):
        for server in ('http://themis.ssl.berkeley.edu/data/themis/',
                       'https://spdf.gsfc.nasa.gov/pub/data/themis/'):
            for version in (None, 'v01', 'v02'):
                with self.subTest(server=server, version=version), patch.dict(
                        LOAD_MODULE + '.CONFIG', remote_data_dir=server,
                        remote_data_layout='spdf' if 'spdf' in server else 'themis'):
                    calls = self.download_calls(instrument='state', level='l1',
                                                probe=['a', 'b'], version=version)
                    self.assertEqual(len(calls), 2)
                    suffix = '_' + version if version else (
                        '_v??' if 'spdf' in server else '')
                    for probe, call in zip(('a', 'b'), calls):
                        self.assertEqual(call['remote_file'], [
                            f'th{probe}/l1/state/2007/th{probe}_l1_state_20070323{suffix}.cdf'])
                        self.assertEqual(call['remote_path'], server)
                        self.assertEqual(call['last_version'], version is None)

    def test_ask_defaults_unchanged(self):
        for kwargs in ({}, {'stations': 'atha'}):
            with self.subTest(kwargs=kwargs):
                calls = self.download_calls(instrument='ask', **kwargs)
                self.assertEqual(len(calls), 1)
                self.assertEqual(calls[0]['remote_file'], [
                    'thg/l2/asi/ask/2007/thg_l2_ask_20070323_v01.cdf'])
                self.assertTrue(calls[0]['last_version'])

    def test_wildcard_paths(self):
        cases = [(name, {}, 1) for name in
                 ('ssc', 'ssc_pre')]
        cases += [('gmag', {'stations': ['idx', 'atha', 'gako', 'gako_100ms', 'upn'],
                            'gmag_group': ['', '', 'variom', 'variom', 'greenland']}, 5)]
        for instrument, kwargs, count in cases:
            for version in (None, 'v01', 'v02'):
                with self.subTest(instrument=instrument, kwargs=kwargs, version=version):
                    calls = self.download_calls(instrument=instrument, version=version, **kwargs)
                    self.assertEqual(len(calls), count)
                    for call in calls:
                        self.assertEqual(call['last_version'], version is None)
                        self.assertTrue(call['remote_file'])
                        for filename in call['remote_file']:
                            self.assertTrue(filename.endswith('_' + (version or 'v??') + '.cdf'))

    def test_probe_versions(self):
        cases = [(name, {}, 1) for name in
                 ('fgm', 'fit', 'fft', 'fbk', 'esa', 'sst', 'mom', 'gmom')]
        cases += [('esa', {'level': 'l1'}, 1),
                  ('esd', {'datatype': 'peif'}, 1),
                  ('scm', {'level': 'l1'}, 3),
                  ('fft', {'level': 'l1'}, 9)]
        for instrument, kwargs, count in cases:
            for version in (None, 'v01', 'v02'):
                with self.subTest(instrument=instrument, kwargs=kwargs, version=version):
                    calls = self.download_calls(instrument=instrument, version=version, **kwargs)
                    self.assertEqual(len(calls), count)
                    expected = version if version is not None else (
                        'v02' if instrument == 'esa' and kwargs.get('level') == 'l1' else 'v01')
                    for call in calls:
                        self.assertFalse(call['last_version'])
                        self.assertTrue(call['remote_file'])
                        for filename in call['remote_file']:
                            self.assertTrue(filename.endswith('_' + expected + '.cdf'))

    def test_fixed_defaults(self):
        for instrument, kwargs in [('efi', {'datatype': ['eff', 'efp']}),
                                   ('scm', {}), ('slp', {})]:
            with self.subTest(instrument=instrument):
                for call in self.download_calls(instrument=instrument, **kwargs):
                    self.assertFalse(call['last_version'])
                    for filename in call['remote_file']:
                        self.assertTrue(filename.endswith('_v01.cdf'))

    def test_fixed_versions_preserved(self):
        for instrument, kwargs in [('ask', {}), ('efi', {'datatype': ['eff', 'efp']}),
                                   ('scm', {}), ('slp', {})]:
            with self.subTest(instrument=instrument):
                calls = self.download_calls(instrument=instrument, version='v02', **kwargs)
                for call in calls:
                    self.assertFalse(call['last_version'])
                    for filename in call['remote_file']:
                        self.assertTrue(filename.endswith('_v01.cdf'))

    def test_wrappers_forward_version(self):
        groups = {
            "spacecraft.fields": ("fgm", "fit", "efi", "scm", "fft", "fbk"),
            "spacecraft.particles": ("esa", "esd", "sst", "mom", "gmom"),
            "state_tools": ("state", "slp", "ssc", "ssc_pre"),
            'ground': ('ask', 'gmag')}
            #"ground": ("ask","gmag")}
        for group, instruments in groups.items():
            for instrument in instruments:
                module = importlib.import_module(f'pyspedas.projects.themis.{group}.{instrument}')
                for version in (None, 'v02'):
                    with self.subTest(instrument=instrument, version=version), patch.object(
                            module, 'load', return_value=[]) as master:
                        kwargs = {} if version is None else {'version': version}
                        if instrument == 'gmag':
                            kwargs['sites'] = ['idx']
                            with patch.object(module, 'in_gmag_group', return_value=False), patch.object(module, '_init_gmag_info'):
                                 module.gmag(downloadonly=True, **kwargs)
                        else:
                            getattr(module, instrument)(downloadonly=True, **kwargs)
                        master.assert_called_once()
                        self.assertEqual(master.call_args.kwargs['version'], version)
                        if instrument == 'gmag':
                            self.assertEqual(master.call_args.kwargs['stations'], ['idx'])
                            self.assertEqual(master.call_args.kwargs['gmag_group'], [''])

class TestDirectDownloads(unittest.TestCase):
    """Run each public loader through the real downloader without network I/O."""

    def check_direct_downloads(self, instrument, datatypes, level='l2', version='v01', **kwargs):
        themis = importlib.import_module('pyspedas.projects.themis')
        for server in ('https://themis.ssl.berkeley.edu/data/themis/',
                       'https://spdf.gsfc.nasa.gov/pub/data/themis/'):
            with self.subTest(server=server, level=level), TemporaryDirectory() as cache:
                session = Mock()
                session.get.side_effect = AssertionError('Unexpected remote directory listing')
                with patch.dict(LOAD_MODULE + '.CONFIG', remote_data_dir=server,
                                local_data_dir=cache, no_download=False), patch(
                        'pyspedas.utilities.download.configure_retry_session', return_value=session), patch(
                        'pyspedas.utilities.download.download_file',
                        side_effect=lambda **kw: kw['filename']) as transfer:
                    files = getattr(themis, instrument)(
                        trange=TRANGE, probe=['a', 'b'], level=level, downloadonly=True, **kwargs)
                expected = [server + f'th{probe}/{level}/{instrument}/2007/'
                            + f'th{probe}_{level}_{datatype}_20070323_{version}.cdf'
                            for probe in ('a', 'b') for datatype in datatypes]
                if instrument in ('efi', 'scm', 'fft'):
                    # L1 fields use the datatype as the directory name.
                    if level == 'l1' or instrument == 'efi':
                        expected = [url.replace(f'/{instrument}/', f'/{datatype}/')
                                    for url, datatype in zip(expected, datatypes * 2)]
                self.assertEqual([call.kwargs['url'] for call in transfer.call_args_list], expected)
                self.assertEqual(len(files), len(expected))
                session.get.assert_not_called()

    def test_fgm_direct_downloads(self):
        for level in ('l1', 'l2'):
            self.check_direct_downloads('fgm', ['fgm'], level=level)

    def test_fit_direct_downloads(self):
        for level in ('l1', 'l2'):
            self.check_direct_downloads('fit', ['fit'], level=level)

    def test_efi_direct_downloads(self):
        self.check_direct_downloads('efi', ['eff', 'efp', 'efw', 'vaf', 'vap', 'vaw',
                                          'vbf', 'vbp', 'vbw'], level='l1', datatype='*')
        self.check_direct_downloads('efi', ['efi', 'efp', 'efw'], datatype='*')

    def test_scm_direct_downloads(self):
        self.check_direct_downloads('scm', ['scp', 'scf', 'scw'], level='l1')
        self.check_direct_downloads('scm', ['scm'])

    def test_fft_direct_downloads(self):
        self.check_direct_downloads('fft', [f'ff{kind}_{size}' for kind in ('f', 'p', 'w')
                                           for size in (16, 32, 64)], level='l1')
        self.check_direct_downloads('fft', ['fft'])

    def test_fbk_direct_downloads(self):
        for level in ('l1', 'l2'):
            self.check_direct_downloads('fbk', ['fbk'], level=level)

    def test_esa_direct_downloads(self):
        self.check_direct_downloads('esa', ['esa'], level='l1', version='v02')
        self.check_direct_downloads('esa', ['esa'])

    def test_esd_direct_downloads(self):
        self.check_direct_downloads('esd', ['esa_peif'], datatype='peif')

    def test_sst_direct_downloads(self):
        for level in ('l1', 'l2'):
            self.check_direct_downloads('sst', ['sst'], level=level)

    def test_mom_direct_downloads(self):
        for level in ('l1', 'l2'):
            self.check_direct_downloads('mom', ['mom'], level=level)

    def test_gmom_direct_downloads(self):
        self.check_direct_downloads('gmom', ['gmom'])

    def test_slp_direct_downloads(self):
        themis = importlib.import_module('pyspedas.projects.themis')
        with TemporaryDirectory() as cache:
            session = Mock()
            session.get.side_effect = AssertionError('Unexpected remote directory listing')
            server = 'https://themis.ssl.berkeley.edu/data/themis/'
            with patch.dict(LOAD_MODULE + '.CONFIG', remote_data_dir=server,
                            local_data_dir=cache, no_download=False), patch(
                    'pyspedas.utilities.download.configure_retry_session', return_value=session), patch(
                    'pyspedas.utilities.download.download_file',
                    side_effect=lambda **kw: kw['filename']) as transfer:
                files = themis.slp(trange=TRANGE, downloadonly=True)
            transfer.assert_called_once()
            self.assertEqual(transfer.call_args.kwargs['url'],
                             server + 'slp/l1/eph/2007/slp_l1_eph_20070323_v01.cdf')
            self.assertEqual(len(files), 1)
            session.get.assert_not_called()



class TestThemisSources(unittest.TestCase):
    def setUp(self):
        self.load_module = importlib.import_module(LOAD_MODULE)
        self.gmag_module = importlib.import_module('pyspedas.projects.themis.ground.gmag')
        self.cache = TemporaryDirectory()
        self.addCleanup(self.cache.cleanup)
        config = patch.dict(self.load_module.CONFIG, {
            'remote_data_dir': 's3://science/themis/',
            'remote_data_layout': 'spdf',
            'variometer_remote_data_dir': 'https://variometers.example/themis/',
            'variometer_remote_data_layout': 'themis',
            'ssc_remote_data_dir': 'https://orbits.example/themis/',
            'gmag_metadata_file': 'https://metadata.example/stations.csv',
            'local_data_dir': self.cache.name,
            'no_download': False,
        })
        config.start()
        self.addCleanup(config.stop)
        metadata = patch.object(self.gmag_module, 'gmag_info', None)
        metadata.start()
        self.addCleanup(metadata.stop)

    def metadata_file(self, root=None, station='ATHA'):
        file = Path(root or self.cache.name) / 'thg/gmags_meta.csv'
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(
            'ccode,network_code,alt_period,notes,all,variom,greenland\n'
            f'{station},CARISMA,,fixture,Y,,\n'
            'S61A,USGS,100ms,fixture,Y,Y,\n'
            'UPN,GREENLAND,,fixture,Y,,Y\n'
            'IDX,THEMIS,,fixture,Y,,\n')
        return file

    def test_state_layout_independent_of_hostname(self):
        for url in ('https://mirror.example/themis/',
                    's3://science/themis/',
                    'https://spdf.gsfc.nasa.gov/pub/data/themis/'):
            for layout in ('themis', 'spdf'):
                for version in (None, 'v03'):
                    with self.subTest(url=url, layout=layout, version=version), patch.dict(
                            self.load_module.CONFIG, remote_data_dir=url, remote_data_layout=layout), patch.object(
                            self.load_module, 'download', return_value=[]) as download:
                        load(instrument='state', level='l1', probe=['a', 'b'],
                             trange=TRANGE, version=version, downloadonly=True)
                        suffix = '_' + version if version else ('_v??' if layout == 'spdf' else '')
                        for probe, call in zip(('a', 'b'), download.call_args_list):
                            self.assertEqual(call.kwargs['remote_file'], [
                                f'th{probe}/l1/state/2007/th{probe}_l1_state_20070323{suffix}.cdf'])
                            self.assertEqual(call.kwargs['last_version'], version is None)
                            self.assertEqual(call.kwargs['remote_path'], url)

    def test_state_highest_version_and_exact_version_from_cache(self):
        directory = Path(self.cache.name) / 'tha/l1/state/2007'
        directory.mkdir(parents=True)
        base = 'tha_l1_state_20070323'
        for suffix in ('', '_v01', '_v03', '_v12'):
            (directory / (base + suffix + '.cdf')).touch()
        with patch.dict(self.load_module.CONFIG, no_download=True), patch(
                'requests.Session.request', side_effect=AssertionError('Unexpected network request')):
            for layout, version, suffix in [('spdf', None, '_v12'), ('themis', None, ''),
                                             ('spdf', 'v03', '_v03'), ('themis', 'v03', '_v03')]:
                with self.subTest(layout=layout, version=version), patch.dict(
                        self.load_module.CONFIG, remote_data_layout=layout):
                    files = load(instrument='state', level='l1', probe='a',
                                 trange=TRANGE, downloadonly=True, version=version)
                    self.assertEqual(files, [str(directory / (base + suffix + '.cdf'))])
            self.assertEqual(load(instrument='state', level='l1', probe='a',
                                  trange=TRANGE, downloadonly=True, version='v99'), [])

    def test_mixed_gmag_station_routing_and_offline_metadata(self):
        self.metadata_file()
        for no_update in (False, True):
            with self.subTest(no_update=no_update), patch.dict(
                    self.load_module.CONFIG, no_download=not no_update), patch.object(
                    self.gmag_module, 'gmag_info', None), patch.object(
                    self.load_module, 'download', return_value=[]) as download, patch(
                    'requests.Session.request', side_effect=AssertionError('Unexpected network request')):
                self.gmag_module.gmag(sites=['atha', 's61a_100ms', 'upn', 'idx', 's61a'],
                                      trange=TRANGE, downloadonly=True, no_update=no_update)
                calls = [call.kwargs for call in download.call_args_list]
                self.assertEqual(len(calls), 5)
                self.assertEqual([call['remote_path'] for call in calls], [
                    's3://science/themis/', 'https://variometers.example/themis/',
                    's3://science/themis/', 's3://science/themis/',
                    'https://variometers.example/themis/'])
                self.assertIn('/variometers/s61a/', calls[1]['remote_file'][0])
                self.assertIn('_s61a_100ms_', calls[1]['remote_file'][0])
                self.assertIn('/greenland_gmag/', calls[2]['remote_file'][0])
                self.assertIn('/l1/mag/idx/', calls[3]['remote_file'][0])
                self.assertTrue(all(call['no_download'] for call in calls))

    def test_metadata_url_and_cache_destination(self):
        file = self.metadata_file()
        with patch.object(self.gmag_module, 'download', return_value=[str(file)]) as download:
            info = self.gmag_module.GMAG_Info()
        self.assertIn('atha', info.station_codes)
        self.assertEqual(download.call_args.kwargs, {
            'remote_file': 'https://metadata.example/stations.csv',
            'local_file': 'thg/gmags_meta.csv',
            'local_path': self.cache.name,
            'no_download': False,
        })

    def test_metadata_cache_refreshes_for_source_or_cache_root(self):
        file = self.metadata_file()
        with patch.object(self.gmag_module, 'download', return_value=[str(file)]) as download:
            self.gmag_module._init_gmag_info()
            first = self.gmag_module.gmag_info
            self.gmag_module._init_gmag_info()
            self.assertEqual(download.call_count, 1)
            # Changing only the science server does not invalidate metadata.
            with patch.dict(self.load_module.CONFIG, remote_data_dir='https://science.example/'):
                self.gmag_module._init_gmag_info()
                self.assertIs(self.gmag_module.gmag_info, first)
            file = self.metadata_file(station='BETT')
            with patch.dict(self.load_module.CONFIG, gmag_metadata_file='https://other.example/meta.csv'):
                self.gmag_module._init_gmag_info()
                self.assertIsNot(self.gmag_module.gmag_info, first)
                self.assertIn('bett', self.gmag_module.gmag_info.station_codes)
                self.assertEqual(download.call_count, 2)
                with TemporaryDirectory() as other_cache, patch.dict(
                        self.load_module.CONFIG, local_data_dir=other_cache):
                    self.gmag_module._init_gmag_info()
                    self.assertEqual(download.call_count, 3)
                    self.assertEqual(download.call_args.kwargs['local_path'], other_cache)

    def test_missing_offline_metadata_fails_without_network(self):
        with patch('requests.Session.request', side_effect=AssertionError('Unexpected network request')):
            with self.assertRaisesRegex(FileNotFoundError, 'GMAG metadata unavailable'):
                self.gmag_module.gmag(sites='atha', no_update=True, downloadonly=True)

    def test_ssc_sources_are_configurable(self):
        for instrument, path in [('ssc', 'tha/ssc/2007/tha_or_ssc_20070301_v??.cdf'),
                                 ('ssc_pre', 'tha/ssc_pre/2007/thapred_or_ssc_20070101_v??.cdf')]:
            with self.subTest(instrument=instrument), patch.object(
                    self.load_module, 'download', return_value=[]) as download:
                load(instrument=instrument, probe='a', trange=TRANGE, downloadonly=True)
                self.assertEqual(download.call_args.kwargs['remote_path'], 'https://orbits.example/themis/')
                self.assertEqual(download.call_args.kwargs['remote_file'], [path])

    def test_failed_source_does_not_try_another_server(self):
        with patch.object(self.load_module, 'download', side_effect=RuntimeError('source unavailable')) as download:
            with self.assertRaisesRegex(RuntimeError, 'source unavailable'):
                load(trange=TRANGE, downloadonly=True)
            download.assert_called_once()

    def test_config_preferences_and_environment(self):
        from pyspedas import preferences
        config_file = Path(self.load_module.__file__).with_name('config.py')
        values = {key: value for key, value in self.load_module.CONFIG.items()
                  if key in ('remote_data_dir', 'remote_data_layout',
                             'variometer_remote_data_dir', 'variometer_remote_data_layout',
                             'gmag_metadata_file', 'ssc_remote_data_dir')}
        with patch.dict(os.environ, {
                'PYSPEDAS_CONFIG_FILE': str(Path(self.cache.name) / 'preferences.toml')}, clear=True):
            self.addCleanup(preferences._read_file.cache_clear)
            preferences.save_preferences('themis', values)
            config = runpy.run_path(str(config_file))['CONFIG']
            for key, value in values.items():
                self.assertEqual(config[key], value)
            env_values = {key: ('themis' if key.endswith('_layout') else f'https://env.example/{key}/')
                          for key in values}
            with patch.dict(os.environ, {'THM_' + key.upper(): value for key, value in env_values.items()}):
                config = runpy.run_path(str(config_file))['CONFIG']
                for key, value in env_values.items():
                    self.assertEqual(config[key], value)

    def test_invalid_layouts_fail_before_downloading(self):
        for family, key in [('data', 'remote_data_layout'),
                            ('variometer', 'variometer_remote_data_layout')]:
            with self.subTest(family=family), patch.dict(
                    self.load_module.CONFIG, {key: 'heliocloud'}):
                with self.assertRaisesRegex(ValueError, 'Unsupported THEMIS'):
                    self.load_module.resolve_source(family)




class SourceSwitcherTests(unittest.TestCase):
    def setUp(self):
        self.config = importlib.import_module('pyspedas.projects.themis.config')
        config_patch = patch.dict(self.config.CONFIG)
        config_patch.start()
        self.addCleanup(config_patch.stop)
        self.families = [
            ('data', self.config.DATA_SOURCES),
            ('variometer', self.config.VARIOMETER_SOURCES),
            ('gmag_metadata', self.config.GMAG_METADATA_SOURCES),
            ('ssc', self.config.SSC_SOURCES),
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
            invalid += [tag for tag in ('ergsc', 'berkeley', 'ucla', 'sdc', 'spdf', 'heliocloud')
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

    def test_presets_select_state_paths_without_hostname_inference(self):
        load_module = importlib.import_module(LOAD_MODULE)
        cases = [
            ('berkeley', 'https://themis.ssl.berkeley.edu/data/themis/', ''),
            ('ucla', 'https://themis-data.igpp.ucla.edu/', ''),
            ('spdf', 'https://spdf.gsfc.nasa.gov/pub/data/themis/', '_v??'),
            ('heliocloud', 's3://gov-nasa-hdrl-data1/spdf/cdaweb/data/themis/', '_v??'),
        ]
        for tag, url, version in cases:
            with self.subTest(tag=tag), patch.object(load_module, 'download', return_value=[]) as download:
                self.config.set_data_source(tag)
                load(instrument='state', level='l1', trange=TRANGE, downloadonly=True)
                self.assertEqual(download.call_args.kwargs['remote_path'], url)
                self.assertTrue(download.call_args.kwargs['remote_file'][0].endswith(version + '.cdf'))
                self.assertTrue(download.call_args.kwargs['last_version'])

    def test_metadata_preset_triggers_existing_cache_invalidation(self):
        gmag_module = importlib.import_module('pyspedas.projects.themis.ground.gmag')
        self.config.set_gmag_metadata_source('berkeley')
        old = Mock(source=(self.config.CONFIG['gmag_metadata_file'], str(self.config.CONFIG['local_data_dir'])))
        with patch.object(gmag_module, 'gmag_info', old), patch.object(gmag_module, 'GMAG_Info') as create:
            self.config.set_gmag_metadata_source('spdf')
            gmag_module._init_gmag_info()
            create.assert_called_once_with(no_download=False)
        self.assertEqual(self.config.CONFIG['gmag_metadata_file'],
                         'https://spdf.gsfc.nasa.gov/pub/data/themis/thg/gmags_meta.csv')

    def test_defaults_and_ssc_endpoint(self):
        with patch.dict(os.environ, {}, clear=True), patch('pyspedas.preferences.apply_mission_preferences'):
            defaults = runpy.run_path(self.config.__file__)
        for family in ('data', 'variometer', 'gmag_metadata'):
            self.assertEqual(defaults['get_' + family + '_source'](), 'berkeley')
        self.assertEqual(defaults['get_ssc_source'](), 'spdf')
        self.config.set_ssc_source('spdf')
        load_module = importlib.import_module(LOAD_MODULE)
        with patch.object(load_module, 'download', return_value=[]) as download:
            load(instrument='ssc', trange=TRANGE, downloadonly=True)
        self.assertEqual(download.call_args.kwargs['remote_path'],
                         'https://cdaweb.gsfc.nasa.gov/pub/data/themis/')


if __name__ == '__main__':
    unittest.main()
