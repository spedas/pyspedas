Plotting routines
=================

In past releases of PySPEDAS, plotting utilities, and many other tools that work with tplot variables, were
imported from the external pytplot-mpl-temp package.  As of PySPEDAS 2.0, they are now bundled with PySPEDAS.

Plotting
--------

tplot is the top level plotting routine.  It uses the matplotlib plotting library to render plots of tplot variables.

.. autofunction:: pyspedas.tplot


lineplot is a line plotting routine called by tplot. It is not usually called by users,
but is documented here for completeness.

.. autofunction:: pyspedas.lineplot

specplot is a spectrogram plotting routine called by tplot. It is not usually called by users,
but is docuemented here for completeness.

.. autofunction:: pyspedas.specplot

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

At the moment, ctime does not work reliably in a Jupyter notebook when the matplotlib 'ipympl'
backend is used, or with the default 'inline' non-interactive back end.  If you are developing a notebook which
calls ctime, we recommend specifying the 'auto' backend (via the 'magic' command "%matplotlib auto") before importing
or calling any pyspedas or matplotlib routines.

.. autofunction:: pyspedas.ctime

Per-Variable Plot Options
-------------------------

.. autofunction:: pyspedas.options

.. autofunction:: pyspedas.timebar

.. autofunction:: pyspedas.databar

"Global" plot options
---------------------

.. autofunction:: pyspedas.tplot_options