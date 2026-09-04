"""Verify version selection without accessing remote servers or local CDFs."""

import importlib
import unittest
from unittest.mock import patch

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

    def test_wildcard_paths(self):
        cases = [(name, {}, 1) for name in
                 ('fgm', 'fit', 'fft', 'fbk', 'esa', 'sst', 'mom', 'gmom', 'ssc', 'ssc_pre')]
        cases += [('esd', {'datatype': 'peif'}, 1),
                  ('scm', {'level': 'l1'}, 3),
                  ('fft', {'level': 'l1'}, 9),
                  ('gmag', {'stations': ['idx', 'atha', 'gako', 'gako_100ms', 'upn'],
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


if __name__ == '__main__':
    unittest.main()
