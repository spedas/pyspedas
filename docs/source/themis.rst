Time History of Events and Macroscale Interactions during Substorms (THEMIS)
==============================================================================
The routines in this module can be used to load data from the Time History of Events and Macroscale Interactions during Substorms (THEMIS) mission.


Fluxgate magnetometer (FGM)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.fgm

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   fgm_vars = pyspedas.projects.themis.fgm(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot(['thd_fgs_btotal', 'thd_fgs_gse'])

.. image:: _static/themis_fgm.png
   :align: center
   :class: imgborder




Search-coil magnetometer (SCM)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.scm

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   scm_vars = pyspedas.projects.themis.scm(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot(['thd_scf_btotal', 'thd_scf_gse'])

.. image:: _static/themis_scm.png
   :align: center
   :class: imgborder




Electric Field Instrument (EFI)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.efi

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   efi_vars = pyspedas.projects.themis.efi(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot('thd_efs_dot0_gse')

.. image:: _static/themis_efi.png
   :align: center
   :class: imgborder




Electrostatic Analyzer (ESA)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.esa

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   esa_vars = pyspedas.projects.themis.esa(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot(['thd_peif_density', 'thd_peif_vthermal'])

.. image:: _static/themis_esa.png
   :align: center
   :class: imgborder




Solid State Telescope (SST)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.sst

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   sst_vars = pyspedas.projects.themis.sst(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot('thd_psif_density')

.. image:: _static/themis_sst.png
   :align: center
   :class: imgborder




Moments data
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.mom

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   mom_vars = pyspedas.projects.themis.mom(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot(['thd_peim_velocity_gsm', 'thd_peim_density'])

.. image:: _static/themis_mom.png
   :align: center
   :class: imgborder




Ground computed moments data
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.gmom

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   gmom_vars = pyspedas.projects.themis.gmom(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot(['thd_ptiff_velocity_gse', 'thd_pteff_density', 'thd_pteff_avgtemp'])

.. image:: _static/themis_gmom.png
   :align: center
   :class: imgborder



State data
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.state

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   state_vars = pyspedas.projects.themis.state(probe='d', trange=['2013-11-5', '2013-11-6'])
   tplot(['thd_pos', 'thd_vel'])

.. image:: _static/themis_state.png
   :align: center
   :class: imgborder



Orbit data from SSCWeb
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.ssc

Example
^^^^^^^^^

.. code-block:: python
   
   from pyspedas.projects.themis import ssc
   ssc_vars = ssc(probe='d', trange=['2012-10-01', '2012-10-02'])
   print(ssc_vars)

   ['GEO_LAT', 'GEO_LON', 'GEO_LCT_T', 'GM_LAT', 'GM_LON', 'GM_LCT_T', 'GSE_LAT', 'GSE_LON', 'GSE_LCT_T', 'GSM_LAT', 'GSM_LON', 'SM_LAT', 'SM_LON', 'SM_LCT_T', 'NorthBtrace_GEO_LAT', 'NorthBtrace_GEO_LON', 'NorthBtrace_GEO_ARCLEN', 'SouthBtrace_GEO_LAT', 'SouthBtrace_GEO_LON', 'SouthBtrace_GEO_ARCLEN', 'NorthBtrace_GM_LAT', 'NorthBtrace_GM_LON', 'NorthBtrace_GM_ARCLEN', 'SouthBtrace_GM_LAT', 'SouthBtrace_GM_LON', 'SouthBtrace_GM_ARCLEN', 'RADIUS', 'MAG_STRTH', 'DNEUTS', 'BOW_SHOCK', 'MAG_PAUSE', 'L_VALUE', 'INVAR_LAT', 'MAG_X', 'MAG_Y', 'MAG_Z', 'XYZ_GEO', 'XYZ_GM', 'XYZ_GSE', 'XYZ_GSM', 'XYZ_SM']



Orbit data from SSCWeb (predicted)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.ssc_pre

Example
^^^^^^^^^

.. code-block:: python
   
   from pyspedas.projects.themis import ssc_pre
   ssc_pre_vars = ssc_pre(probe='a', trange=['2028-12-01', '2028-12-02'])
   print(ssc_pre_vars)

   ['GEO_LAT', 'GEO_LON', 'GEO_LCT_T', 'GM_LAT', 'GM_LON', 'GM_LCT_T', 'GSE_LAT', 'GSE_LON', 'GSE_LCT_T', 'GSM_LAT', 'GSM_LON', 'SM_LAT', 'SM_LON', 'SM_LCT_T', 'NorthBtrace_GEO_LAT', 'NorthBtrace_GEO_LON', 'NorthBtrace_GEO_ARCLEN', 'SouthBtrace_GEO_LAT', 'SouthBtrace_GEO_LON', 'SouthBtrace_GEO_ARCLEN', 'NorthBtrace_GM_LAT', 'NorthBtrace_GM_LON', 'NorthBtrace_GM_ARCLEN', 'SouthBtrace_GM_LAT', 'SouthBtrace_GM_LON', 'SouthBtrace_GM_ARCLEN', 'RADIUS', 'MAG_STRTH', 'DNEUTS', 'BOW_SHOCK', 'MAG_PAUSE', 'L_VALUE', 'INVAR_LAT', 'MAG_X', 'MAG_Y', 'MAG_Z', 'XYZ_GEO', 'XYZ_GM', 'XYZ_GSE', 'XYZ_GSM', 'XYZ_SM']



Ground magnetometer data
----------------------------------------------------------
.. autofunction:: pyspedas.projects.themis.gmag

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   gmag_vars = pyspedas.projects.themis.gmag(sites='ccnv', trange=['2013-11-5', '2013-11-6'])
   tplot('thg_mag_ccnv')

.. image:: _static/themis_gmag.png
   :align: center
   :class: imgborder



