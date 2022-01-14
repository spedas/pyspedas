Deep Space Climate Observatory (DSCOVR)
========================================================================
The routines in this module can be used to load data from the Deep Space Climate Observatory (DSCOVR) mission.


Magnetometer (MAG)
----------------------------------------------------------
.. autofunction:: pyspedas.dscovr.mag

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   mag_vars = pyspedas.dscovr.mag(trange=['2018-11-5', '2018-11-6'])
   tplot('dsc_h0_mag_B1GSE')

.. image:: _static/dscovr_mag.png
   :align: center
   :class: imgborder



Faraday cup (FC)
----------------------------------------------------------
.. autofunction:: pyspedas.dscovr.fc

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   fc_vars = pyspedas.dscovr.fc(trange=['2018-11-5', '2018-11-6'])
   tplot(['dsc_h1_fc_V_GSE', 'dsc_h1_fc_THERMAL_SPD', 'dsc_h1_fc_Np', 'dsc_h1_fc_THERMAL_TEMP'])

.. image:: _static/dscovr_fc.png
   :align: center
   :class: imgborder



Orbit data
----------------------------------------------------------
.. autofunction:: pyspedas.dscovr.orb

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   orb_vars = pyspedas.dscovr.orb(trange=['2018-11-5', '2018-11-6'])
   tplot(['dsc_orbit_SUN_R', 'dsc_orbit_GCI_POS', 'dsc_orbit_GCI_VEL', 'dsc_orbit_GSE_POS', 'dsc_orbit_MOON_GSE_POS'])

.. image:: _static/dscovr_orb.png
   :align: center
   :class: imgborder



Attitude data
----------------------------------------------------------
.. autofunction:: pyspedas.dscovr.att

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   att_vars = pyspedas.dscovr.att(trange=['2018-11-5', '2018-11-6'])
   tplot(['dsc_att_GSE_Yaw', 'dsc_att_GSE_Pitch', 'dsc_att_GSE_Roll'])

.. image:: _static/dscovr_att.png
   :align: center
   :class: imgborder



Load all data at once
----------------------------------------------------------
.. autofunction:: pyspedas.dscovr.all

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   all_vars = pyspedas.dscovr.all(trange=['2018-11-5', '2018-11-6'])
   tplot(['dsc_h0_mag_B1GSE', 'dsc_h1_fc_V_GSE', 'dsc_h1_fc_THERMAL_SPD', 'dsc_h1_fc_Np', 'dsc_orbit_GSE_POS'])

.. image:: _static/dscovr_all.png
   :align: center
   :class: imgborder


