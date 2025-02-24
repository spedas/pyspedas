Mars Atmosphere and Volatile Evolution (MAVEN)
========================================================================
The routines in this module can be used to load data from the Mars Atmosphere and Volatile Evolution (MAVEN) mission.


Magnetometer (MAG)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.maven.mag

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   mag_vars = pyspedas.projects.maven.mag(trange=['2014-10-18', '2014-10-19'])
   tplot('OB_B')

.. image:: _static/maven_mag.png
   :align: center
   :class: imgborder




Solar Wind Electron Analyzer (SWEA)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.maven.swea

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   swe_vars = pyspedas.projects.maven.swea(trange=['2014-10-18', '2014-10-19'])
   tplot('diff_en_fluxes_svyspec')

.. image:: _static/maven_swea.png
   :align: center
   :class: imgborder




Solar Wind Ion Analyzer (SWIA)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.maven.swia

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   swi_vars = pyspedas.projects.maven.swia(trange=['2014-10-18', '2014-10-19'])
   tplot('spectra_diff_en_fluxes_onboardsvyspec')

.. image:: _static/maven_swia.png
   :align: center
   :class: imgborder




SupraThermal And Thermal Ion Composition (STATIC)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.maven.sta

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   sta_vars = pyspedas.projects.maven.sta(trange=['2014-10-18', '2014-10-19'])
   tplot('hkp_2a-hkp')

.. image:: _static/maven_sta.png
   :align: center
   :class: imgborder




Solar Energetic Particle (SEP)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.maven.sep

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   sep_vars = pyspedas.projects.maven.sep(trange=['2014-10-18', '2014-10-19'])
   tplot('f_ion_flux_tot_s2-cal-svy-full')

.. image:: _static/maven_sep.png
   :align: center
   :class: imgborder




Langmuir Probe and Waves (LPW)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.maven.lpw

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   lpw_vars = pyspedas.projects.maven.lpw(trange=['2014-10-18', '2014-10-19'])
   tplot('mvn_lpw_lp_iv_l2_lpiv')

.. image:: _static/maven_lpw.png
   :align: center
   :class: imgborder




Extreme Ultraviolet Monitor (EUV)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.maven.euv

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot, options
   euv_vars = pyspedas.projects.maven.euv(trange=['2014-10-18', '2014-10-19'])
   options('mvn_euv_calib_bands_bands','ylog',0)
   tplot('mvn_euv_calib_bands_bands')

.. image:: _static/maven_euv.png
   :align: center
   :class: imgborder



