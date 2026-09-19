Managing preferences
====================

PySPEDAS keeps mission defaults in each mission's ``config.py`` (or equivalent)
module. You can override existing configuration keys in a user TOML file
without editing the installed package. For example::

   [projects.themis]
   local_data_dir = "/data/themis"
   remote_data_dir = "https://spdf.gsfc.nasa.gov/pub/data/themis/"

   [pyspedas.plotting]
   global_display = false
   plot_directory = "pyspedas_plots"

   [pyspedas.testing]
   output_dir = "/data/pyspedas-tests"
   validation_dir = "https://github.com/spedas/test_data/raw/refs/heads/main/"
   global_display = false

The default file is ``preferences.toml`` in the platform's user configuration
directory (for example, ``~/.config/pyspedas/preferences.toml`` on Linux). Use
``pyspedas.preferences.preferences_path()`` to see the exact location. Set
``PYSPEDAS_CONFIG_FILE`` to use a different file, including a temporary file
for testing or a project-specific setup. A missing file is normal; PySPEDAS
does not create it until you save a preference.

The order of precedence is: explicit load-function parameter, existing
environment variable, user preference, then PySPEDAS default. A preference
cannot override an environment variable already recognized by the mission.
Only keys already present in a mission's ``CONFIG`` dictionary are supported.
This phase does not add source selection or new transport methods.

Package-wide plotting defaults live in ``pyspedas.config.CONFIG``. With no
preference file, ``global_display`` is ``true`` and ``plot_directory`` is
``pyspedas_plots`` relative to the current working directory. An omitted
``display`` argument in ``tplot``, ``tplotxy``, or ``tplotxy3`` uses
``global_display``; an explicit ``display=True`` or ``display=False`` wins.
``PYSPEDAS_GLOBAL_DISPLAY`` and ``PYSPEDAS_PLOT_DIRECTORY`` environment
variables override the corresponding TOML values.
Bare image filenames passed to ``save_png``, ``save_pdf``, and the other
plot-save arguments are placed under ``plot_directory``. Filenames that
include a directory, whether relative or absolute, are used as given. The
configured directory is created only when saving a bare filename.
``tplot_save`` data exports are not affected.

Test settings live separately in ``pyspedas.config.CONFIG["testing"]``.
``output_dir`` defaults to ``_testing_output`` relative to the current
directory and holds test plots and downloaded validation files;
``validation_dir`` points to the reference data and may also be a local path
for offline tests. Test ``global_display`` defaults to ``false``, independently
of the normal plotting default. The tests read these settings when their
modules are imported. ``PYSPEDAS_TESTING_DIR`` overrides ``output_dir``;
otherwise ``SPEDAS_DATA_DIR`` places it under that directory as
``_testing_output``. ``PYSPEDAS_VALIDATION_DIR`` overrides ``validation_dir``.
``PYSPEDAS_TEST_GLOBAL_DISPLAY`` overrides the test display setting;
``PYSPEDAS_GLOBAL_DISPLAY`` also affects it for backward compatibility.
Environment variables take precedence over TOML preferences.

Use the Python helpers to create or update the file::

   from pyspedas import preferences

   preferences.set_preference("themis", "remote_data_dir",
                              "https://spdf.gsfc.nasa.gov/pub/data/themis/")
   preferences.save_preferences("themis", {"local_data_dir": "/data/themis"})
   preferences.unset_preference("themis", "local_data_dir")
   preferences.set_preference("pyspedas.plotting", "global_display", False)
   preferences.set_preference("pyspedas.plotting", "plot_directory", "/data/plots")
   preferences.set_preference("pyspedas.testing", "output_dir", "/data/pyspedas-tests")
   print(preferences.read_preferences())

``save_preferences`` accepts a partial dictionary and preserves other keys and
missions. It also accepts a complete mission ``CONFIG`` dictionary, but doing
so stores all serializable, non-``None`` values as explicit user preferences.
Because TOML has no null value, passing ``None`` removes an override.
Credentials in a saved dictionary are written as **plaintext**; protect the
file accordingly. The writer uses an atomic replacement and preserves
unrelated TOML entries and comments.

Configuration dictionaries are populated when their modules are imported.
If you manually edit the TOML file or call a saving helper while a module is
already imported, restart Python to apply the new values. This includes
package-wide plotting settings. ``reload_preferences()`` refreshes the parsed
file for subsequent reads but does not mutate already-imported ``CONFIG``
dictionaries.

.. autofunction:: pyspedas.preferences.preferences_path
.. autofunction:: pyspedas.preferences.read_preferences
.. autofunction:: pyspedas.preferences.reload_preferences
.. autofunction:: pyspedas.preferences.save_preferences
.. autofunction:: pyspedas.preferences.set_preference
.. autofunction:: pyspedas.preferences.unset_preference
.. autofunction:: pyspedas.preferences.apply_mission_preferences
.. autofunction:: pyspedas.preferences.apply_pyspedas_preferences
