"""Tests for user preference storage and CONFIG overlays."""

import os
import importlib
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

    def test_no_download_environment_overrides_toml(self):
        preferences.set_preference("themis", "no_download", True)
        config_path = Path(__file__).parents[2] / "projects" / "themis" / "config.py"
        with patch.dict(os.environ, {"THM_NO_DOWNLOAD": "false"}):
            config = runpy.run_path(str(config_path))["CONFIG"]
        self.assertFalse(config["no_download"])

    def test_no_download_default_and_preference(self):
        config = {"no_download": False}
        preferences.apply_mission_preferences(config, "themis")
        self.assertFalse(config["no_download"])

        preferences.set_preference("themis", "no_download", True)
        config = {"no_download": False}
        preferences.apply_mission_preferences(config, "themis")
        self.assertTrue(config["no_download"])

    def test_no_download_environment_rejects_invalid_boolean(self):
        config = {"no_download": False}
        with patch.dict(os.environ, {"ACE_NO_DOWNLOAD": "sometimes"}):
            with self.assertRaisesRegex(ValueError, "ACE_NO_DOWNLOAD must be true or false"):
                preferences.apply_no_download_environment(config, "ACE_NO_DOWNLOAD")

    def test_mission_no_download_reaches_download(self):
        ace_load = importlib.import_module("pyspedas.projects.ace.load")
        with patch.dict(ace_load.CONFIG, {"no_download": True}):
            with patch.object(ace_load, "download", return_value=[]) as download:
                ace_load.load(downloadonly=True)
        self.assertTrue(download.call_args.kwargs["no_download"])

    def test_existing_no_download_argument_overrides_config(self):
        ae_load = importlib.import_module("pyspedas.projects.kyoto.load_ae")
        with patch.dict(ae_load.CONFIG, {"no_download": True}):
            with patch.object(ae_load, "dailynames", return_value=["202001/test"]):
                with patch.object(ae_load, "download", return_value=[]) as download:
                    ae_load.load_ae_worker(
                        trange=["2020-01-01", "2020-01-02"],
                        datatypes=["ae"],
                        no_download=False,
                        download_only=True,
                        skip_realtime=True,
                    )
        self.assertFalse(download.call_args.kwargs["no_download"])

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
        from pyspedas.projects.mms.config import CONFIG as mms_config

        maven_values = dict(maven_config, maven_password="test-password")
        mms_values = dict(mms_config, mirror_data_dir=None)
        preferences.save_preferences("maven", maven_values)
        preferences.save_preferences("mms", mms_values)
        saved = preferences.read_preferences()["projects"]
        self.assertEqual(saved["maven"]["maven_password"], "test-password")
        self.assertNotIn("mirror_data_dir", saved["mms"])  # TOML has no null.

    def test_pyspedas_plotting_preferences(self):
        preferences.set_preference("themis", "local_data_dir", "/mission-data")
        preferences.save_preferences(
            "pyspedas.plotting",
            {"global_display": False, "plot_directory": "my_plots"},
        )
        self.assertEqual(
            preferences.read_preferences()["pyspedas"]["plotting"],
            {"global_display": False, "plot_directory": "my_plots"},
        )
        self.assertEqual(
            preferences.read_preferences()["projects"]["themis"]["local_data_dir"],
            "/mission-data",
        )
        config = {
            "plotting": {"global_display": True, "plot_directory": "pyspedas_plots"}
        }
        self.assertIs(preferences.apply_pyspedas_preferences(config), config)
        self.assertEqual(
            config["plotting"],
            {"global_display": False, "plot_directory": "my_plots"},
        )
        preferences.unset_preference("pyspedas.plotting", "plot_directory")
        self.assertNotIn(
            "plot_directory", preferences.read_preferences()["pyspedas"]["plotting"]
        )

    def test_pyspedas_plotting_types_are_validated(self):
        with self.assertRaisesRegex(TypeError, "must be bool"):
            preferences.set_preference("pyspedas.plotting", "global_display", "False")
        with self.assertRaisesRegex(ValueError, "Unknown preference"):
            preferences.set_preference("pyspedas.plotting", "unknown", "value")
        self.assertFalse(self.preference_file.exists())

    def test_pyspedas_testing_preferences(self):
        preferences.save_preferences(
            "pyspedas.testing",
            {"output_dir": "test-artifacts", "global_display": True},
        )
        config = {
            "testing": {
                "output_dir": "_testing_output",
                "validation_dir": "https://example.org/validation/",
                "global_display": False,
            }
        }
        preferences.apply_pyspedas_preferences(config)
        self.assertEqual(config["testing"]["output_dir"], "test-artifacts")
        self.assertTrue(config["testing"]["global_display"])
        self.assertEqual(
            config["testing"]["validation_dir"],
            "https://example.org/validation/",
        )

    def test_testing_environment_overrides_preferences(self):
        preferences.save_preferences(
            "pyspedas.testing",
            {"output_dir": "from-toml", "global_display": True},
        )
        with patch.dict(
            os.environ,
            {"SPEDAS_DATA_DIR": "from-data-env", "PYSPEDAS_GLOBAL_DISPLAY": "false"},
        ):
            config = runpy.run_module("pyspedas.config")["CONFIG"]
        self.assertEqual(config["testing"]["output_dir"], "from-data-env/_testing_output")
        self.assertFalse(config["testing"]["global_display"])
        with patch.dict(os.environ, {"PYSPEDAS_TESTING_DIR": "from-test-env"}):
            config = runpy.run_module("pyspedas.config")["CONFIG"]
        self.assertEqual(config["testing"]["output_dir"], "from-test-env")
        with patch.dict(
            os.environ, {"PYSPEDAS_VALIDATION_DIR": "/local/validation"}
        ):
            config = runpy.run_module("pyspedas.config")["CONFIG"]
        self.assertEqual(config["testing"]["validation_dir"], "/local/validation")

    def test_testing_display_environment_parses_false(self):
        with patch.dict(os.environ, {"PYSPEDAS_TEST_GLOBAL_DISPLAY": "False"}):
            config = runpy.run_module("pyspedas.config")["CONFIG"]
        self.assertFalse(config["testing"]["global_display"])

    def test_plot_directory_is_used_for_relative_names(self):
        from pyspedas.config import CONFIG

        save_plot_module = importlib.import_module(
            "pyspedas.tplot_tools.MPLPlotter.save_plot"
        )
        with tempfile.TemporaryDirectory() as directory:
            plot_directory = Path(directory) / "plots"
            with patch.dict(CONFIG["plotting"], {"plot_directory": str(plot_directory)}):
                with patch.object(save_plot_module.plt, "savefig") as savefig:
                    save_plot_module.save_plot(save_png="figure")
                    savefig.assert_called_once_with(
                        str(plot_directory / "figure.png"), dpi=300
                    )
                self.assertTrue(plot_directory.is_dir())
                with patch.object(save_plot_module.plt, "savefig") as savefig:
                    save_plot_module.save_plot(save_png=str(Path(directory) / "absolute.png"))
                    savefig.assert_called_once_with(
                        str(Path(directory) / "absolute.png"), dpi=300
                    )
                with patch.object(save_plot_module.plt, "savefig") as savefig:
                    save_plot_module.save_plot(save_png="existing/relative.png")
                    savefig.assert_called_once_with("existing/relative.png", dpi=300)

    def test_global_display_is_default_but_explicit_argument_wins(self):
        import matplotlib.pyplot as plt
        import pyspedas
        from pyspedas.config import CONFIG

        variable = "preference_display_test"
        pyspedas.store_data(variable, data={"x": [1, 2], "y": [3, 4]})
        self.addCleanup(pyspedas.del_data, variable)
        self.addCleanup(plt.close, "all")
        with patch.dict(CONFIG["plotting"], {"global_display": False}):
            with patch.object(plt, "show") as show:
                pyspedas.tplot(variable)
                show.assert_not_called()
                pyspedas.tplot(variable, display=True)
                show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
