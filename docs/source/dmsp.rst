Defense Meteorological Satellite Program (DMSP)
===============================================

The DMSP loaders retrieve space physics CDF products from the
`NASA SPDF DMSP archive <https://spdf.gsfc.nasa.gov/pub/data/dmsp/>`_.

.. list-table:: Supported instruments and spacecraft
   :header-rows: 1
   :widths: 15 50 35

   * - Loader
     - Measurements
     - Spacecraft
   * - ``ssj()``
     - Precipitating electrons and ions
     - F06-F09, F12-F18
   * - ``ssies()``
     - SSIES-3 thermal plasma
     - F16-F18
   * - ``ssm()``
     - Magnetic field
     - F15-F18

Coverage varies by spacecraft and instrument. SSJ and SSM files contain daily
measurements; SSIES files cover individual orbits. The loaders retain every
matching orbit and select the newest available version of each file.

.. note::

   The SPDF F19 archive contains SSUSI products only. These loaders do not
   support SSUSI or the F19 particle observations discussed in
   `issue #1299 <https://github.com/spedas/pyspedas/issues/1299>`_.

Common options
--------------

Use ``probe=18``, ``probe='18'``, or ``probe='f18'`` to select a spacecraft.
A list, such as ``probe=['16', '18']``, selects multiple spacecraft. Original
CDF variable names are preserved, so use separate calls with distinct
``prefix`` values when spacecraft share variable names.

All three loaders support ``trange``, ``prefix``, ``suffix``,
``get_support_data``, ``varformat``, ``varnames``, ``downloadonly``, ``notplot``,
``no_update``, ``time_clip``, and ``force_download``. By default, they return
names of imported tplot variables. ``downloadonly=True`` returns local file
paths, and ``notplot=True`` returns data dictionaries without creating tplot
variables. ``time_clip=True`` clips tplot variables to the requested range;
it does not clip dictionaries returned by ``notplot=True``.

The default cache directory is ``dmsp_data/``. Mission preferences can change
it; ``SPEDAS_DATA_DIR`` places the cache in a ``dmsp`` subdirectory, and
``DMSP_DATA_DIR`` overrides that location. ``DMSP_NO_DOWNLOAD=1`` disables
network downloads, and ``no_update=True`` uses only cached files for a call.
See :doc:`projects` for shared loader conventions.

Precipitating electrons and ions (SSJ)
--------------------------------------

.. autofunction:: pyspedas.projects.dmsp.ssj

Example
^^^^^^^

.. code-block:: python

   import pyspedas

   variables = pyspedas.projects.dmsp.ssj(
       trange=['2014-01-01', '2014-01-02'],
       probe='18', prefix='f18_', time_clip=True)
   pyspedas.tplot(variables)

Thermal plasma (SSIES)
----------------------

.. autofunction:: pyspedas.projects.dmsp.ssies

Example
^^^^^^^

.. code-block:: python

   import pyspedas

   variables = pyspedas.projects.dmsp.ssies(
       trange=['2014-01-01', '2014-01-02'],
       probe='18', prefix='f18_', time_clip=True)
   pyspedas.tplot(variables)

Magnetometer (SSM)
------------------

.. autofunction:: pyspedas.projects.dmsp.ssm

Example
^^^^^^^

.. code-block:: python

   import pyspedas

   variables = pyspedas.projects.dmsp.ssm(
       trange=['2015-03-01', '2015-03-02'],
       probe='18', prefix='f18_', time_clip=True)
   pyspedas.tplot(variables)
