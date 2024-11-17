Solar Terrestrial Relations Observatory (STEREO)
========================================================================
The routines in this module can be used to load data from the Solar Terrestrial Relations Observatory (STEREO) mission.


Magnetometer (MAG)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.mag

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   mag_vars = pyspedas.projects.stereo.mag(trange=['2013-11-5', '2013-11-6'])
   tplot('BFIELD')

.. image:: _static/stereo_mag.png
   :align: center
   :class: imgborder


Solar Wind Electron Analyzer (SWEA)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.swea


Suprathermal Electron Telescope (STE)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.ste


Solar Electron Proton Telescope (SEPT)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.sept


Suprathermal Ion Telescope (SIT)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.sit


Low Energy Telescope (LET)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.let


High Energy Telescope (HET)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.het


PLAsma and SupraThermal Ion Composition (PLASTIC)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.stereo.plastic

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   plastic_vars = pyspedas.projects.stereo.plastic(trange=['2013-11-5', '2013-11-6'])
   tplot(['proton_number_density', 'proton_bulk_speed', 'proton_temperature', 'proton_thermal_speed'])

.. image:: _static/stereo_plastic.png
   :align: center
   :class: imgborder



