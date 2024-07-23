PyTplot
=======

PyTplot (as implemented by the pytplot-matplotlib-temp PyPI package) can be thought of as a companion package to PySPEDAS.  (In the future,
pyspedas will absorb the PyTplot tools and it will no longer have this
external dependency.

Some of the most useful and frequently used pytplot utilities are
documented below:


Tplot Variables
----------------

.. autofunction:: pytplot.get_data
.. autofunction:: pytplot.store_data
.. autofunction:: pytplot.tplot_names
.. autofunction:: pytplot.tnames

Arithmetic
----------
.. autofunction:: pytplot.tplot_math.add
.. autofunction:: pytplot.tplot_math.subtract
.. autofunction:: pytplot.tplot_math.multiply
.. autofunction:: pytplot.tplot_math.divide

Add Across Columns
------------------
.. autofunction:: pytplot.tplot_math.add_across

Average over time
-----------------
.. autofunction:: pytplot.tplot_math.avg_res_data

Clean Spikes
------------
.. autofunction:: pytplot.tplot_math.clean_spikes

Clip Data
---------
.. autofunction:: pytplot.tplot_math.clip

Crop Data
---------
.. autofunction:: pytplot.tplot_math.crop

Deflag Data
-----------
.. autofunction:: pytplot.tplot_math.deflag

Degap Data
----------
.. autofunction:: pytplot.tplot_math.degap

Derivative
----------
.. autofunction:: pytplot.tplot_math.derive

Dynamic Power Spectrum
----------------------
.. autofunction:: pytplot.tplot_math.dpwrspc

Flatten Data
------------
.. autofunction:: pytplot.tplot_math.flatten

Interpolate through NaN values
------------------------------
.. autofunction:: pytplot.tplot_math.interp_nan

Join/Split Data
---------------
.. autofunction:: pytplot.tplot_math.join_vec
.. autofunction:: pytplot.tplot_math.split_vec

Make a data gap
------------------------------
.. autofunction:: pytplot.tplot_math.makegap

Power Spectrum
--------------
.. autofunction:: pytplot.tplot_math.pwr_spec

Subtract Average/Median
-----------------------
.. autofunction:: pytplot.tplot_math.subtract_average
.. autofunction:: pytplot.tplot_math.subtract_median

Vector Dot/Cross Products
-------------------------
.. autofunction:: pytplot.tplot_math.tdotp
.. autofunction:: pytplot.tplot_math.tcrossp

Dynamic Power Spectrum of Tplot variable
-----------------------------------------
.. autofunction:: pytplot.tplot_math.tdpwrspc

Time Clip
---------
.. autofunction:: pytplot.tplot_math.time_clip

Interpolate Tplot Variables
---------------------------
.. autofunction:: pytplot.tplot_math.tinterp

Km to/from Earth Radii unit conversion
--------------------------------------
.. autofunction:: pytplot.tplot_math.tkm2re

Normalize to unit vectors
--------------------------------------
.. autofunction:: pytplot.tplot_math.tnormalize

Power Spectrum of Tplot variable
--------------------------------
.. autofunction:: pytplot.tplot_math.tpwrspc

Smooth Data
-----------
.. autofunction:: pytplot.tplot_math.tsmooth


Spectrum Multiplication
-----------------------
.. autofunction:: pytplot.tplot_math.spec_mult


Plotting
--------

tplot is the top level plotting routine.  It is now just a wrapper
for the matplotlib-specific plot routines described below.

.. autofunction:: pytplot.tplot

The matplotlib-specific version of tplot, which actually does all the work.

.. autofunction:: pytplot.MPLPlotter.tplot.tplot

Line plotting routine called by tplot. Not usually called by users,
documented here for completeness.

.. autofunction:: pytplot.MPLPlotter.lineplot.lineplot

Spectrogram plotting routine called by tplot. Not usually called by users,
docuemented here for completeness.

.. autofunction:: pytplot.MPLPlotter.specplot.specplot


Per-Variable Plot Options
-------------------------

.. autofunction:: pytplot.options

"Global" plot options
---------------------

.. autofunction:: pytplot.tplot_options