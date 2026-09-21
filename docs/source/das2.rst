Load Data via DAS2
==================

The utilities in ``pyspedas.utilities.das2`` request dataset information and
ASCII data from DAS2 servers, parse the responses, and create tplot variables.
They support the DAS 2.1 server API with ASCII responses. Parsing is currently
limited to scalar time series; binary data and spectra are not supported.
Coordinate systems are not inferred from the dataset.

Find datasets
-------------

Use ``das2info`` with ``server="list"`` to list available datasets,
``server="peers"`` to list peer servers, or ``server="dsdf"`` to retrieve a
dataset's Data Source Definition File. The ``dsdf`` request also requires a
dataset identifier. Results are returned as response text.

.. code-block:: python

   from pyspedas.utilities.das2.das2info import das2info

   url = "https://jupiter.physics.uiowa.edu/das/server"
   print(das2info(url=url, server="list"))
   print(das2info(
       url=url,
       server="dsdf",
       dataset="Juno/Ephemeris/Jovicentric",
   ))

Download and plot data
----------------------

Use ``das2ascii`` with ``server="dataset"`` to download response text, then
pass that text to ``das2tplot`` to create tplot variables. The server URL must
start with ``https://``. The default ``extra="ascii=true"`` requests ASCII
output. Optional ``interval`` and ``params`` arguments are passed to the
server; their supported values depend on the dataset.

.. code-block:: python

   from pyspedas import tplot
   from pyspedas.utilities.das2.das2ascii import das2ascii
   from pyspedas.utilities.das2.das2tplot import das2tplot

   data = das2ascii(
       url="https://jupiter.physics.uiowa.edu/das/server",
       server="dataset",
       dataset="Juno/Ephemeris/Jovicentric",
       start_time="2020-01-01T01:00:00",
       end_time="2020-01-01T02:00:00",
       interval=300,
       extra="ascii=true",
   )

   if data:
       variables = das2tplot(data, prefix="jovicentric_")
       if variables:
           tplot(variables)

``das2ascii`` returns an empty string for a missing or non-HTTPS URL, a
non-200 HTTP response, or a Requests network exception. ``das2info`` also
returns an empty string for an invalid information request.

Variable selection and metadata
-------------------------------

``das2tplot`` returns the names of successfully created tplot variables.
Output names are ``prefix + source_name.lower() + suffix``. Its ``varnames``
argument accepts a source variable name or a list of names, matched exactly
and case-sensitively before output names are lowercased. ``None``, an empty
list, ``"*"``, or ``""`` selects all variables.

Variable ``yLabel`` and ``units`` attributes supply the plot's y-axis title
and subtitle. Common Autoplot formatting codes are converted to readable
text, for example ``R!bJ!n`` becomes ``R_J``. Each variable also stores a
``DAS2`` metadata dictionary containing ``STREAM_TITLE`` (the resolved stream
title) and ``VATT`` (the variable attributes). These metadata entries do not
appear on the plot by default but can be accessed programmatically, for example:

.. code-block:: python

   from pyspedas import get_data

   if variables:
       data = get_data(variables[0])
       metadata = get_data(variables[0], metadata=True)
       print(metadata)
       stream_title = metadata["DAS2"]["STREAM_TITLE"]
       variable_attributes = metadata["DAS2"]["VATT"]


Function reference
------------------

.. autofunction:: pyspedas.utilities.das2.das2ascii.das2ascii

.. autofunction:: pyspedas.utilities.das2.das2info.das2info

.. autofunction:: pyspedas.utilities.das2.das2tplot.das2tplot
