Kyoto Dst
========================================================================
The routines in this module can be used to load Kyoto Dst data from the World Data Center for Geomagnetism, Kyoto.


Load the data
----------------------------------------------------------
.. autofunction:: pyspedas.projects.kyoto.dst

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   dst_vars = pyspedas.projects.kyoto.dst(trange=['2018-11-5', '2018-11-6'])
   tplot('kyoto_dst')

.. image:: _static/kyoto_dst.png
   :align: center
   :class: imgborder



