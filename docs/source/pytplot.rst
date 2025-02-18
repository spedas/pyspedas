PyTplot
=======

PyTplot (as implemented by the pytplot-matplotlib-temp PyPI package) can be thought of as a companion package to PySPEDAS.

In the future, the pytplot tools will be migrated into the pyspedas package.  They are all available for
importing directly from the top level pyspedas module.

Some of the most useful and frequently used pytplot utilities are
documented below:


Tplot Variables
----------------

.. autofunction:: pyspedas.get_data
.. autofunction:: pyspedas.store_data
.. autofunction:: pyspedas.tplot_names
.. autofunction:: pyspedas.tnames

Arithmetic
----------
.. autofunction:: pyspedas.add
.. autofunction:: pyspedas.subtract
.. autofunction:: pyspedas.multiply
.. autofunction:: pyspedas.divide

.. autofunction:: pyspedas.derive
.. autofunction:: pyspedas.deriv_data

.. autofunction:: pyspedas.subtract_average
.. autofunction:: pyspedas.subtract_median


Add Across Columns
------------------
.. autofunction:: pyspedas.add_across

Clean Spikes
------------
.. autofunction:: pyspedas.clean_spikes

Clip Data Values
-----------------
.. autofunction:: pyspedas.clip

Crop Data
---------
.. autofunction:: pyspedas.crop

Deflag Data
-----------
.. autofunction:: pyspedas.deflag

Degap Data
----------
.. autofunction:: pyspedas.degap

Dynamic Power Spectrum
----------------------
.. autofunction:: pyspedas.dpwrspc

Flatten Data
------------
.. autofunction:: pyspedas.flatten

Interpolate through NaN values
------------------------------
.. autofunction:: pyspedas.interp_nan

Join/Split Data
---------------
.. autofunction:: pyspedas.join_vec
.. autofunction:: pyspedas.split_vec

Make a data gap
------------------------------
.. autofunction:: pyspedas.makegap

Power Spectrum
--------------
.. autofunction:: pyspedas.pwr_spec


Vector Dot/Cross Products
-------------------------
.. autofunction:: pyspedas.tdotp
.. autofunction:: pyspedas.tcrossp

Dynamic Power Spectrum of Tplot variable
-----------------------------------------
.. autofunction:: pyspedas.tdpwrspc

Time Clip
---------
.. autofunction:: pyspedas.time_clip

Interpolate Tplot Variables
---------------------------
.. autofunction:: pyspedas.tinterp

Km to/from Earth Radii unit conversion
--------------------------------------
.. autofunction:: pyspedas.tkm2re

Normalize to unit vectors
--------------------------------------
.. autofunction:: pyspedas.tnormalize

Power Spectrum of Tplot variable
--------------------------------
.. autofunction:: pyspedas.tpwrspc

Smooth Data
-----------
.. autofunction:: pyspedas.tsmooth


Spectrum Multiplication
-----------------------
.. autofunction:: pyspedas.spec_mult


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

.. autofunction:: pyspedas.options

"Global" plot options
---------------------

.. autofunction:: pyspedas.tplot_options