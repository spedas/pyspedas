"""Offline MMS regressions for archive selection and dedicated SDC sources."""
import importlib
import json
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import numpy as np
from cdflib import cdfwrite, cdfepoch

from pyspedas.projects.mms.config import CONFIG, sdc_url
from pyspedas.tplot_tools import del_data, get_data

science = importlib.import_module('pyspedas.projects.mms.mms_load_data')
archive = importlib.import_module('pyspedas.projects.mms.mms_load_data_archive')
TRANGE = ['2015-10-16', '2015-10-17']
NAME = 'mms1_fgm_srvy_l2_20151016_v1.2.3.cdf'


class MMSSourceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.cache = Path(temporary.name)
        config = patch.dict(CONFIG, {
            'local_data_dir': str(self.cache), 'mirror_data_dir': None,
            'data_access': 'sdc', 'remote_data_dir': 'https://archive.example/mms/',
            'sdc_data_dir': 'https://sdc.example/mms/sdc/',
            'no_download': False, 'download_only': False,
        })
        config.start()
        self.addCleanup(config.stop)

    def test_dispatch_and_legacy_spdf_override(self):
        for mode, spdf, use_archive in [('sdc', False, False), ('sdc', True, True),
                                        ('archive', False, True), ('archive', True, True)]:
            with self.subTest(mode=mode, spdf=spdf), patch.dict(CONFIG, data_access=mode), patch.object(
                    science, 'mms_load_data_archive', return_value=['archive']) as selected, patch.object(
                    science, 'mms_login_lasp', return_value=(MagicMock(), None)) as login, patch.object(
                    science, 'download', return_value=json.dumps({'files': []})):
                result = science.mms_load_data(trange=TRANGE, available=True, spdf=spdf,
                                               prefix='pre_', suffix='_suf', no_update=False)
                if use_archive:
                    self.assertEqual(result, ['archive'])
                    login.assert_not_called()
                    self.assertTrue(selected.call_args.kwargs['available'])
                    self.assertEqual(selected.call_args.kwargs['prefix'], 'pre_')
                    self.assertEqual(selected.call_args.kwargs['suffix'], '_suf')
                else:
                    self.assertEqual(result, [])
                    selected.assert_not_called()
                    login.assert_called_once()

    def test_sdc_only_science_stays_on_sdc(self):
        for instrument, level in [('fsm', 'l3'), ('fpi', 'sitl'), ('fpi', 'trig'),
                                  ('feeps', 'l1b')]:
            for spdf in (False, True):
                with self.subTest(instrument=instrument, level=level, spdf=spdf), patch.dict(
                        CONFIG, data_access='archive'), patch.object(science, 'mms_load_data_archive') as selected, patch.object(
                        science, 'mms_login_lasp', return_value=(MagicMock(), None)), patch.object(
                        science, 'download', return_value=json.dumps({'files': []})) as download:
                    science.mms_load_data(instrument=instrument, level=level, available=True, spdf=spdf)
                    selected.assert_not_called()
                    self.assertTrue(download.call_args.kwargs['remote_file'].startswith(
                        'https://sdc.example/mms/sdc/public/files/api/v1/file_info/science?'))

    def test_sdc_query_and_transfer_urls(self):
        for user, access in [(None, 'public'), ('test-user', 'sitl')]:
            record = {'file_name': NAME, 'timetag': '2015-10-16T00:00:00', 'file_size': 1}
            with self.subTest(access=access), patch.dict(CONFIG, download_only=True), patch.object(
                    science, 'mms_login_lasp', return_value=(MagicMock(), user)), patch.object(
                    science, 'download', side_effect=[json.dumps({'files': [record]}), [str(self.cache / NAME)]]) as download:
                result = science.mms_load_data(trange=TRANGE)
                self.assertEqual(len(result), 1)
                self.assertTrue(download.call_args_list[0].kwargs['remote_file'].startswith(
                    f'https://sdc.example/mms/sdc/{access}/files/api/v1/file_info/science?'))
                self.assertEqual(download.call_args_list[1].kwargs['remote_file'],
                    f'https://sdc.example/mms/sdc/{access}/files/api/v1/download/science?file={NAME}')

    def test_legacy_helper_does_not_overwrite_configuration(self):
        legacy = importlib.import_module('pyspedas.projects.mms.mms_load_data_spdf')
        importlib.reload(legacy)
        self.assertEqual(CONFIG['remote_data_dir'], 'https://archive.example/mms/')
        with patch.object(legacy, 'mms_load_data_archive', return_value=['file']) as loader:
            self.assertEqual(legacy.mms_load_data_spdf(probe='2'), ['file'])
            loader.assert_called_once_with(probe='2')

    def test_archive_failure_does_not_query_sdc(self):
        with patch.dict(CONFIG, data_access='archive'), patch.object(
                science, 'mms_login_lasp') as login, patch.object(
                archive, 'download', side_effect=RuntimeError('archive unavailable')):
            with self.assertRaisesRegex(RuntimeError, 'archive unavailable'):
                science.mms_load_data(trange=TRANGE)
            login.assert_not_called()

    def test_archive_url_and_offline_flags(self):
        for url in ('https://mirror.example/mms', 's3://bucket/mms/'):
            for no_update in (False, True):
                with self.subTest(url=url, no_update=no_update), patch.dict(
                        CONFIG, data_access='archive', remote_data_dir=url, no_download=not no_update,
                        download_only=True), patch.object(archive, 'download', return_value=[]) as download, patch.object(
                        archive, 'mms_get_local_files', return_value=[]):
                    science.mms_load_data(trange=TRANGE, no_update=no_update)
                    self.assertEqual(download.call_args.kwargs['remote_path'], url.rstrip('/') + '/')
                    self.assertTrue(download.call_args.kwargs['no_download'])

    def write_cdf(self, probe):
        filename = self.cache / f'mms{probe}/fgm/srvy/l2/2015/10/mms{probe}_fgm_srvy_l2_20151016_v1.2.3.cdf'
        filename.parent.mkdir(parents=True)
        with cdfwrite.CDF(filename) as cdf:
            cdf.write_var({'Variable': 'Epoch', 'Data_Type': cdfwrite.CDF.CDF_EPOCH,
                           'Num_Elements': 1, 'Rec_Vary': True, 'Dim_Sizes': []},
                          var_attrs={'VAR_TYPE': 'support_data'},
                          var_data=cdfepoch.compute_epoch([[2015, 10, 16, 0, 0, 0, 0],
                                                         [2015, 10, 16, 0, 0, 1, 0]]))
            cdf.write_var({'Variable': f'mms{probe}_test', 'Data_Type': cdfwrite.CDF.CDF_DOUBLE,
                           'Num_Elements': 1, 'Rec_Vary': True, 'Dim_Sizes': []},
                          var_attrs={'VAR_TYPE': 'data', 'DEPEND_0': 'Epoch'}, var_data=np.array([1., 2.]))
        return str(filename)

    def test_archive_notplot_and_prefix_from_real_cached_cdfs(self):
        self.write_cdf('1')
        self.write_cdf('2')
        with patch.dict(CONFIG, data_access='archive', no_download=True), patch(
                'requests.Session.request', side_effect=AssertionError('Unexpected network request')):
            result = science.mms_load_data(trange=TRANGE, probe=['1', '2'], notplot=True,
                                           prefix='pre_', suffix='_suf')
        self.assertEqual(set(result), {'pre_mms1_test_suf', 'pre_mms2_test_suf'})
        np.testing.assert_array_equal(result['pre_mms1_test_suf']['y'], [1., 2.])

    def test_archive_download_only_and_available_use_cached_files(self):
        filename = self.write_cdf('1')
        with patch.dict(CONFIG, data_access='archive', no_download=True, download_only=True), patch.object(
                archive, 'cdf_to_tplot') as importer, patch('requests.Session.request', side_effect=AssertionError('Unexpected request')):
            self.assertEqual(science.mms_load_data(trange=TRANGE), [filename])
            self.assertEqual(science.mms_load_data(trange=TRANGE, available=True), [NAME])
            importer.assert_not_called()

    def test_archive_time_clip_keeps_requested_interval(self):
        filename = self.write_cdf('1')
        self.addCleanup(del_data, 'routing_mms1_test')
        with patch.dict(CONFIG, data_access='archive', no_download=True), patch(
                'requests.Session.request', side_effect=AssertionError('Unexpected request')):
            result = science.mms_load_data(trange=['2015-10-16T00:00:00', '2015-10-16T00:00:00.5'],
                                           prefix='routing_', time_clip=True)
        self.assertIn('routing_mms1_test', result)
        np.testing.assert_array_equal(get_data('routing_mms1_test').y, [1.])

    def test_available_http_reads_indexes_only_and_filters_versions(self):
        names = [NAME, NAME.replace('1.2.3', '2.0.0')]
        html = ''.join(f'<a href="{name}">{name}</a>' for name in names)
        with patch.dict(CONFIG, data_access='archive'), patch.object(
                archive, 'download', return_value=html) as download, patch.object(archive, 'cdf_to_tplot') as importer:
            result = science.mms_load_data(trange=TRANGE, available=True, cdf_version='1.2.3')
            self.assertEqual(result, [NAME])
            self.assertEqual(download.call_count, 1)
            self.assertTrue(download.call_args.kwargs['return_text'])
            self.assertEqual(download.call_args.kwargs['remote_file'],
                             'https://archive.example/mms/mms1/fgm/srvy/l2/2015/10/')
            importer.assert_not_called()

    def test_available_s3_lists_without_transferring(self):
        fs = MagicMock()
        fs.glob.return_value = ['bucket/mms/mms1/fgm/srvy/l2/2015/10/' + NAME]
        context = MagicMock()
        context.__enter__.return_value = fs
        with patch.dict(CONFIG, data_access='archive', remote_data_dir='s3://bucket/mms/'), patch.object(
                archive, '_managed_filesystem', return_value=context), patch.object(archive, 'download') as download:
            self.assertEqual(science.mms_load_data(trange=TRANGE, available=True), [NAME])
            download.assert_not_called()
            fs.glob.assert_called_once()

    def test_burst_padding_not_accumulated_across_probes(self):
        trange = ['2015-10-16T13:06:00', '2015-10-16T13:10:00']
        with patch.dict(CONFIG, data_access='archive', download_only=True), patch.object(
                archive, 'download', return_value=[]) as download, patch.object(archive, 'mms_get_local_files', return_value=[]):
            science.mms_load_data(trange=trange, probe=['1', '2'], data_rate='brst')
            first, second = [call.kwargs['remote_file'] for call in download.call_args_list]
            self.assertEqual([name.replace('mms1', 'mms2') for name in first], second)
            self.assertEqual(trange, ['2015-10-16T13:06:00', '2015-10-16T13:10:00'])

    def test_ancillary_products_use_sdc_even_in_archive_mode(self):
        for name, function, kwargs in [
                ('mms_get_state_data', 'mms_get_state_data', {'datatypes': ['pos']}),
                ('mms_get_tetrahedron_qf', 'mms_get_tetrahedron_qf', {})]:
            module = importlib.import_module('pyspedas.projects.mms.mec_ascii.' + name)
            for user, access in [(None, 'public'), ('test-user', 'sitl')]:
                with self.subTest(product=name, access=access), patch.dict(CONFIG, data_access='archive', download_only=True), patch.object(
                        module, 'mms_login_lasp', return_value=(MagicMock(), user)), patch.object(
                        module, 'download', return_value=json.dumps({'files': []})) as download:
                    getattr(module, function)(trange=TRANGE, **kwargs)
                    self.assertTrue(download.call_args.kwargs['remote_file'].startswith(
                        f'https://sdc.example/mms/sdc/{access}/files/api/v1/file_info/ancillary?'))

    def test_sdc_interval_services_ignore_archive_mode(self):
        burst = importlib.import_module('pyspedas.projects.mms.databar_tools.mms_update_brst_intervals')
        fast = importlib.import_module('pyspedas.projects.mms.databar_tools.mms_update_fast_intervals')
        sroi = importlib.import_module('pyspedas.projects.mms.databar_tools.mms_load_sroi_segments')
        with patch.dict(CONFIG, data_access='archive'), patch.object(burst, 'mms_login_lasp', return_value=(MagicMock(), None)), patch.object(
                burst, 'download', return_value=[]) as download:
            burst.mms_download_brst_intervals(burst.time_double(TRANGE))
            self.assertEqual(download.call_args.kwargs['remote_path'],
                             'https://sdc.example/mms/sdc/public/service/latis/')
        with patch.dict(CONFIG, data_access='archive'), patch.object(fast, 'download', return_value='one.sav') as download:
            self.assertEqual(fast.get_mms_abs_selections(*TRANGE), ['one.sav'])
            self.assertTrue(download.call_args.kwargs['remote_file'].startswith(
                'https://sdc.example/mms/sdc/sitl/files/api/v1/file_names/abs_selections?'))
        with patch.dict(CONFIG, data_access='archive'), patch.object(sroi, 'download', return_value=[]) as download:
            sroi.download_mms_srois(*TRANGE, sc_id='mms1')
            self.assertEqual(download.call_args.kwargs['remote_path'],
                             'https://sdc.example/mms/sdc/public/service/latis/mms_events_view.csv')

    def test_ancillary_offline_does_not_attempt_authentication(self):
        state = importlib.import_module('pyspedas.projects.mms.mec_ascii.mms_get_state_data')
        quality = importlib.import_module('pyspedas.projects.mms.mec_ascii.mms_get_tetrahedron_qf')
        for module, function in [(state, state.mms_get_state_data), (quality, quality.mms_get_tetrahedron_qf)]:
            with self.subTest(module=module.__name__), patch.dict(CONFIG, no_download=True, download_only=True), patch.object(
                    module, 'mms_login_lasp') as login, patch.object(module, 'download') as download:
                function(trange=TRANGE)
                login.assert_not_called()
                download.assert_not_called()

    def test_authentication_uses_configured_sdc_endpoint(self):
        login = importlib.import_module('pyspedas.projects.mms.mms_login_lasp')
        import pickle
        with (self.cache / 'mms_auth_info.pkl').open('wb') as file:
            pickle.dump({'user': 'test-user', 'passwd': 'test-password'}, file)
        session = MagicMock()
        session.get.return_value.status_code = 200
        with patch.object(login.os.path, 'expanduser', return_value=str(self.cache)), patch.object(
                login, 'readsav', side_effect=FileNotFoundError), patch.object(
                login, 'configure_retry_session', return_value=session):
            login.mms_login_lasp()
        self.assertEqual(session.get.call_args.args[0],
                         'https://sdc.example/mms/sdc/sitl/files/api/v1/download/science')

    def test_photoelectron_model_uses_sdc_in_archive_mode(self):
        model = importlib.import_module('pyspedas.projects.mms.particles.mms_part_des_photoelectrons')
        def get_model_data(name, metadata=False):
            if metadata:
                return {'CDF': {'GATT': {'Energy_table_name': ['energies_des_0.txt']}}}
            return [1., 2.]
        with patch.dict(CONFIG, data_access='archive'), patch.object(model, 'get_data', side_effect=get_model_data), patch.object(
                model, 'download', return_value=['model.cdf']) as download, patch.object(model, 'cdf_to_tplot'):
            model.mms_part_des_photoelectrons('mms1_des_dist_fast')
        self.assertEqual(download.call_args.kwargs['remote_path'],
                         'https://sdc.example/mms/sdc/public/data/models/fpi/')

    def test_config_preferences_environment_and_import_order(self):
        from pyspedas import preferences
        values = {'data_access': 'archive', 'remote_data_dir': 's3://preferences/mms/',
                  'sdc_data_dir': 'https://preferences.example/mms/sdc/'}
        with patch.dict(os.environ, {'PYSPEDAS_CONFIG_FILE': str(self.cache / 'prefs.toml')}, clear=True):
            self.addCleanup(preferences._read_file.cache_clear)
            preferences.save_preferences('mms', values)
            config = runpy.run_path(str(Path(science.__file__).with_name('config.py')))['CONFIG']
            for key, value in values.items():
                self.assertEqual(config[key], value)
            with patch.dict(os.environ, {'MMS_DATA_ACCESS': 'sdc', 'MMS_REMOTE_DATA_DIR': 'https://env.example/mms/',
                                         'MMS_SDC_DATA_DIR': 'https://env.example/sdc/'}):
                config = runpy.run_path(str(Path(science.__file__).with_name('config.py')))['CONFIG']
                self.assertEqual(config['data_access'], 'sdc')
                self.assertEqual(config['remote_data_dir'], 'https://env.example/mms/')
                self.assertEqual(config['sdc_data_dir'], 'https://env.example/sdc/')

    def test_invalid_mode_fails_before_network(self):
        with patch.dict(CONFIG, data_access='typo'), patch.object(science, 'mms_login_lasp') as login:
            with self.assertRaisesRegex(ValueError, 'Unsupported MMS data_access'):
                science.mms_load_data()
            login.assert_not_called()


if __name__ == '__main__':
    unittest.main()
