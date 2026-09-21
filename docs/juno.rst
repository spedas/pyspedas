Juno
====

Load Juno ephemeris and magnetic field data from the University of Iowa DAS2
server into PySPEDAS tplot variables. The loader requests ASCII data and uses
the PySPEDAS DAS2 utilities to parse the response and create the variables.

Quick start
-----------

.. code-block:: python

   from pyspedas import tplot
   from pyspedas.projects.juno.load import load

   variables = load(
       trange=["2020-02-02 12:00:00", "2020-02-02 14:00:00"],
       datatype="jovicentric",
       interval=300,
   )
   if variables:
       tplot(variables)

``load`` returns a list of the created tplot variable names. Data availability
depends on the dataset, requested time range, and server response. Supply
``trange`` as a list of start and end time strings, with the start before the
end and a duration of at most two days. A supported ``datatype`` is required.

Supported datasets
------------------

``load`` accepts the following parameters: ``trange``, ``datatype``, ``params``, ``interval``, ``varnames``, ``prefix``, ``suffix``, ``extra``

Select a dataset setting the ``datatype`` parameter to its abbreviation or to the full DAS2 path. Abbreviations are
case-insensitive; full paths are case-sensitive. For example, ``magnitude``,
``MAGNITUDE``, and ``Juno/FGM/Magnitude`` select the same dataset. 
The available ``params`` and ``interval`` values depend on the dataset. 
See the table below for details.

.. list-table:: Supported Juno datatypes
   :header-rows: 1
   :widths: 10 22 23 23 15 7

   * - **abrev**
     - **full_path**
     - **description**
     - **tplot vars**
     - **params**
     - **interval**
   * - ``europa``
     - ``Juno/Ephemeris/EuropaCoRotational``
     - Juno Europa Co-Rotational orbit
     - ``europa_x``, ``europa_y``, ``europa_z``, ``europa_radius``
     - SALT
     - Required
   * - ``ganymede``
     - ``Juno/Ephemeris/GanymedeCoRotational``
     - Juno Ganymede Co-Rotational orbit
     - ``ganymede_x``, ``ganymede_y``, ``ganymede_z``, ``ganymede_radius``
     - SALT
     - Required
   * - ``geocentric``
     - ``Juno/Ephemeris/Geocentric``
     - Juno Earth orbit parameters
     - ``geocentric_radius``, ``geocentric_mlat``, ``geocentric_mlt``, ``geocentric_l_shell``
     - None
     - Required
   * - ``heliocentric``
     - ``Juno/Ephemeris/Heliocentric``
     - Juno Solar orbit parameters
     - ``heliocentric_radius``, ``heliocentric_lon``, ``heliocentric_lat``
     - None
     - Required
   * - ``io``
     - ``Juno/Ephemeris/IoCoRotational``
     - Juno Io Co-Rotational orbit parameters
     - ``io_x``, ``io_y``, ``io_z``, ``io_radius``
     - SALT
     - Required
   * - ``jse``
     - ``Juno/Ephemeris/JSE_Attitude``
     - Juno Jupiter Solar Ecliptic Pointing angles
     - ``jse_phi``, ``jse_theta``, ``jse_omega``
     - None
     - Required
   * - ``jovicentric``
     - ``Juno/Ephemeris/Jovicentric``
     - Juno Jupiter orbit parameters
     - ``jovicentric_radius``, ``jovicentric_long``, ``jovicentric_mlat``, ``jovicentric_mlt``, ``jovicentric_l``, ``jovicentric_io_phase``
     - JLAT JALT JPLG CLAT JULT
     - Required
   * - ``electron``
     - ``Juno/FGM/ElectronCyclotron``
     - Electron Cyclotron Resonance Frequency
     - ``electron_fce``
     - None
     - None
   * - ``mag``
     - ``Juno/FGM/MagComponents``
     - Quicklook Magnetic Field Components in Payload, Planetocentric or Sun State Coordinates
     - ``mag_x``, ``mag_y``, ``mag_z``, ``mag_mag``
     - coord.eq.PC coord.eq.SS coord.eq.I_PHIO coord.eq.E_PHIO coord.eq.G_PHIO coord.eq.C_PHIO
     - None
   * - ``magnitude``
     - ``Juno/FGM/Magnitude``
     - Magnetic Field Magnitude from payload coordinates data
     - ``magnitude_mag``
     - None
     - None

Sampling and request parameters
-------------------------------

``interval`` specifies a sampling interval in seconds. Its argument defaults
to ``None``; the loader supplies 300 seconds for ephemeris datasets when it is
omitted. For ``electron``, ``mag``, and ``magnitude``, the loader omits the
interval even if a value is supplied, since these datasets have fixed sampling rates.

``params`` controls the server request and is handled by dataset:

* ``europa``, ``ganymede``, and ``io`` accept ``"SALT"``. Any other non-None
  value is replaced with ``"SALT"`` and a warning is logged.
* ``geocentric``, ``heliocentric``, and ``jse`` ignore ``params``.
* ``jovicentric`` passes ``params`` through to the server. Optional variables
  include ``JLAT``, ``JALT``, ``JPLG``, ``CLAT``, and ``JULT``; separate
  multiple names with spaces, for example ``params="JLAT CLAT JULT"``.
* ``electron`` and ``magnitude`` ignore ``params``.
* ``mag`` accepts coordinate selectors such as ``"coord.eq.PC"`` and
  ``"coord.eq.SS"``. The shortcuts ``pc``, ``ss``, ``i_phio``, ``e_phio``,
  ``g_phio``, and ``c_phio`` are matched case-insensitively and expanded to
  ``coord.eq.PC``, ``coord.eq.SS``, ``coord.eq.I_PHIO``, ``coord.eq.E_PHIO``,
  ``coord.eq.G_PHIO``, and ``coord.eq.C_PHIO``, respectively.

For example, request planetocentric magnetic field components:

.. code-block:: python

   mag_variables = load(
       trange=["2020-02-02 12:00:00", "2020-02-02 14:00:00"],
       datatype="mag",
       params="pc",
   )

``extra`` supplies additional query parameters. When omitted or empty, it
becomes ``"ascii=true"``. A custom value replaces that default; retain the
ASCII request option so the response can be parsed by the loader.

Variable selection and naming
-----------------------------

Use ``varnames`` to select source variables from the response. Names are
case-sensitive and must exclude the output prefix and suffix. If omitted,
all variables are loaded. This selection occurs after the server request;
``params`` controls what is requested from the server.

By default, output names use the dataset abbreviation followed by ``_`` and
the lowercase source variable name, such as ``jovicentric_mlat``,
``electron_fce``, or ``magnitude_mag``. A nonempty ``prefix`` replaces the
default prefix; ``suffix`` is appended to each name.

.. code-block:: python

   variables = load(
       trange=["2020-02-02T12:00:00", "2020-02-02T14:00:00"],
       datatype="magnitude",
       prefix="juno_",
       suffix="_example",
   )
   # Output name: juno_mag_example

Data and metadata
-----------------

Use ``get_data`` to retrieve loaded arrays or metadata. Each variable carries
a ``DAS2`` dictionary with ``STREAM_TITLE`` for the resolved stream title and
``VATT`` for variable attributes. These entries are not displayed as plot
titles by default. Axis labels and units come from the variable descriptors.

.. code-block:: python

   from pyspedas import get_data

   if variables:
       data = get_data(variables[0])
       metadata = get_data(variables[0], metadata=True)
       print(metadata)
       stream_title = metadata["DAS2"]["STREAM_TITLE"]
       variable_attributes = metadata["DAS2"]["VATT"]

Dataset information
-------------------

``get_info`` retrieves a dataset's Data Source Definition File as response
text. Supply a supported abbreviation or exact full path, using the same
selection rules as ``load``. An empty or unsupported selector raises
``ValueError``; a non-string selector raises ``TypeError``. An unsuccessful
server request returns an empty string.

.. code-block:: python

   from pyspedas.projects.juno.load import get_info

   print(get_info(datatype="magnitude"))

Browser access for raw data
---------------------------

An example URL for the Juno DAS2 server is:

https://jupiter.physics.uiowa.edu/das/server?server=dataset&dataset=Juno/Ephemeris/Jovicentric&start_time=2020-02-02T12:00:00.000Z&end_time=2020-02-02T14:00:00.000Z&interval=300&ascii=true

This dataset URL can be opened in a web browser to view the raw ASCII response.

Using PySPEDAS DAS2 utilities, the same data can be loaded into tplot variables and plotted with:

.. code-block:: python

   from pyspedas import tplot
   from pyspedas.projects.juno.load import load

   vars = load(
       trange=["2020-02-02 12:00:00", "2020-02-02 14:00:00"],
       datatype="jovicentric",
       interval=300,
   )
   tplot(vars)


Loader reference
----------------

.. autofunction:: pyspedas.projects.juno.load.load

.. autofunction:: pyspedas.projects.juno.load.get_info

