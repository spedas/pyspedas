"""Verify version selection without accessing remote servers or local CDFs."""

import importlib
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
                        LOAD_MODULE + '.CONFIG', remote_data_dir=server):
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
                            'greenland': [False, False, False, False, True],
                            'variometer': [0, 0, 1, 10, 0]}, 5)]
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
        groups = {'spacecraft.fields': ('fgm', 'fit', 'efi', 'scm', 'fft', 'fbk'),
                  'spacecraft.particles': ('esa', 'esd', 'sst', 'mom', 'gmom'),
                  'state_tools': ('state', 'slp', 'ssc', 'ssc_pre'),
                  'ground': ('ask', 'gmag')}
        for group, instruments in groups.items():
            for instrument in instruments:
                module = importlib.import_module(f'pyspedas.projects.themis.{group}.{instrument}')
                for version in (None, 'v02'):
                    with self.subTest(instrument=instrument, version=version), patch.object(
                            module, 'load', return_value=[]) as master:
                        kwargs = {} if version is None else {'version': version}
                        if instrument == 'gmag':
                            kwargs['sites'] = ['idx']
                            with patch.object(module, 'check_variometer', return_value=0), patch.object(
                                    module, 'check_greenland', return_value=False):
                                module.gmag(downloadonly=True, **kwargs)
                        else:
                            getattr(module, instrument)(downloadonly=True, **kwargs)
                        master.assert_called_once()
                        self.assertEqual(master.call_args.kwargs['version'], version)


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


if __name__ == '__main__':
    unittest.main()
