"""Tests for user preference storage and CONFIG overlays."""

import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch

from pyspedas import preferences


class TestPreferences(unittest.TestCase):
    def setUp(self):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.preference_file = Path(temporary_directory.name) / "preferences.toml"
        environment = patch.dict(
            os.environ, {"PYSPEDAS_CONFIG_FILE": str(self.preference_file)}
        )
        environment.start()
        self.addCleanup(environment.stop)
        preferences.reload_preferences()
        self.addCleanup(preferences._read_file.cache_clear)

    def test_missing_file_keeps_defaults(self):
        config = {"local_data_dir": "themis_data/"}
        self.assertIs(preferences.apply_mission_preferences(config, "themis"), config)
        self.assertEqual(config["local_data_dir"], "themis_data/")
        self.assertEqual(preferences.read_preferences(), {})

    def test_overlay_and_write_preserve_other_missions(self):
        preferences.save_preferences("themis", {"local_data_dir": "/tmp/themis"})
        preferences.save_preferences("ace", {"local_data_dir": "/tmp/ace"})
        preferences.set_preference("themis", "remote_data_dir", "https://example.org/")

        config = {"local_data_dir": "themis_data/", "remote_data_dir": "default"}
        preferences.apply_mission_preferences(config, "themis")
        self.assertEqual(
            config,
            {
                "local_data_dir": "/tmp/themis",
                "remote_data_dir": "https://example.org/",
            },
        )
        self.assertEqual(
            preferences.read_preferences()["projects"]["ace"]["local_data_dir"],
            "/tmp/ace",
        )

        preferences.unset_preference("themis", "local_data_dir")
        self.assertNotIn(
            "local_data_dir", preferences.read_preferences()["projects"]["themis"]
        )

    def test_unknown_key_cannot_be_saved(self):
        with self.assertRaisesRegex(ValueError, "Unknown preference"):
            preferences.set_preference("themis", "not_a_config_key", "value")
        self.assertFalse(self.preference_file.exists())

    def test_wrong_value_type_cannot_be_saved(self):
        with self.assertRaisesRegex(TypeError, "must be str"):
            preferences.set_preference("themis", "local_data_dir", False)
        self.assertFalse(self.preference_file.exists())

    def test_invalid_file_reports_path(self):
        self.preference_file.write_text("[projects.themis\n", encoding="utf-8")
        preferences._read_file.cache_clear()
        with self.assertRaisesRegex(ValueError, "Could not read PySPEDAS preferences"):
            preferences.read_preferences()

    def test_maven_spdf_nested_section(self):
        preferences.set_preference(
            "maven.spdf", "remote_data_dir", "https://example.org/maven/"
        )
        parent = {
            "local_data_dir": "maven_data/",
            "maven_username": "",
            "maven_password": "",
        }
        preferences.apply_mission_preferences(parent, "maven")
        self.assertEqual(parent["local_data_dir"], "maven_data/")
        config = {"remote_data_dir": "default", "local_data_dir": "maven/"}
        preferences.apply_mission_preferences(config, "maven.spdf")
        self.assertEqual(config["remote_data_dir"], "https://example.org/maven/")

    def test_environment_overrides_toml(self):
        preferences.set_preference("themis", "local_data_dir", "/from/toml")
        config_path = Path(__file__).parents[2] / "projects" / "themis" / "config.py"
        with patch.dict(os.environ, {"THM_DATA_DIR": "/from/environment"}):
            config = runpy.run_path(str(config_path))["CONFIG"]
        self.assertEqual(config["local_data_dir"], "/from/environment")

    def test_comments_are_preserved(self):
        self.preference_file.write_text(
            "# A personal note\n[projects.themis]\n", encoding="utf-8"
        )
        preferences.set_preference("themis", "local_data_dir", "/tmp/themis")
        self.assertTrue(
            self.preference_file.read_text(encoding="utf-8").startswith(
                "# A personal note"
            )
        )

    def test_complete_config_dictionary_can_be_saved(self):
        from pyspedas.projects.maven.config import CONFIG as maven_config
        from pyspedas.projects.mms.mms_config import CONFIG as mms_config

        maven_values = dict(maven_config, maven_password="test-password")
        mms_values = dict(mms_config, mirror_data_dir=None)
        preferences.save_preferences("maven", maven_values)
        preferences.save_preferences("mms", mms_values)
        saved = preferences.read_preferences()["projects"]
        self.assertEqual(saved["maven"]["maven_password"], "test-password")
        self.assertNotIn("mirror_data_dir", saved["mms"])  # TOML has no null.


if __name__ == "__main__":
    unittest.main()
