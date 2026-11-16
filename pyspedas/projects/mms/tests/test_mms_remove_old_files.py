"""MMS cleanup tests: all data and server responses are local fixtures."""

import importlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests

cleanup = importlib.import_module("pyspedas.projects.mms.mms_remove_old_files")
CONTROL = "mms1_fgm_srvy_l2_20151215_v4.18.0.cdf"
OLD = "mms1_fgm_srvy_l2_20151215_v0.0.0.cdf"


def response(names=(), status=200):
    result = MagicMock(status_code=status)
    result.json.return_value = {
        "files": [{"file_name": name} for name in names],
        "files_were_truncated": False,
    }
    result.__enter__.return_value = result
    return result


class MMSRemoveOldFilesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.addCleanup(patch.stopall)
        patch.dict(cleanup.CONFIG, local_data_dir=str(self.root), mirror_data_dir=None, no_download=False).start()
        self.session = MagicMock()
        self.session.get.side_effect = self.query
        self.login = patch.object(cleanup, "mms_login_lasp", return_value=(self.session, None)).start()
        self.available = {CONTROL}
        self.visible = set()

    def query(self, url, params, **kwargs):
        if "file" in params:
            return response(set(params["file"].split(",")) & self.available)
        if params["data_level"] == "l2":
            return response([CONTROL])
        return response(self.visible)

    def create(self, name=OLD, contents=b"test", root=None):
        match = cleanup._FILENAME.fullmatch(name)
        probe, instrument, rate, level, datatype, date = match.groups()
        parts = [probe, instrument, rate, level]
        if datatype:
            parts.append(datatype)
        parts += [date[:4], date[4:6]]
        if rate == "brst":
            parts.append(date[6:8])
        path = (root or self.root).joinpath(*parts, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)
        return path

    def test_default_is_preview_with_paths_and_size(self):
        old = self.create(contents=b"12345")
        current = self.create(CONTROL)
        result = cleanup.mms_remove_old_files()
        self.assertEqual(result, {"files": [str(old)], "total_size": 5, "deleted": []})
        self.assertTrue(old.exists())
        self.assertTrue(current.exists())
        self.session.close.assert_called_once()

    def test_explicit_deletion_retains_available_old_versions(self):
        obsolete = self.create()
        retained = self.create("mms1_fgm_srvy_l2_20151215_v1.0.0.cdf")
        self.available.add(retained.name)
        result = cleanup.mms_remove_old_files(dry_run=False)
        self.assertEqual(result["deleted"], [str(obsolete)])
        self.assertFalse(obsolete.exists())
        self.assertTrue(retained.exists())

    def test_spacecraft_instrument_rate_level_and_descriptor_selection(self):
        target = self.create("mms2_fpi_brst_l2_dis-moms_20151215120000_v0.0.0.cdf")
        others = [
            self.create(),
            self.create("mms2_fpi_brst_l2_des-moms_20151215120000_v0.0.0.cdf"),
            self.create("mms2_fpi_fast_l2_dis-moms_20151215120000_v0.0.0.cdf"),
            self.create("mms2_fpi_brst_l1b_dis-moms_20151215120000_v0.0.0.cdf"),
        ]
        result = cleanup.mms_remove_old_files(
            probes=[2],
            instruments="FPI",
            data_rates="brst",
            levels=["l2"],
            datatypes="dis-moms",
            dry_run=False,
        )
        self.assertEqual(result["deleted"], [str(target)])
        self.assertTrue(all(path.exists() for path in others))

    def test_time_range_includes_start_and_excludes_end(self):
        target = self.create("mms1_fgm_brst_l2_20151215120000_v0.0.0.cdf")
        end = self.create("mms1_fgm_brst_l2_20151215130000_v0.0.0.cdf")
        earlier = self.create("mms1_fgm_brst_l2_20151215115959_v0.0.0.cdf")
        result = cleanup.mms_remove_old_files(trange=["2015-12-15/12:00", "2015-12-15/13:00"])
        self.assertEqual(result["files"], [str(target)])
        self.assertTrue(end.exists() and earlier.exists())

    def test_numeric_times_and_descriptorless_selection(self):
        old = self.create()
        self.create("mms1_fpi_srvy_l2_dis-moms_20151215_v0.0.0.cdf")
        result = cleanup.mms_remove_old_files(
            trange=[cleanup.time_double("2015-12-15"), cleanup.time_double("2015-12-16")],
            datatypes="",
        )
        self.assertEqual(result["files"], [str(old)])

    def test_version_selection_is_per_product(self):
        self.create()
        target = self.create("mms1_fgm_srvy_l2_20151215_v2.0.0.cdf")
        fpi = self.create("mms1_fpi_fast_l2_dis-moms_20151215_v1.0.0.cdf")
        result = cleanup.mms_remove_old_files(latest_version=True)
        self.assertEqual(set(result["files"]), {str(target), str(fpi)})

    def test_exact_minimum_and_major_version_selection(self):
        self.create()
        v1 = self.create("mms1_fgm_srvy_l2_20151215_v1.0.0.cdf")
        v2 = self.create("mms1_fgm_srvy_l2_20151215_v2.0.0.cdf")
        v21 = self.create("mms1_fgm_srvy_l2_20151215_v2.1.0.cdf")
        for options, expected in [
            ({"cdf_version": "1"}, [str(v1)]),
            ({"min_version": "2"}, [str(v2), str(v21)]),
            ({"major_version": True}, [str(v2), str(v21)]),
        ]:
            with self.subTest(options=options):
                self.assertEqual(cleanup.mms_remove_old_files(**options)["files"], expected)

    def test_empty_cache_and_empty_selection_do_not_log_in(self):
        self.assertEqual(cleanup.mms_remove_old_files()["files"], [])
        self.create()
        self.assertEqual(cleanup.mms_remove_old_files(probes=[])["files"], [])
        self.assertEqual(cleanup.mms_remove_old_files(cdf_version="9")["files"], [])
        self.login.assert_not_called()

    def test_invalid_time_ranges_and_dry_run_are_rejected(self):
        for trange in ["2015-12-15", [1], [2, 1], [1, 1], [1, float("nan")]]:
            with self.subTest(trange=trange), self.assertRaises(ValueError):
                cleanup.mms_remove_old_files(trange=trange)
        with self.assertRaises(TypeError):
            cleanup.mms_remove_old_files(dry_run="False")
        self.login.assert_not_called()

    def test_cloud_paths_rejected_and_offline_mode_prevents_requests(self):
        with patch.dict(cleanup.CONFIG, local_data_dir="s3://bucket/mms"), self.assertRaises(ValueError):
            cleanup.mms_remove_old_files()
        old = self.create()
        with patch.dict(cleanup.CONFIG, no_download=True), self.assertRaises(RuntimeError):
            cleanup.mms_remove_old_files(dry_run=False)
        self.assertTrue(old.exists())
        self.login.assert_not_called()

    def test_public_access_retains_non_l2_after_authentication_fallback(self):
        private = self.create("mms1_fgm_srvy_l1b_20151215_v0.0.0.cdf")
        with self.assertLogs(cleanup.logger, level="WARNING"):
            result = cleanup.mms_remove_old_files(dry_run=False)
        self.assertEqual(result["files"], [])
        self.assertTrue(private.exists())
        self.assertTrue(all("/public/" in call.args[0] for call in self.session.get.call_args_list))

    def test_authenticated_product_requires_positive_visibility(self):
        private = self.create("mms1_fgm_srvy_l1b_20151215_v0.0.0.cdf")
        self.login.return_value = self.session, "team-user"
        with self.assertLogs(cleanup.logger, level="WARNING"):
            result = cleanup.mms_remove_old_files(dry_run=False)
        self.assertEqual(result["deleted"], [])
        self.assertTrue(private.exists())
        self.visible = {"mms1_fgm_srvy_l1b_20151215_v1.0.0.cdf"}
        self.available.update(self.visible)
        result = cleanup.mms_remove_old_files(dry_run=False, always_prompt=True)
        self.assertEqual(result["deleted"], [str(private)])
        self.login.assert_called_with(always_prompt=True)
        self.assertTrue(all("/sitl/" in call.args[0] for call in self.session.get.call_args_list))

    def test_http_errors_and_redirects_never_delete(self):
        old = self.create()
        for status in [302, 401, 403, 404, 429, 500, 503]:
            with self.subTest(status=status):
                self.session.get.side_effect = [response([CONTROL]), response(status=status)]
                with self.assertRaises(RuntimeError):
                    cleanup.mms_remove_old_files(dry_run=False)
                self.assertTrue(old.exists())

    def test_restricted_access_loss_and_wrong_product_visibility_never_delete(self):
        private = self.create("mms1_fpi_fast_l1b_dis-moms_20151215_v0.0.0.cdf")
        self.login.return_value = self.session, "team-user"
        self.visible = {"mms1_fpi_fast_l1b_des-moms_20151215_v1.0.0.cdf"}
        with self.assertLogs(cleanup.logger, level="WARNING"):
            result = cleanup.mms_remove_old_files(dry_run=False)
        self.assertEqual(result["deleted"], [])
        self.visible = {"mms1_fpi_fast_l1b_dis-moms_20151215_v1.0.0.cdf"}
        # The product listing succeeds, but the subsequent filename query
        # cannot see its positive control (e.g. permission was lost).
        with self.assertRaises(RuntimeError):
            cleanup.mms_remove_old_files(dry_run=False)
        self.assertTrue(private.exists())

    def test_incomplete_or_invalid_responses_never_delete(self):
        old = self.create()
        payloads = [
            {},
            [],
            {"files": [], "files_were_truncated": True},
            {"files": [], "files_were_truncated": "false"},
            {"files": {}, "files_were_truncated": False},
            {"files": [{}], "files_were_truncated": False},
            {"files": [{"file_name": "not-an-mms-file"}], "files_were_truncated": False},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                invalid = response()
                invalid.json.return_value = payload
                self.session.get.side_effect = [response([CONTROL]), invalid]
                with self.assertRaises(RuntimeError):
                    cleanup.mms_remove_old_files(dry_run=False)
                self.assertTrue(old.exists())

    def test_invalid_json_and_network_errors_never_delete(self):
        old = self.create()
        invalid = response()
        invalid.json.side_effect = ValueError("HTML response")
        self.session.get.side_effect = [response([CONTROL]), invalid]
        with self.assertRaises(RuntimeError):
            cleanup.mms_remove_old_files(dry_run=False)
        for error in [requests.Timeout("timeout"), requests.ConnectionError("offline")]:
            self.session.get.side_effect = [response([CONTROL]), error]
            with self.assertRaises(requests.RequestException):
                cleanup.mms_remove_old_files(dry_run=False)
        self.assertTrue(old.exists())
        self.assertEqual(self.session.close.call_count, 3)

    def test_empty_health_check_or_missing_control_never_delete(self):
        old = self.create()
        for replies in [
            [response()],
            [response([CONTROL]), response()],
            [response([CONTROL]), response([CONTROL, "mms2_fgm_srvy_l2_20151215_v1.0.0.cdf"])],
        ]:
            self.session.get.side_effect = replies
            with self.assertRaises(RuntimeError):
                cleanup.mms_remove_old_files(dry_run=False)
            self.assertTrue(old.exists())

    def test_late_batch_failure_prevents_all_deletions(self):
        paths = [self.create(f"mms1_fgm_srvy_l2_20151215_v0.0.{i}.cdf") for i in range(26)]
        self.session.get.side_effect = [response([CONTROL]), response([CONTROL]), requests.Timeout()]
        with self.assertRaises(requests.Timeout):
            cleanup.mms_remove_old_files(dry_run=False)
        self.assertTrue(all(path.exists() for path in paths))

    def test_batching_and_positive_control_in_every_request(self):
        for i in range(51):
            self.create(f"mms1_fgm_srvy_l2_20151215_v0.0.{i}.cdf")
        result = cleanup.mms_remove_old_files()
        self.assertEqual(len(result["files"]), 51)
        self.assertEqual(self.session.get.call_count, 4)
        for call in self.session.get.call_args_list[1:]:
            self.assertIn(CONTROL, call.kwargs["params"]["file"].split(","))
            self.assertLessEqual(len(call.kwargs["params"]["file"].split(",")), 26)
            self.assertEqual(call.kwargs["timeout"], 30)
            self.assertFalse(call.kwargs["allow_redirects"])

    def test_changed_candidate_prevents_all_deletions(self):
        first = self.create()
        changed = self.create("mms1_fgm_srvy_l2_20151215_v1.0.0.cdf")

        def query_and_change(url, params, **kwargs):
            if "file" in params:
                changed.write_bytes(b"download replaced this file")
            return self.query(url, params, **kwargs)

        self.session.get.side_effect = query_and_change
        with self.assertRaises(RuntimeError):
            cleanup.mms_remove_old_files(dry_run=False)
        self.assertTrue(first.exists())
        self.assertTrue(changed.exists())

    def test_unrecognized_or_misplaced_files_are_ignored(self):
        self.root.joinpath(OLD).write_bytes(b"misplaced")
        path = self.create()
        path.rename(path.with_name("mms1_fgm_srvy_l2_20159999_v0.0.0.cdf"))
        path.with_name("notes.txt").write_text("notes")
        self.assertEqual(cleanup.mms_remove_old_files(dry_run=False)["files"], [])
        self.login.assert_not_called()

    def test_symbolic_files_and_directories_are_skipped(self):
        outside = self.root / "outside.cdf"
        outside.write_bytes(b"retained")
        path = self.create()
        path.unlink()
        try:
            path.symlink_to(outside)
            external = self.create("mms2_fgm_srvy_l2_20151215_v0.0.0.cdf", root=self.root / "external")
            alias = self.root / "mms2"
            alias.symlink_to(self.root / "external" / "mms2", target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symbolic links are unavailable")
        self.assertEqual(cleanup.mms_remove_old_files(dry_run=False)["files"], [])
        self.assertTrue(path.is_symlink())
        self.assertEqual(outside.read_bytes(), b"retained")
        self.assertTrue(external.exists())
        self.login.assert_not_called()

    def test_directory_replaced_by_link_during_check_aborts(self):
        path = self.create()
        backup = path.parent.with_name("backup")

        def query_and_replace(url, params, **kwargs):
            if "file" in params:
                path.parent.rename(backup)
                try:
                    path.parent.symlink_to(backup, target_is_directory=True)
                except (OSError, NotImplementedError):
                    self.skipTest("Symbolic links are unavailable")
            return self.query(url, params, **kwargs)

        self.session.get.side_effect = query_and_replace
        with self.assertRaises(RuntimeError):
            cleanup.mms_remove_old_files(dry_run=False)
        self.assertTrue(backup.joinpath(path.name).exists())

    def test_read_only_mirror_is_excluded(self):
        mirror = self.root / "mirror"
        mirrored = self.create(root=mirror)
        local = self.create()
        with patch.dict(cleanup.CONFIG, mirror_data_dir=str(mirror)):
            result = cleanup.mms_remove_old_files(dry_run=False)
        self.assertEqual(result["deleted"], [str(local)])
        self.assertTrue(mirrored.exists())
        for local_root in [mirror, mirror / "nested"]:
            with (
                patch.dict(cleanup.CONFIG, mirror_data_dir=str(mirror), local_data_dir=str(local_root)),
                self.assertRaises(ValueError),
            ):
                cleanup.mms_remove_old_files(dry_run=False)

    def test_public_exports(self):
        import pyspedas
        from pyspedas.projects.mms import mms_remove_old_files

        self.assertIs(mms_remove_old_files, cleanup.mms_remove_old_files)
        self.assertIs(pyspedas.mms_remove_old_files, cleanup.mms_remove_old_files)


if __name__ == "__main__":
    unittest.main()
