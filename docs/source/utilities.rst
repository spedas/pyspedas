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

.. autofunction:: pyspedas.tai2unix(tinput)

.. autofunction:: pyspedas.unix2tai(tinput)

Creating and Managing Tplot Variables
-------------------------------------

.. autofunction:: pyspedas.get_data

A few notes about get_data:

The type of the return value will differ depending on what is being requested.   If metadata=True is
passed, the return value will be a dictionary containing the various metadata attributes, CDF metadata, plot
options, and so forth.  Otherwise, the returned value will be a Python tuple, with a number of named fields.
The first two fields returned will always be 'times' (the timestamps or X values), and 'y' (the data values).
There may be additional fields, depending on whether v, v1, v2 (etc) attributes are defined for higher
dimensional data types.  So be cautious about constructs like this:

``mytimes, myvals = get_data('some_tplot_variable')``

If 'some_tplot_variable' contains 'v', 'v1'. 'v2', or other DEPEND_N attributes, this will cause errors or
warnings like 'too many values to unpack'.  Unless you already know how much metadata to expect,
it's safer to do this:

``mydata = get_data('some_tplot_variable')``

then reference ``mydata.times``, ``mydata.y``, ``mydata.v``, etc.

In some cases, due to the internal represenation of tplot variables as xarray and pandas objects,
the arrays returned by get_data may be read-only views of pandas indexes or other parts of the data
structure.  At this writing (January 2026), if pandas-3.0.0 or above is installed in the PySPEDAS environment,
the time and data arrays returned by get_data should always be writeable, but the v, v1`, v2 (etc) elements might be read-only.
In the (somewhat rare) case where you need to modify the returned arrays, you can specify ``ensure_writeable=True``
in the get_data call. In this case, get_data will return read-write copies of the arrays, rather than read-only
views.  The default setting is ``ensure_writeable=False``, to avoid unnecessary copies and save memory.


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
.. autofunction:: pyspedas.tplot_wildcard_expand

Tplot Variable Metadata Getters/Setters
----------------------------------------

Some PySPEDAS routines (for example, coordinate transforms and magnetic field models)
need access to certain metadata to operate properly.  When loading from external data sources,
this is often taken care of automatically, but if your code needs to create its own tplot variables
or inspect metadata for input variables, these routines can help.

.. autofunction:: pyspedas.get_coords
.. autofunction:: pyspedas.set_coords
.. autofunction:: pyspedas.rotmat_set_coords
.. autofunction:: pyspedas.rotmat_get_coords
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

There are several routines for performing interpolation in PySPEDAS, each designed
for slightly different use cases.

pyspedas.tinterpol_mxn() interpolates along time independently for each component
of a scalar, vector, matrix, or higher-dimensional series. It accepts tplot names
(including lists and wildcards) or dictionaries containing ``x`` and ``y``.
This initial implementation supports linear interpolation only. Existing
interpolation routines remain unchanged.

Like IDL SPEDAS, the default is to extrapolate. Use ``nan_extrapolate=True`` to
keep the target grid and fill outside source coverage with NaNs,
``no_extrapolate=True`` to trim it, or ``repeat_extrapolate=True`` to repeat
first/last finite values per component. These options are mutually exclusive.
``ignore_nans=True`` removes NaNs independently for each component; this may
extrapolate beyond that component's valid samples even inside the original
source time coverage. No maximum gap duration is imposed.

For example::

    import numpy as np
    import pyspedas

    # Three matrix-valued samples; interpolate each matrix element in time.
    matrices = np.arange(27).reshape(3, 3, 3)
    result = pyspedas.tinterpol_mxn(
        {'x': [0, 2, 4], 'y': matrices}, [1, 3])
    assert result['y'].shape == (2, 3, 3)

    pyspedas.store_data('input', data={'x': [0, 2], 'y': [0, 4]})
    names = pyspedas.tinterpol_mxn(
        'input', [-1, 1, 3], nan_extrapolate=True)
    # Creates input_interp with values [NaN, 2, NaN].
    data = pyspedas.tinterpol_mxn('input', [1], return_data=True)
    # Returns a dictionary without creating a tplot variable.

Returned dictionary times use ``datetime64[ns]``. Static dependency coordinates
are copied. Time-dependent ``v``, ``v1``, ``v2``, and ``v3`` bins (including the
``spec_bins`` alias) repeat the bin map at the latest source time at or before
each target time. Exact transition times select the new map. Bin-map NaNs are
retained even with ``ignore_nans=True``. Outside coverage, default extrapolation
and repeat extrapolation retain endpoint maps; NaN extrapolation fills with NaNs
and no extrapolation trims the grid. Y values remain linearly interpolated across
bin changes, without rebinning or suppressing interpolation at mode transitions.
Tplot output preserves coordinate attributes, data metadata and plot options, while updating
time and value ranges. Matrix interpolation is component-wise and does not
preserve special constraints such as rotation-matrix orthogonality.

Intentional differences from IDL include preserving exact valid samples next to
NaNs, trimming each source independently in a batch, consistently applying
repeat filling to tensors, and using previous bin maps instead of interpolating
them linearly. Invalid options and inputs raise Python exceptions. Stored results return a list of names; empty trimmed
results are skipped, while returned-data mode returns empty arrays.

.. autofunction:: pyspedas.tinterpol_mxn

pyspedas.interpol() operates directly on arrays, not tplot variables. It is a wrapper around scipy.interpolate.interp1d().

.. autofunction:: pyspedas.interpol

pyspedas.tinterpol() operates on tplot variables, and uses the xarray interp() method (which itself uses scipy.interp1d) internally.  It can take a list of
tplot variables and perform the interpolation on all of them.

.. autofunction:: pyspedas.tinterpol

pyspedas.interp_nan() operates on single tplot variables, and uses the xarray interpolate_na() method to perform
interpolation through NaN values. Use ``max_gap_time`` to limit the duration of
filled gaps in seconds, or ``max_gap_samples`` to limit the number of consecutive
NaNs filled. Both limits can be used together. The deprecated ``s_limit`` argument
now follows its documented meaning in seconds and is an alias for ``max_gap_time``;
use ``max_gap_samples`` to retain the previous sample-count behavior.

.. autofunction:: pyspedas.interp_nan

pyspedas.tinterp() operates on single tplot variables, using the xarray interp_like() method internally.

.. autofunction:: pyspedas.tinterp


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

File Format Readers/Writers
----------------------------

.. autofunction:: pyspedas.tplot_ascii
.. autofunction:: pyspedas.tplot_save
.. autofunction:: pyspedas.cdf_to_tplot
.. autofunction:: pyspedas.netcdf_to_tplot
.. autofunction:: pyspedas.sts_to_tplot
.. autofunction:: pyspedas.tplot_restore

Miscellaneous utilities
------------------------

.. autofunction:: pyspedas.find_datasets
.. autofunction:: pyspedas.find_ip_address
.. autofunction:: pyspedas.is_gzip
.. autofunction:: pyspedas.libs
.. autofunction:: pyspedas.wildcard_expand
.. autofunction:: pyspedas.mpause_2
.. autofunction:: pyspedas.mpause_t96


