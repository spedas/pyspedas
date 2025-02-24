Wind
========================================================================
The routines in this module can be used to load data from the Wind mission.


Magnetic Field Investigation (MFI)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.wind.mfi

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   mfi_vars = pyspedas.projects.wind.mfi(trange=['2013-11-5', '2013-11-6'])
   tplot('BGSE')

.. image:: _static/wind_mfi.png
   :align: center
   :class: imgborder



Solar Wind Experiment (SWE)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.wind.swe

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   swe_vars = pyspedas.projects.wind.swe(trange=['2013-11-5', '2013-11-6'])
   tplot(['N_elec', 'T_elec'])

.. image:: _static/wind_swe.png
   :align: center
   :class: imgborder



Radio and Plasma Waves (WAVES)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.wind.waves

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   waves_vars = pyspedas.projects.wind.waves(trange=['2013-11-5', '2013-11-6'])
   tplot(['E_VOLTAGE_RAD2', 'E_VOLTAGE_RAD1', 'E_VOLTAGE_TNR'])

.. image:: _static/wind_waves.png
   :align: center
   :class: imgborder



3D Plasma Analyzer (3DP)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.wind.threedp

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   threedp_vars = pyspedas.projects.wind.threedp()
   tplot(['V_e_xyz_gse_wi_3dp', 'N_e_dens_wi_3dp', 'T_e_par_wi_3dp'])

.. image:: _static/wind_threedp.png
   :align: center
   :class: imgborder



Solar Wind and Suprathermal Ion Composition Experiment (SMS)
-------------------------------------------------------------
.. autofunction:: pyspedas.projects.wind.sms

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   sms_vars = pyspedas.projects.wind.sms()
   tplot(['C_ion_temp', 'O_ion_temp'])

.. image:: _static/wind_sms.png
   :align: center
   :class: imgborder



Orbit data
----------------------------------------------------------
.. autofunction:: pyspedas.projects.wind.orbit

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   orb_vars = pyspedas.projects.wind.orbit(trange=['2013-11-5', '2013-11-6'])
   tplot(['GSE_POS', 'GSE_VEL', 'GSM_POS', 'GSM_VEL'])

.. image:: _static/wind_orbit.png
   :align: center
   :class: imgborder


