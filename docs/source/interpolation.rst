Interpolation
====================================
There are several routines for performing interpolation in pyspedas and pytplot, each designed
for slightly different use cases.

pyspedas.interpol() operates directly on arrays, not tplot variables. It is a wrapper around scipy.interpolate.interp1d().

.. autofunction:: pyspedas.interpol

pyspedas.tinterpol() operates on tplot variables, and uses the xarray interp() method internally.  It can take a list of
tplot variables and perform the interpolation on all of them.

.. autofunction:: pyspedas.tinterpol

pytplot.interp_nan() operates on single tplot variables, and uses the xarray interpolat_na() method to perform
interpolation, while ignoring sufficiently short runs of NaN values.

.. autofunction:: pytplot.interp_nan

pytplot.tinterp() operates on single tplot variables, using the xarray interp_like() method internally.

.. autofunction:: pytplot.tinterp