"""Offline tests for archive routing and loader behavior."""
import importlib
import unittest
from unittest.mock import patch

from pyspedas.projects import dmsp

loader = importlib.import_module('pyspedas.projects.dmsp.load')


class DmspTests(unittest.TestCase):
    def test_archive_paths(self):
        products = {
            'ssj': 'ssj/precipitating-electrons-ions/2014/dmsp-f18_ssj_precipitating-electrons-ions_20140101_v*.cdf',
            'ssies': 'ssies/ssies-3rl/thermal-plasma-cdf/2014/dmsp-f18_ssies-3_thermal-plasma_20140101????_v*.cdf',
            'ssm': 'ssm/magnetometer/2014/dmsp-f18_ssm_magnetometer_20140101_v*.cdf',
        }
        for instrument, path in products.items():
            with self.subTest(instrument=instrument), patch.object(loader, 'download', return_value=[]) as fetch:
                self.assertEqual(getattr(dmsp, instrument)(downloadonly=True), [])
                self.assertEqual(fetch.call_args.kwargs['remote_file'], ['dmspf18/' + path])

    def test_orbits_and_numeric_versions(self):
        files = ['dmsp-f18_ssies-3_thermal-plasma_201401010124_v01.cdf',
                 'dmsp-f18_ssies-3_thermal-plasma_201401010306_v01.cdf',
                 'dmsp-f18_ssies-3_thermal-plasma_201401010124_v02.cdf']
        with patch.object(loader, 'download', return_value=files):
            self.assertEqual(dmsp.ssies(downloadonly=True), sorted(files[1:]))
        with patch.object(loader, 'download', return_value=['test_v1.9.cdf', 'test_v1.10.cdf']):
            self.assertEqual(dmsp.ssj(downloadonly=True), ['test_v1.10.cdf'])

    def test_probe_validation_precedes_download(self):
        with patch.object(loader, 'download') as fetch:
            for args in [{'probe': 'f19'}, {'instrument': 'unknown'}, {'instrument': 'ssies', 'probe': 15}]:
                with self.subTest(args=args), self.assertRaises(ValueError):
                    dmsp.load(**args)
            fetch.assert_not_called()

    def test_multiple_probes(self):
        with patch.object(loader, 'download', return_value=[]) as fetch:
            dmsp.ssj(probe=['f16', 18, '16'], downloadonly=True)
            paths = fetch.call_args.kwargs['remote_file']
            self.assertEqual(len(paths), 2)
            self.assertTrue(paths[0].startswith('dmspf16/'))
            self.assertTrue(paths[1].startswith('dmspf18/'))

    def test_cache_and_import_options(self):
        with patch.object(loader, 'download', return_value=['a.cdf']) as fetch, patch.object(loader, 'cdf_to_tplot', return_value=['pre_flux_suf']) as convert, patch.object(loader, 'tclip') as clip:
            names = dmsp.ssj(prefix='pre_', suffix='_suf', varnames=['flux'],
                             get_support_data=True, no_update=True, time_clip=True)
            self.assertEqual(names, ['pre_flux_suf'])
            self.assertTrue(fetch.call_args.kwargs['no_download'])
            self.assertEqual(convert.call_args.kwargs['varnames'], ['flux'])
            self.assertEqual(convert.call_args.kwargs['prefix'], 'pre_')
            clip.assert_called_once_with('pre_flux_suf', '2014-01-01', '2014-01-02', suffix='')

    def test_notplot_and_empty_archive(self):
        with patch.object(loader, 'download', return_value=['a.cdf']), patch.object(loader, 'cdf_to_tplot', return_value={'flux': {}}), patch.object(loader, 'tclip') as clip:
            self.assertEqual(dmsp.ssj(notplot=True, time_clip=True), {'flux': {}})
            clip.assert_not_called()
        with patch.object(loader, 'download', return_value=None), patch.object(loader, 'cdf_to_tplot') as convert:
            self.assertEqual(dmsp.ssj(), [])
            self.assertEqual(dmsp.ssj(notplot=True), {})
            convert.assert_not_called()


if __name__ == '__main__':
    unittest.main()
