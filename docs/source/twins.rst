Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS) Mission
========================================================================
The routines in this module can be used to load data from the Two Wide-Angle Imaging Neutral-Atom Spectrometers (TWINS) Mission mission.


Lyman-alpha Detector (LAD)
----------------------------------------------------------
.. autofunction:: pyspedas.twins.lad

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   lad_vars = pyspedas.twins.lad(trange=['2018-11-5/6:00', '2018-11-5/6:20'], time_clip=True)
   tplot(['lad1_data', 'lad2_data'])

.. image:: _static/twins_lad.png
   :align: center
   :class: imgborder




Ephemeris
----------------------------------------------------------
.. autofunction:: pyspedas.twins.ephemeris

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   ephem_vars = pyspedas.twins.ephemeris(trange=['2018-11-5', '2018-11-6'])
   tplot('FSCGSM')

.. image:: _static/twins_ephemeris.png
   :align: center
   :class: imgborder



