Cluster
========================================================================
The routines in this module can be used to load data from the Cluster mission.


Fluxgate Magnetometer (FGM)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.fgm

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   fgm_vars = pyspedas.projects.cluster.fgm(trange=['2018-11-5', '2018-11-6'])
   tplot('B_xyz_gse__C1_UP_FGM')

.. image:: _static/cluster_fgm.png
   :align: center
   :class: imgborder




Active Spacecraft Potential Control experiment (ASPOC)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.aspoc

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   asp_vars = pyspedas.projects.cluster.aspoc(trange=['2004-10-01', '2004-10-2'])
   tplot('I_ion__C1_PP_ASP')

.. image:: _static/cluster_aspoc.png
   :align: center
   :class: imgborder




Cluster Ion Spectroscopy experiment (CIS)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.cis

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   cis_vars = pyspedas.projects.cluster.cis(trange=['2004-10-01', '2004-10-2'])
   tplot(['N_p__C1_PP_CIS', 'V_p_xyz_gse__C1_PP_CIS', 'T_p_par__C1_PP_CIS', 'T_p_perp__C1_PP_CIS'])

.. image:: _static/cluster_cis.png
   :align: center
   :class: imgborder




Digital Wave Processing instrument (DWP)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.dwp

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   dwp_vars = pyspedas.projects.cluster.dwp(trange=['2004-10-01', '2004-10-2'])
   tplot('Correl_Ivar__C1_PP_DWP')

.. image:: _static/cluster_dwp.png
   :align: center
   :class: imgborder




Electron Drift Instrument (EDI)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.edi

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   edi_vars = pyspedas.projects.cluster.edi(trange=['2004-10-01', '2004-10-2'])
   tplot(['V_ed_xyz_gse__C1_PP_EDI', 'E_xyz_gse__C1_PP_EDI'])

.. image:: _static/cluster_edi.png
   :align: center
   :class: imgborder




Electric Field and Wave experiment (EFW)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.efw

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   efw_vars = pyspedas.projects.cluster.efw(trange=['2004-10-01', '2004-10-2'])
   tplot('E_dusk__C1_PP_EFW')

.. image:: _static/cluster_efw.png
   :align: center
   :class: imgborder




Plasma Electron and Current Experiment (PEACE)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.peace

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   peace_vars = pyspedas.projects.cluster.peace(trange=['2004-10-01', '2004-10-2'])
   tplot(['N_e_den__C1_PP_PEA', 'V_e_xyz_gse__C1_PP_PEA', 'T_e_par__C1_PP_PEA', 'T_e_perp__C1_PP_PEA'])

.. image:: _static/cluster_peace.png
   :align: center
   :class: imgborder




Research with Adaptive Particle Imaging Detectors (RAPID)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.rapid

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   rap_vars = pyspedas.projects.cluster.rapid(trange=['2004-10-01', '2004-10-2'])
   tplot(['J_e_lo__C1_PP_RAP', 'J_e_hi__C1_PP_RAP', 'J_p_lo__C1_PP_RAP', 'J_p_hi__C1_PP_RAP'])

.. image:: _static/cluster_rapid.png
   :align: center
   :class: imgborder




Spatio-Temporal Analysis of Field Fluctuation experiment (STAFF)
-----------------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.staff

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   sta_vars = pyspedas.projects.cluster.staff(trange=['2004-10-01', '2004-10-02'])
   tplot('B_par_f1__C1_PP_STA')

.. image:: _static/cluster_staff.png
   :align: center
   :class: imgborder




Wide Band Data receiver (WBD)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.wbd

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   wbd_vars = pyspedas.projects.cluster.wbd(trange=['2012-11-06/02:10', '2012-11-06/02:20'])
   tplot('WBD_Elec')

.. image:: _static/cluster_wbd.png
   :align: center
   :class: imgborder




Waves of High Frequency and Sounder for Probing of Density by Relaxation (WHISPER)
-----------------------------------------------------------------------------------
.. autofunction:: pyspedas.projects.cluster.whi

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   whi_vars = pyspedas.projects.cluster.whi()
   tplot('N_e_res__C1_PP_WHI')

.. image:: _static/cluster_whi.png
   :align: center
   :class: imgborder


Load Data from Cluster Science Archive
---------------------------------------

The above routines load data from NASA's SPDF archive.  There is also a way to download Cluster data products
directly from ESA's Cluster Science Archive

.. autofunction:: pyspedas.projects.cluster.load_csa



