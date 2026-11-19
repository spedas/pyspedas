import os
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, Mock, patch
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

import pyspedas
from pyspedas.utilities.download import (
    _managed_filesystem,
    configure_retry_session,
    download,
    download_file,
    LoggingRetry,
)
from pyspedas.utilities.download_ftp import download_ftp

from pyspedas.projects.themis.config import CONFIG
# Use whichever remote server is configured for THEMIS, in case the Berkeley server is unavailable
themis_remote = CONFIG['remote_data_dir']


class DownloadTestCases(unittest.TestCase):
    def test_managed_filesystem_closes_s3_session_on_success(self):
        filesystem = Mock()
        filesystem.close = None
        filesystem.loop = Mock()
        filesystem._s3creator = Mock()

        with patch(
            "pyspedas.utilities.download.fsspec.filesystem",
            return_value=filesystem,
        ) as filesystem_factory:
            with _managed_filesystem("s3", anon=True) as result:
                self.assertIs(result, filesystem)

        filesystem_factory.assert_called_once_with(
            "s3", skip_instance_cache=True, anon=True
        )
        filesystem.close_session.assert_called_once_with(
            filesystem.loop, filesystem._s3creator
        )

    def test_managed_filesystem_closes_s3_session_on_error(self):
        filesystem = Mock()
        filesystem.close = None
        filesystem.loop = Mock()
        filesystem._s3creator = Mock()

        with patch(
            "pyspedas.utilities.download.fsspec.filesystem",
            return_value=filesystem,
        ):
            with self.assertRaisesRegex(RuntimeError, "filesystem operation failed"):
                with _managed_filesystem("s3", anon=True):
                    raise RuntimeError("filesystem operation failed")

        filesystem.close_session.assert_called_once_with(
            filesystem.loop, filesystem._s3creator
        )

    def test_download_file_streams_chunks(self):
        response = Mock(status_code=200)
        response.iter_content.return_value = [b"first", b"", b"second"]
        session = Mock()
        session.get.return_value = response

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "streamed.txt")
            result = download_file(
                url="https://example.com/streamed.txt",
                filename=filename,
                session=session,
                text_only=False,
            )

            self.assertEqual(result, filename)
            with open(filename, "rb") as downloaded_file:
                self.assertEqual(downloaded_file.read(), b"firstsecond")

        response.iter_content.assert_called_once_with(
            chunk_size=1024 * 1024, decode_unicode=False
        )
        response.close.assert_called_once()

    def test_download_file_cleans_up_temp_file_on_copy_error(self):
        response = Mock(status_code=200)
        response.iter_content.return_value = [b"content"]
        session = Mock()
        session.get.return_value = response
        real_named_temporary_file = tempfile.NamedTemporaryFile

        with tempfile.TemporaryDirectory() as temp_dir:
            def temporary_file_in_test_dir(*args, **kwargs):
                kwargs["dir"] = temp_dir
                return real_named_temporary_file(*args, **kwargs)

            with patch(
                "pyspedas.utilities.download.NamedTemporaryFile",
                side_effect=temporary_file_in_test_dir,
            ), patch(
                "pyspedas.utilities.download.copy",
                side_effect=RuntimeError("copy failed"),
            ):
                with self.assertRaisesRegex(RuntimeError, "copy failed"):
                    download_file(
                        url="https://example.com/streamed.txt",
                        filename=os.path.join(temp_dir, "destination.txt"),
                        session=session,
                        text_only=False,
                    )

            self.assertEqual(os.listdir(temp_dir), [])

        response.close.assert_called_once()

    def test_download_file_ignores_permission_error_during_temp_cleanup(self):
        response = Mock(status_code=200)
        response.iter_content.return_value = [b"content"]
        session = Mock()
        session.get.return_value = response

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "downloaded.txt")
            with patch(
                "pyspedas.utilities.download.os.unlink",
                side_effect=PermissionError("temporary file is still in use"),
            ):
                result = download_file(
                    url="https://example.com/downloaded.txt",
                    filename=filename,
                    session=session,
                    text_only=False,
                )

            self.assertEqual(result, filename)
            with open(filename, "rb") as downloaded_file:
                self.assertEqual(downloaded_file.read(), b"content")

        response.close.assert_called_once()

    def test_configure_retry_session_preserves_state(self):
        session = requests.Session()
        session.auth = ("test-user", "test-password")

        configured_session = configure_retry_session(session)

        self.assertIs(configured_session, session)
        self.assertEqual(configured_session.auth, ("test-user", "test-password"))
        retries = configured_session.adapters["https://"].max_retries
        self.assertIsInstance(retries, LoggingRetry)
        self.assertEqual(retries.total, 3)
        self.assertEqual(
            retries.status_forcelist,
            [429, 500, 502, 503, 504],
        )

    def test_configured_session_retries_429(self):
        class RetryHandler(BaseHTTPRequestHandler):
            request_count = 0

            def do_GET(self):
                RetryHandler.request_count += 1
                if RetryHandler.request_count == 1:
                    self.send_response(429)
                    self.send_header("Retry-After", "0")
                    self.end_headers()
                    return

                body = b"success"
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), RetryHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        session = configure_retry_session()
        try:
            with self.assertLogs(level="WARNING") as log:
                response = session.get(
                    f"http://127.0.0.1:{server.server_port}/mms-query"
                )
        finally:
            session.close()
            server.shutdown()
            server.server_close()
            server_thread.join()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "success")
        self.assertEqual(RetryHandler.request_count, 2)
        self.assertIn("HTTP 429", log.output[0])

    def test_return_text_retries_429(self):
        class RetryHandler(BaseHTTPRequestHandler):
            request_count = 0

            def do_GET(self):
                RetryHandler.request_count += 1
                if RetryHandler.request_count == 1:
                    self.send_response(429)
                    self.send_header("Retry-After", "0")
                    self.end_headers()
                    return

                body = b"mvn_mag_l2_20200101_v01_r01.cdf"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), RetryHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        try:
            with self.assertLogs(level="WARNING") as log:
                result = download(
                    remote_file=(
                        f"http://127.0.0.1:{server.server_port}/file_names"
                        "?instrument=mag&level=l2"
                    ),
                    return_text=True,
                )
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join()

        self.assertEqual(result, "mvn_mag_l2_20200101_v01_r01.cdf")
        self.assertEqual(RetryHandler.request_count, 2)
        self.assertIn("HTTP 429", log.output[0])
        self.assertIn("retries remaining: 2", log.output[0])
        self.assertIn("Retry-After: 0", log.output[0])

    def test_return_text_rejects_multiple_urls(self):
        with self.assertLogs(level="ERROR") as log:
            result = download(
                remote_file=["https://example.com/one", "https://example.com/two"],
                return_text=True,
            )

        self.assertIsNone(result)
        self.assertIn("supports only one remote file", log.output[0])

    def test_remote_path(self):
        # only specifying remote_path saves the files to the current working directory
        files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_remote_file(self):
        # only specifying remote_file saves the files to the current working directory
        files = download(remote_file='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_wildcard(self):
        # Test a wildcard pattern with several matches
        files = download(remote_path="https://themis.ssl.berkeley.edu/data/themis/tha/l1/state/2008/tha_l1_state_20080323_v??.cdf", last_version=False)
        self.assertTrue(len(files) == 4)  # v00, v01, v02, v03 should be available on this date
        self.assertTrue(files[3] == os.path.join(os.getcwd(), 'tha_l1_state_20080323_v03.cdf'))

    def test_missing_index(self):
        # Test a wildcard pattern on a nonexistent directory
        # This should warn "Remote index not found"
        files = download(remote_path=themis_remote+'l1/state/2006/tha_l1_state_20060323_v??.cdf')
        self.assertTrue(len(files) == 0)

    def test_last_version(self):
        # Test a wildcard pattern with several matches, and last_version=True, returning the final (lexicographic) value
        files = download(remote_path=themis_remote+'tha/l1/state/2008/tha_l1_state_20080323_v??.cdf',last_version=True)
        self.assertTrue(len(files) == 1)  # v00, v01, v02, v03 should be available on this date, should only return v03
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'tha_l1_state_20080323_v03.cdf'))

    def test_last_version_nomatch(self):
        # Test a wildcard pattern that doesn't match anything.
        # This should warn about no matching file found in the index.
        files = download(remote_path=themis_remote+'tha/l1/state/2008/tha_l1_state_20080332_v??.cdf',last_version=True)
        self.assertTrue(len(files) == 0)  # Nonexistent date, nothing should be found

    def test_remote_path_file(self):
        # specifying both remote_path and remote_file saves the files to the current working directory + the path specified in remote_file
        files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/', remote_file='psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_local_file(self):
        # specifying local_file changes the local file name
        files = download(local_file='psp_data.cdf', remote_file='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'psp_data.cdf'))

    def test_local_path(self):
        # specifying local_path changes the local data directory
        files = download(local_path='psp_data/spc/l3', remote_file='https://spdf.gsfc.nasa.gov/pub/data/psp/sweap/spc/l3/l3i/2019/psp_swp_spc_l3i_20190401_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join('psp_data/spc/l3', 'psp_swp_spc_l3i_20190401_v01.cdf'))

    def test_force_download(self):
        # specifying both remote_path and remote_file saves the files to the current working directory + the path specified in remote_file
        files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/', remote_file='themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf')
        self.assertTrue(len(files) == 1)
        self.assertTrue(files[0] == os.path.join(os.getcwd(), 'themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf'))
        # Download the same file without force_download, should not re-download
        with self.assertLogs(level='INFO') as log:
            files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/',
                             remote_file='themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf')
            self.assertIn("File is current", log.output[0])
        # Download the same file with force_download, should re-download
        with self.assertLogs(level='INFO') as log:
            files = download(remote_path='https://spdf.gsfc.nasa.gov/pub/data/',
                             remote_file='themis/tha/l1/state/2007/tha_l1_state_20070217_v01.cdf',
                             force_download=True)
            self.assertIn("Downloading", log.output[0])

    def test_cdf_to_tplot_varformat(self):
        # Check varnamea, varformat, exclude_format, and suffixes in various combinations
        # single varformat pattern
        vars = pyspedas.projects.themis.state(probe='a',varformat='*pos*')
        vars.sort()
        self.assertEqual(vars, ['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse'])
        # single varformat pattern with "|", should include both options
        vars = pyspedas.projects.themis.state(probe='a', varformat='*pos*|*vel*')
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm', 'tha_vel_sel', 'tha_vel_sse'])
        # varformat pattern with spaces, should treat as alternate patterns
        vars = pyspedas.projects.themis.state(probe='a', varformat='*pos*  *vel*')
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm', 'tha_vel_sel', 'tha_vel_sse'])
        # varformat and exclude_format patterns with spaces
        vars = pyspedas.projects.themis.state(probe='a', varformat='*pos*  *vel*', exclude_format='*sel* *sse*')
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm'])
        # varformat patterns as array, should treat as alternate patterns
        vars = pyspedas.projects.themis.state(probe='a', varformat=['*pos*','*vel*'])
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_pos_sel', 'tha_pos_sse', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm', 'tha_vel_sel', 'tha_vel_sse'])
        # varformat and exclude_format patterns as arrays
        vars = pyspedas.projects.themis.state(probe='a', varformat=['*pos*','*vel*'], exclude_format=['*sel*', '*sse*'])
        vars.sort()
        self.assertEqual(vars,['tha_pos', 'tha_pos_gse', 'tha_pos_gsm', 'tha_vel', 'tha_vel_gse', 'tha_vel_gsm'])
        # varnames with suffix specified, should return requested variables even though CDF names don't have suffix
        vars = pyspedas.projects.themis.state(probe='a',suffix='_suf', varnames=['tha_pos_suf', 'tha_pos_gse_suf'])
        vars.sort()
        self.assertEqual(vars, ['tha_pos_gse_suf', 'tha_pos_suf'])
        # varformat with suffix specified, should return values
        vars = pyspedas.projects.themis.state(probe='a',suffix='_suf', varformat=['*pos_suf', '*pos_gse_suf'])
        vars.sort()
        self.assertEqual(vars, ['tha_pos_gse_suf', 'tha_pos_suf'])
        # exclude_format with suffix specified, should remove variables with or without suffixes
        vars = pyspedas.projects.themis.state(probe='a',suffix='_suf', exclude_format=['*vel*', '*spin*','*sse*_suf', '*sel'])
        vars.sort()
        self.assertEqual(vars, ['tha_pos_gse_suf', 'tha_pos_gsm_suf', 'tha_pos_suf'])

    def test_download_ftp(self):
        from pyspedas.projects.noaa.config import CONFIG
        kp_mirror = "ftp.gfz-potsdam.de"
        remote_kp_dir = "/pub/home/obs/kp-ap/wdc/yearly/"
        local_data_dir = CONFIG['local_data_dir']
        pre = "kp"
        suf = ".wdc"
        start_year = 2019
        end_year = 2021
        # Remote names
        remote_names = [
            pre + str(year) + suf for year in range(start_year, end_year + 1)
        ]
        files=[]
        for yearstr in remote_names:
            dfile = download_ftp(
                kp_mirror,
                remote_kp_dir,
                yearstr,
                local_data_dir,
                force_download=True,
            )
            if len(dfile) > 0:
                files.append(dfile[0])
        self.assertTrue(os.path.exists(files[0]))
        self.assertTrue(os.path.exists(files[1]))
        self.assertTrue(os.path.exists(files[2]))
        # repeat download of first file to exercise 'file not modified' path
        dfile = download_ftp(
            kp_mirror,
            remote_kp_dir,
            remote_names[0],
            local_data_dir,
            force_download=False,
        )
        self.assertTrue(len(dfile) == 1)



class VersionedDownloadTests(unittest.TestCase):
    """Exercise the real wildcard selection/recursion without network traffic."""

    names = ['obs_A_v01.cdf', 'obs_A_v02.cdf', 'obs_B_v01.cdf']
    pattern = r'(?P<identity>obs_[AB])_v(?P<version>\d{2})\.cdf'

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.cache = temporary.name
        self.session = Mock()
        self.session.get.return_value = Mock(
            status_code=200,
            text=''.join(f'<a href="{name}">{name}</a>' for name in reversed(self.names)),
        )
        for name in self.names:
            open(os.path.join(self.cache, name), 'wb').close()
        pause = patch('pyspedas.utilities.download.sleep')
        pause.start()
        self.addCleanup(pause.stop)

    def run_case(self, transport, last_version, versioned_regex):
        self.session.reset_mock()
        fs = MagicMock()
        fs.glob.return_value = ['bucket/data/' + name for name in reversed(self.names)]
        fs.walk.return_value = [('bucket/cache', [], list(reversed(self.names)))]
        context = MagicMock()
        context.__enter__.return_value = fs
        remote_path = 'https://example.test/data/'
        local_path = self.cache
        kwargs = {}
        if transport.startswith('s3'):
            remote_path = 's3://bucket/data/'
        if transport == 's3_force':
            kwargs['force_download'] = True
        if transport == 's3_copy':
            local_path = 's3://bucket/cache/'
        if transport.startswith('offline'):
            kwargs['no_download'] = True
            if transport == 'offline_s3':
                local_path = 's3://bucket/cache/'
        with patch('pyspedas.utilities.download._managed_filesystem', return_value=context), patch(
                'pyspedas.utilities.download.download_file',
                side_effect=lambda **args: args['filename']) as transfer:
            result = download(remote_path=remote_path, remote_file='obs_*_v*.cdf',
                              local_path=local_path, session=self.session,
                              last_version=last_version, versioned_regex=versioned_regex, **kwargs)
        selected = self.names if not last_version else (
            ['obs_A_v02.cdf', 'obs_B_v01.cdf'] if versioned_regex else ['obs_B_v01.cdf'])
        if transport == 's3_stream':
            expected = [remote_path + name for name in selected]
        elif transport == 'offline_s3':
            expected = ['s3://bucket/cache/' + name for name in selected]
        else:
            expected = [os.path.join(local_path, name) for name in selected]
        self.assertEqual(sorted(result), expected)
        self.assertEqual(transfer.call_count, len(selected) if transport in ('http', 's3_force', 's3_copy') else 0)
        if transport != 'http':
            self.session.get.assert_not_called()

    def test_selection_across_transports(self):
        for transport in ('http', 's3_stream', 's3_force', 's3_copy', 'offline', 'offline_s3'):
            for last_version, regex in ((False, None), (False, '['), (True, None), (True, self.pattern)):
                with self.subTest(transport=transport, last_version=last_version, regex=regex):
                    self.run_case(transport, last_version, regex)

    def test_regex_filename_matching_is_independent_of_version_grouping(self):
        with patch('pyspedas.utilities.download.download_file', side_effect=lambda **args: args['filename']):
            result = download(remote_path='https://example.test/', remote_file=r'obs_.*_v.*\.cdf',
                              local_path=self.cache, session=self.session, regex=True,
                              last_version=True, versioned_regex=self.pattern)
        self.assertEqual([os.path.basename(name) for name in result], self.names[1:])

    def test_failed_transfer_uses_cache_with_selection_options(self):
        with patch('pyspedas.utilities.download.download_file', return_value=None):
            result = download(remote_path='https://example.test/', remote_file='obs_*_v*.cdf',
                              local_path=self.cache, session=self.session,
                              last_version=True, versioned_regex=self.pattern)
        self.assertEqual([os.path.basename(name) for name in result], self.names[1:])

    def test_invalid_regex_and_unmatched_candidates_fail(self):
        for regex, message in (('[', 'valid'), (r'(?P<identity>other).*', 'does not fully match')):
            for offline in (False, True):
                with self.subTest(regex=regex, offline=offline), self.assertRaisesRegex(ValueError, message):
                    download(remote_path='https://example.test/', remote_file='obs_*_v*.cdf',
                             local_path=self.cache, session=self.session, no_download=offline,
                             last_version=True, versioned_regex=regex)

    def test_empty_matches_return_empty_list(self):
        for offline in (False, True):
            with self.subTest(offline=offline):
                self.assertEqual(download(remote_path='https://example.test/', remote_file='missing*.cdf',
                                          local_path=self.cache, session=self.session, no_download=offline,
                                          last_version=True, versioned_regex=self.pattern), [])

    def test_single_candidate_is_still_validated(self):
        self.session.get.return_value.text = '<a href="obs_A_v01.cdf">file</a>'
        with self.assertRaisesRegex(ValueError, 'does not fully match'):
            download(remote_path='https://example.test/', remote_file='obs_A_v*.cdf',
                     local_path=self.cache, session=self.session, last_version=True,
                     versioned_regex=r'(?P<identity>other).*')

    def test_mms_issue_1582_fixtures_on_http_s3_and_offline(self):
        from pyspedas.utilities.tests.test_last_version_per_identity import HPCA_FILES, EDP_FILES, MMS_PATTERN
        for names, expected in ((HPCA_FILES, HPCA_FILES), (EDP_FILES, [EDP_FILES[-1]])):
            for transport in ('http', 's3', 'offline'):
                with self.subTest(transport=transport, product=names[0]), tempfile.TemporaryDirectory() as cache:
                    for name in names:
                        open(os.path.join(cache, name), 'wb').close()
                    self.session.get.return_value.text = ''.join(f'<a href="{name}">{name}</a>' for name in names)
                    context = MagicMock()
                    context.__enter__.return_value.glob.return_value = ['bucket/data/' + name for name in names]
                    with patch('pyspedas.utilities.download._managed_filesystem', return_value=context), patch(
                            'pyspedas.utilities.download.download_file', side_effect=lambda **args: args['filename']):
                        result = download(remote_path='s3://bucket/data/' if transport == 's3' else 'https://example.test/',
                                          remote_file='mms2_*.cdf', local_path=cache, session=self.session,
                                          no_download=transport == 'offline', last_version=True, versioned_regex=MMS_PATTERN)
                    self.assertEqual([name.rsplit('/', 1)[-1] for name in result], expected)


if __name__ == "__main__":
    unittest.main()
