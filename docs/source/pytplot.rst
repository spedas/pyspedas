PyTplot
=======

PyTplot (as implemented by the pytplot-matplotlib-temp PyPI package) can be thought of as a companion package to PySPEDAS.

In the future, the pytplot tools will be migrated into the pyspedas package.  They are all available for
importing directly from the top level pyspedas module.

This section describes the tools relevant for creating plots in PySPEDAS.


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

Time Windowing and Plot Limits
-------------------------------

.. autofunction:: pyspedas.tlimit
.. autofunction:: pyspedas.timespan
.. autofunction:: pyspedas.xlim
.. autofunction:: pyspedas.ylim
.. autofunction:: pyspedas.zlim

Interactive Time Selection from Plots
--------------------------------------

The ctime routine is a close analogue of the IDL SPEDAS tool.  A call to tplot()
with return_plot_objects=True will return Matplotlib figure and axis objects that can
be passed to ctime.  During a call to ctime, a vertical time bar will track the cursor
location within the plot. Left-clicking will save that timestamp to the output list; after
selecting the desired number of points, the user can right-click to quit.  ctime will
then return the list of timestamps selected.

.. autofunction:: pyspedas.ctime

Per-Variable Plot Options
-------------------------

.. autofunction:: pyspedas.options

"Global" plot options
---------------------

.. autofunction:: pyspedas.tplot_options