Utilities
====================================

.. toctree::
   :maxdepth: 2

Time Conversions
----------------

Most routines in PySPEDAS will accept or produce times in one of two representations: either
as floating-point values interpreted as a count of seconds since the Unix
epoch 1970-01-01/00:00  (often called "Unix time"), or as strings, for example '2018-04-01/12:00:00.001'.

The PySPEDAS time_string(), time_float(), and time_double() can be used
to convert single timestamps, or lists or arrays of timestamps, between these
representations.

The format of PySPEDAS timestamps is somewhat flexible...basically enything
that can be handled via the dateutil.parser parse() or isoparse() utilities.

Internally, PySPEDAS currently uses Numpy datetime64() objects with nanosecond precision
as the time representation of tplot variables and Matplotlib plots.  This is an
implementation detail that should not be relied on in user code!  The PySPEDAS get_data
and store_data() routines (described below) for using and creating tplot variables
do the appropriate conversions between the internal time representation and
the Unix times or string timestamps used elsewhere in PySPEDAS.

The use of Unix times in much of PySPEDAS (and indeed, Python in general) leads to potential pitfalls when
dealing with leap seconds, which are by definition ignored when converting between
Unix times and string timestamps.  This is a bit of a sore point in the scientific
Python community.  The Astropy package has one of the few fully leap-second-aware time representations,
but the lack of support for it in commonly used scientific Python packages (e.g. Numpy, Pandas, xarray)
are a hindrance to adopting it as a common time representation in PySPEDAS and
elsewhere in the PyHC ecosystem.


.. autofunction:: pyspedas.time_string
   :no-index:

Example
^^^^^^^^^

.. code-block:: python

   from pyspedas import time_string
   time_string(1444953600.0)

.. code-block:: python

   '2015-10-16 00:00:00.000000'

.. autofunction:: pyspedas.time_double
   :no-index:

Example
^^^^^^^^^

.. code-block:: python

   from pyspedas import time_double
   time_double('2015-10-16/14:00')

.. code-block:: python

   1445004000.0



There may be occasions (for example, when passing times to routines
in other packages) when it might be useful to convert to/from Python datetime
objects. time_datetime() accepts either Unix times or strings, and returns Python datetime objects.

.. autofunction:: pyspedas.time_datetime
   :no-index:

Example
^^^^^^^^^

.. code-block:: python

   from pyspedas import time_datetime
   time_datetime('2015-10-16/14:00')


.. code-block:: python

   datetime.datetime(2015, 10, 16, 14, 0, tzinfo=datetime.timezone.utc)


.. autofunction:: pyspedas.time_ephemeris

Creating and Managing Tplot Variables
-------------------------------------

.. autofunction:: pyspedas.get_data
.. autofunction:: pyspedas.store_data
.. autofunction:: pyspedas.tplot_names
.. autofunction:: pyspedas.tnames
.. autofunction:: pyspedas.join_vec
.. autofunction:: pyspedas.split_vec
.. autofunction:: pyspedas.del_data
.. autofunction:: pyspedas.data_exists
.. autofunction:: pyspedas.get_timespan
.. autofunction:: pyspedas.tres
.. autofunction:: pyspedas.get_ylimits
.. autofunction:: pyspedas.replace_data
.. autofunction:: pyspedas.replace_metadata
.. autofunction:: pyspedas.tplot_copy
.. autofunction:: pyspedas.tplot_rename

Tplot Variable Metadata Getters/Setters
----------------------------------------

Some PySPEDAS routines (for example, coordinate transforms and magnetic field models)
need access to certain metadata to operate properly.  When loading from external data sources,
this is often taken care of automatically, but if your code needs to create its own tplot variables
or inspect metadata for input variables, these routines can help.

.. autofunction:: pyspedas.get_coords
.. autofunction:: pyspedas.set_coords
.. autofunction:: pyspedas.get_units
.. autofunction:: pyspedas.set_units

Arithmetic
----------
.. autofunction:: pyspedas.add
.. autofunction:: pyspedas.subtract
.. autofunction:: pyspedas.multiply
.. autofunction:: pyspedas.divide

.. autofunction:: pyspedas.add_across
.. autofunction:: pyspedas.avg_data
.. autofunction:: pyspedas.derive
.. autofunction:: pyspedas.deriv_data
.. autofunction:: pyspedas.tkm2re
.. autofunction:: pyspedas.avg_res_data
.. autofunction:: pyspedas.flatten
.. autofunction:: pyspedas.subtract_average
.. autofunction:: pyspedas.subtract_median

Matrix/Vector Operations
-------------------------
.. autofunction:: pyspedas.tdotp
.. autofunction:: pyspedas.tcrossp
.. autofunction:: pyspedas.tnormalize
.. autofunction:: pyspedas.tvector_rotate
.. autofunction:: pyspedas.tvectot


Data Cleanup Operations
------------------------

.. autofunction:: pyspedas.clean_spikes
.. autofunction:: pyspedas.clip
.. autofunction:: pyspedas.crop
.. autofunction:: pyspedas.time_clip
.. autofunction:: pyspedas.deflag
.. autofunction:: pyspedas.degap
.. autofunction:: pyspedas.makegap
.. autofunction:: pyspedas.tsmooth

Interpolation Tools
--------------------

There are several routines for performing interpolation in pyspedas and pytplot, each designed
for slightly different use cases.

pyspedas.interpol() operates directly on arrays, not tplot variables. It is a wrapper around scipy.interpolate.interp1d().

.. autofunction:: pyspedas.interpol

pyspedas.tinterpol() operates on tplot variables, and uses the xarray interp() method (which itself uses scipy.interp1d) internally.  It can take a list of
tplot variables and perform the interpolation on all of them.

.. autofunction:: pyspedas.tinterpol

pytplot.interp_nan() operates on single tplot variables, and uses the xarray interpolat_na() method to perform
interpolation, while ignoring sufficiently short runs of NaN values.

.. autofunction:: pytplot.interp_nan

pytplot.tinterp() operates on single tplot variables, using the xarray interp_like() method internally.

.. autofunction:: pytplot.tinterp


Wave, Polarization, Power Spectrum operations
---------------------------------------------
.. autofunction:: pyspedas.dpwrspc
.. autofunction:: pyspedas.twavpol
.. autofunction:: pyspedas.pwr_spec
.. autofunction:: pyspedas.pwrspc
.. autofunction:: pyspedas.tpwrspc
.. autofunction:: pyspedas.tdpwrspc
.. autofunction:: pyspedas.spec_mult

Download utilities
-------------------

.. autofunction:: pyspedas.download
.. autofunction:: pyspedas.download_ftp
.. autofunction:: pyspedas.dailynames
.. autofunction:: pyspedas.load_leap_table

Miscellaneous utilities
------------------------

.. autofunction:: pyspedas.find_datasets
.. autofunction:: pyspedas.find_ip_address
.. autofunction:: pyspedas.is_gzip
.. autofunction:: pyspedas.libs
.. autofunction:: pyspedas.mpause_2
.. autofunction:: pyspedas.mpause_t96


