Space Weather Follow-On (SWFO / SOLAR-1)
========================================

The SWFO plug-in loads MAG, SWiPS and STIS in situ data from the NOAA NCEI
SOLAR-1 archive into tplot variables. It reads daily netCDF files, including
files compressed with gzip. See the `NOAA SWFO documentation
<https://www.ncei.noaa.gov/products/space-weather/swfo>`_ for product descriptions
and availability. CCOR coronagraph images are outside this loader's scope.

Magnetometer (MAG)
------------------

Use ``pyspedas.projects.swfo.mag()`` to load magnetic field measurements.
Level 3 files contain both one-second and one-minute averages; each variable
retains its own time axis.

.. code-block:: python

   import pyspedas

   mag_vars = pyspedas.projects.swfo.mag(
       trange=['2026-10-01/00:00:00', '2026-10-01/01:00:00'],
       level='l3',
       varnames=['b_gse_min', 'b_gsm_min'],
       time_clip=True)
   pyspedas.tplot(mag_vars)

This creates ``swfo_mag_l3_b_gse_min`` and ``swfo_mag_l3_b_gsm_min``.

Solar Wind Plasma Sensor (SWiPS)
--------------------------------

Use ``pyspedas.projects.swfo.swips()`` to load plasma measurements. Samples
are assigned the midpoint of each instrument sweep.

.. code-block:: python

   import pyspedas

   plasma_vars = pyspedas.projects.swfo.swips(
       trange=['2026-10-01/00:00:00', '2026-10-01/01:00:00'],
       level='l2',
       varnames=['proton_n_corr', 'proton_v_corr_gse', 'proton_t_corr'],
       time_clip=True)
   pyspedas.tplot(plasma_vars)

SupraThermal Ion Sensor (STIS)
------------------------------

Use ``pyspedas.projects.swfo.stis()`` to load suprathermal ion and electron
measurements. Flux variables retain the corresponding time-dependent energy
channels and are configured as spectrograms when those coordinates are present.

.. code-block:: python

   import pyspedas

   stis_vars = pyspedas.projects.swfo.stis(
       trange=['2026-10-01/00:00:00', '2026-10-01/01:00:00'],
       level='l2',
       varnames=['electron_flux_epam_weighted_GdE'],
       time_clip=True)
   pyspedas.tplot(stis_vars)

Product selection
-----------------

The default product is operational Level 2 (``level='l2', science=False``).
Accepted levels are ``'l0b'``, ``'l1a'``, ``'l1b'``, ``'l2'`` and ``'l3'``;
not every instrument has every product for every date.

Set ``science=True`` to request retrospective science products. For STIS,
``science=True, level='l3'`` selects ``'l3-avg1m-nt-bc'`` automatically; that
explicit level is also accepted with STIS science data. The loader selects the
latest processing timestamp for each observation interval. An empty selection
returns ``[]``, or ``{}`` with ``notplot=True``.

Variable names and data quality
-------------------------------

Tplot names have the form ``swfo_<instrument>_<level>_<file_variable>``.
Science products add ``science_`` before the file variable name. A user
``prefix`` is prepended to the complete name, and ``suffix`` is appended.
For example, ``prefix='comparison_', suffix='_a'`` changes
``swfo_mag_l3_b_gse_min`` to ``comparison_swfo_mag_l3_b_gse_min_a``.

``varnames`` selects original netCDF variable names. ``varformat`` selects
those names with a wildcard pattern such as ``'proton_*'``. When both are given,
a variable must match both selections.

By default, the loader imports all numeric time-dependent variables, including
quality flags. Missing values become NaN. Quality flags are retained without
masking measurements by quality; consult the product documentation when
selecting samples for analysis.

Return arrays or downloaded files
---------------------------------

Set ``notplot=True`` to return arrays without creating tplot variables:

.. code-block:: python

   import pyspedas

   plasma = pyspedas.projects.swfo.swips(
       trange=['2026-10-01/00:00:00', '2026-10-01/01:00:00'],
       varnames=['proton_n_corr'], notplot=True, time_clip=True)
   density = plasma['swfo_swips_l2_proton_n_corr']
   times = density['x']  # Unix seconds
   values = density['y']
   metadata = density['attrs']['NETCDF']

Each entry contains ``x`` and ``y``, optional energy coordinates ``v``, and
metadata in ``attrs``. Variable and global netCDF attributes are under
``attrs['NETCDF']['VATT']`` and ``attrs['NETCDF']['GATT']``, respectively.
``time_clip=True`` restricts both tplot and dictionary output to the inclusive
requested time range. Without it, samples from the entire daily file are returned.

Set ``downloadonly=True`` to return local file paths without importing data:

.. code-block:: python

   files = pyspedas.projects.swfo.mag(
       trange=['2026-10-01', '2026-10-02'], downloadonly=True)

Cache and configuration
-----------------------

Downloaded files are cached under ``swfo_data/`` by default.
``SPEDAS_DATA_DIR`` places the cache in its ``swfo`` subdirectory;
``SWFO_DATA_DIR`` overrides that location. Preferences under
``[projects.swfo]`` are applied before environment variables.

Use ``no_update=True`` to load cached files without contacting NOAA, or set
``SWFO_NO_DOWNLOAD=true`` to enforce that behavior through configuration.
Use ``force_download=True`` to download a selected file again even if it is
already cached. Cache-only requests require the desired products to have been
downloaded previously.

API reference
-------------

The ``mag()``, ``swips()`` and ``stis()`` wrappers accept the shared loader's
keywords and set ``instrument`` to the corresponding instrument.

.. autofunction:: pyspedas.projects.swfo.load
