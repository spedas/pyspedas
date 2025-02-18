Utilities
====================================

.. toctree::
   :maxdepth: 2

   time_conversion

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
.. autofunction:: pyspedas.get_ylimits
.. autofunction:: pyspedas.replace_data
.. autofunction:: pyspedas.replace_metadata
.. autofunction:: pyspedas.tplot_copy
.. autofunction:: pyspedas.tplot_rename

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
===================

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

