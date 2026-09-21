Galileo
=======

Load Galileo ephemeris and magnetic field data from the University of Iowa
DAS2 server into PySPEDAS tplot variables. The loader requests ASCII data and
uses the PySPEDAS DAS2 utilities to parse the response and create variables.

Quick start
-----------

.. code-block:: python

   from pyspedas import tplot
   from pyspedas.projects.galileo.load import load

   variables = load(
       trange=["1996-09-30 12:00:00", "1996-09-30 14:00:00"],
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

Select a dataset using its abbreviation or full DAS2 path. Abbreviations are
case-insensitive; full paths are case-sensitive. For example, ``magnitude``,
``MAGNITUDE``, and ``Galileo/MAG/Magnitude`` select the same dataset.

The following output names use the default prefix and no suffix.

.. list-table:: Supported Galileo datatypes
   :header-rows: 1
   :widths: 12 28 25 35

   * - **abrev**
     - **full_path**
     - **description**
     - **tplot vars loaded**
   * - ``jovicentric``
     - ``Galileo/Ephemeris/Jovicentric``
     - Galileo Jupiter orbit parameters
     - ``galileo_radius``, ``galileo_longitude``, ``galileo_mlat``, ``galileo_lt``, ``galileo_l``, ``galileo_io_phase``
   * - ``fce``
     - ``Galileo/MAG/Fce``
     - Cyclotron Electron Frequency
     - ``galileo_fce``
   * - ``magnitude``
     - ``Galileo/MAG/Magnitude``
     - Magnetic Field Magnitude
     - ``galileo_b_mag``

.. list-table:: Variables and units
   :header-rows: 1
   :widths: 18 67 15

   * - **var**
     - **description**
     - **units**
   * - radius
     - Distance from the center of Jupiter in Jovian radii
     - Rj
   * - longitude
     - Jupiter System III longitude of the sub-spacecraft point
     - degrees
   * - mlat
     - Magnetic Latitude
     - degrees
   * - lt
     - Magnetic Local time of the sub-spacecraft point
     - hours
   * - l
     - L Value
     - Rj
   * - io_phase
     - Io phase
     - degrees
   * - fce
     - Cyclotron Electron Frequency
     - Hz
   * - b_mag
     - B-Field Magnitude
     - nT

Sampling interval
-----------------

``interval`` sets the ephemeris sampling interval in seconds and defaults to
300. For ``fce`` and ``magnitude``, the loader omits the interval even when a
value is supplied, allowing the MAG datasets to use their native cadence.
All requests include ``ascii=true``.

Variable selection and naming
-----------------------------

Use ``varnames`` to select source variables from the response. Names are
case-sensitive and must exclude the output prefix and suffix. If omitted,
all variables are loaded. Selection is passed directly to the DAS2 converter;
use the exact source name, such as ``longitude``, rather than the alias
``long``.

The default prefix is ``galileo_`` for every dataset. Output names combine
that prefix, the lowercase source variable name, and the supplied ``suffix``.
A nonempty ``prefix`` replaces the entire default prefix.

.. code-block:: python

   variables = load(
       trange=["1996-06-30 00:00:00", "1996-06-30 01:00:00"],
       datatype="Galileo/MAG/Magnitude",
       prefix="custom_",
       suffix="_example",
   )
   # Output name: custom_b_mag_example

Data and metadata
-----------------

Use ``get_data`` to retrieve loaded arrays or metadata. Each variable carries
a ``DAS2`` dictionary with ``STREAM_TITLE`` for the resolved stream title and
``VATT`` for variable attributes. These entries are not displayed as plot
titles by default. Axis labels and units come from the variable descriptors
and can be adjusted using PySPEDAS ``options``.

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

   from pyspedas.projects.galileo.load import get_info

   print(get_info(datatype="fce"))

Loader reference
----------------

.. autofunction:: pyspedas.projects.galileo.load.load

.. autofunction:: pyspedas.projects.galileo.load.get_info

