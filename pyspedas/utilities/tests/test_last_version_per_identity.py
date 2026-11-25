"""Offline string-only tests for explicit per-identity version selection."""

import re
import unittest
from itertools import permutations

from pyspedas.utilities.last_version_per_identity import last_version_per_identity


MMS_PATTERN = r'(?P<identity>mms2_.+_\d{14})_v(?P<version>\d+\.\d+\.\d+)\.cdf'

# Actual SPDF HPCA filenames reported in issue #1582. Different timestamps
# legitimately have different latest versions; none may be dropped globally.
HPCA_TIMESTAMPS = [
    '20240511105113', '20240511105313', '20240511110503',
    '20240511110723', '20240511110953', '20240511111213',
    '20240511111443', '20240511111703', '20240511111933',
    '20240511112153', '20240511113153', '20240511120823',
    '20240511121443', '20240511122623', '20240511123753',
    '20240511143943', '20240511144203', '20240511144413',
    '20240511144633',
]
HPCA_FILES = [
    f'mms2_hpca_brst_l2_moments_{timestamp}_v'
    + ('4.3.2' if timestamp == '20240511144633' else '4.3.0') + '.cdf'
    for timestamp in HPCA_TIMESTAMPS
]
EDP_FILES = [
    'mms2_edp_brst_l2_scpot_20240511143943_v2.9.0.cdf',
    'mms2_edp_brst_l2_scpot_20240511143943_v2.9.1.cdf',
]


class LastVersionPerIdentityTests(unittest.TestCase):
    def test_mms_hpca_preserves_all_nineteen_timestamps(self):
        result = last_version_per_identity(list(reversed(HPCA_FILES)), MMS_PATTERN)
        self.assertEqual(len(result), 19)
        self.assertEqual(result, HPCA_FILES)

    def test_mms_edp_keeps_one_version_of_the_same_timestamp(self):
        self.assertEqual(last_version_per_identity(EDP_FILES, MMS_PATTERN), [EDP_FILES[1]])

    def test_multiple_identities_each_get_their_own_latest_version(self):
        # The second timestamp's newest version is lower than the first one's.
        second_timestamp = 'mms2_edp_brst_l2_scpot_20240511144203_v2.8.0.cdf'
        self.assertEqual(
            last_version_per_identity(EDP_FILES + [second_timestamp], MMS_PATTERN),
            [EDP_FILES[1], second_timestamp],
        )

    def test_empty_input(self):
        self.assertEqual(last_version_per_identity([], MMS_PATTERN), [])

    def test_none_and_empty_iterables_return_empty_lists_without_regex_validation(self):
        for filenames in (None, [], (), iter(())):
            with self.subTest(filenames=filenames):
                self.assertEqual(last_version_per_identity(filenames, None), [])

    def test_single_string_returns_a_one_element_list_without_regex_validation(self):
        for filename in (EDP_FILES[0], 'unrelated.txt', ''):
            with self.subTest(filename=filename):
                self.assertEqual(last_version_per_identity(filename, None), [filename])

    def test_single_match(self):
        self.assertEqual(last_version_per_identity([EDP_FILES[0]], MMS_PATTERN), [EDP_FILES[0]])

    def test_duplicate_input_filenames_do_not_duplicate_results(self):
        self.assertEqual(last_version_per_identity(EDP_FILES * 2, MMS_PATTERN), [EDP_FILES[1]])

    def test_empty_identity_selects_a_single_latest_version(self):
        pattern = r'fixed_(?P<identity>)v(?P<version>\d{2})\.cdf'
        files = ['fixed_v02.cdf', 'fixed_v01.cdf', 'fixed_v03.cdf']
        self.assertEqual(last_version_per_identity(files, pattern), ['fixed_v03.cdf'])

    def test_identity_only_pattern_keeps_all_distinct_files(self):
        files = ['observation_B.cdf', 'observation_A.cdf']
        pattern = r'(?P<identity>observation_[A-Z])\.cdf'
        self.assertEqual(last_version_per_identity(files, pattern), sorted(files))

    def test_version_capture_is_optional(self):
        pattern = r'(?P<identity>file_[AB])_v\d{2}\.cdf'
        files = ['file_A_v01.cdf', 'file_A_v02.cdf', 'file_B_v01.cdf']
        self.assertEqual(last_version_per_identity(files, pattern), files[1:])

    def test_input_is_unchanged_and_output_order_is_deterministic(self):
        files = ['file_B_v01.cdf', 'file_A_v02.cdf', 'file_A_v01.cdf']
        pattern = r'(?P<identity>file_[AB])_v\d{2}\.cdf'
        for ordered in permutations(files):
            with self.subTest(order=ordered):
                original = list(ordered)
                result = last_version_per_identity(original, pattern)
                self.assertEqual(result, ['file_A_v02.cdf', 'file_B_v01.cdf'])
                self.assertEqual(original, list(ordered))
                self.assertIsNot(result, original)

    def test_matches_basenames_and_preserves_original_paths_or_urls(self):
        prefixes = ['/cache/data/', 'relative/data/',
                    'https://archive.example/data/', 's3://bucket/data/',
                    'C:\\cache\\data\\']
        for prefix in prefixes:
            with self.subTest(prefix=prefix):
                paths = [prefix + name for name in EDP_FILES]
                self.assertEqual(last_version_per_identity(paths, MMS_PATTERN), [paths[1]])

    def test_compiled_regex_retains_flags(self):
        pattern = re.compile(r'(?P<identity>file_A)_v(?P<version>\d{2})\.cdf', re.IGNORECASE)
        files = ['FILE_A_v01.CDF', 'FILE_A_v02.CDF']
        self.assertEqual(last_version_per_identity(files, pattern), [files[1]])

    def test_other_version_formats_and_fixed_suffixes(self):
        cases = [
            (r'prefix_(?P<identity>\d{8})_v(?P<version>\d{2}_\d{2})_suffix\.cdf',
             ['prefix_20240511_v01_02_suffix.cdf', 'prefix_20240511_v01_12_suffix.cdf']),
            (r'prefix_(?P<identity>\d{8})_revision(?P<version>[A-Z])\.dat',
             ['prefix_20240511_revisionA.dat', 'prefix_20240511_revisionB.dat']),
            (r'prefix_(?P<identity>\d{8})_v(?P<version>\d{2})\.nc\.gz',
             ['prefix_20240511_v01.nc.gz', 'prefix_20240511_v02.nc.gz']),
        ]
        for pattern, files in cases:
            with self.subTest(pattern=pattern):
                self.assertEqual(last_version_per_identity(files, pattern), [files[1]])

    def test_sorting_is_deliberately_lexicographic_not_numeric(self):
        files = ['file_A_v2.10.0.cdf', 'file_A_v2.9.0.cdf']
        pattern = r'(?P<identity>file_A)_v(?P<version>\d+\.\d+\.\d+)\.cdf'
        self.assertEqual(last_version_per_identity(files, pattern), ['file_A_v2.9.0.cdf'])

    def test_invalid_regex_is_rejected_for_nonempty_lists(self):
        for pattern in ['[', '(?P<identity>', None, 3, b'(?P<identity>.*)',
                        re.compile(b'(?P<identity>.*)')]:
            with self.subTest(pattern=pattern):
                with self.assertRaisesRegex(ValueError, 'versioned_regex'):
                    last_version_per_identity([EDP_FILES[0]], pattern)

    def test_named_identity_group_is_required(self):
        for pattern in [r'(.*)_v\d+\.cdf', r'(?P<version>.*)']:
            with self.subTest(pattern=pattern):
                with self.assertRaisesRegex(ValueError, "named 'identity' group"):
                    last_version_per_identity([EDP_FILES[0]], pattern)

    def test_unmatched_files_are_rejected_instead_of_silently_dropped(self):
        for bad in ['unrelated.txt', EDP_FILES[0] + '.bak']:
            with self.subTest(filename=bad):
                with self.assertRaisesRegex(ValueError, 'does not fully match') as error:
                    last_version_per_identity([EDP_FILES[0], bad], MMS_PATTERN)
                self.assertIn(bad, str(error.exception))

    def test_fullmatch_does_not_accept_an_unmatched_prefix(self):
        pattern = r'file_(?P<identity>A)_v\d{2}\.cdf'
        with self.assertRaisesRegex(ValueError, 'does not fully match'):
            last_version_per_identity(['unexpected_file_A_v01.cdf'], pattern)

    def test_identity_must_participate_in_the_match(self):
        pattern = r'(?P<identity>file_A)?_v\d{2}\.cdf'
        with self.assertRaisesRegex(ValueError, 'No identity captured'):
            last_version_per_identity(['_v01.cdf'], pattern)

    def test_non_string_filenames_are_rejected(self):
        for files in [[None], [1], [b'file.cdf'], [EDP_FILES[0], None], b'file.cdf', b'']:
            with self.subTest(files=files):
                with self.assertRaisesRegex(TypeError, 'filenames'):
                    last_version_per_identity(files, MMS_PATTERN)


if __name__ == '__main__':
    unittest.main()
