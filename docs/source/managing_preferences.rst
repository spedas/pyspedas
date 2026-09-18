Managing preferences
====================

PySPEDAS keeps mission defaults in each mission's ``config.py`` (or equivalent)
module. You can override existing configuration keys in a user TOML file
without editing the installed package. For example::

   [projects.themis]
   local_data_dir = "/data/themis"
   remote_data_dir = "https://spdf.gsfc.nasa.gov/pub/data/themis/"

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

Use the Python helpers to create or update the file::

   from pyspedas import preferences

   preferences.set_preference("themis", "remote_data_dir",
                              "https://spdf.gsfc.nasa.gov/pub/data/themis/")
   preferences.save_preferences("themis", {"local_data_dir": "/data/themis"})
   preferences.unset_preference("themis", "local_data_dir")
   print(preferences.read_preferences())

``save_preferences`` accepts a partial dictionary and preserves other keys and
missions. It also accepts a complete mission ``CONFIG`` dictionary, but doing
so stores all serializable, non-``None`` values as explicit user preferences.
Because TOML has no null value, passing ``None`` removes an override.
Credentials in a saved dictionary are written as **plaintext**; protect the
file accordingly. The writer uses an atomic replacement and preserves
unrelated TOML entries and comments.

Configuration dictionaries are populated when their mission modules are
imported. If you manually edit the TOML file or call a saving helper while a
mission is already imported, restart the Python process to apply the new
values to that mission. ``reload_preferences()`` refreshes the parsed file for
subsequent reads but does not mutate already-imported ``CONFIG`` dictionaries.

.. autofunction:: pyspedas.preferences.preferences_path
.. autofunction:: pyspedas.preferences.read_preferences
.. autofunction:: pyspedas.preferences.reload_preferences
.. autofunction:: pyspedas.preferences.save_preferences
.. autofunction:: pyspedas.preferences.set_preference
.. autofunction:: pyspedas.preferences.unset_preference
.. autofunction:: pyspedas.preferences.apply_mission_preferences
