Van Allen Probes (RBSP)
========================================================================
The routines in this module can be used to load data from the Van Allen Probes (RBSP) mission.


Electric and Magnetic Field Instrument Suite and Integrated Science (EMFISIS)
----------------------------------------------------------
.. autofunction:: pyspedas.rbsp.emfisis

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   emfisis_vars = pyspedas.rbsp.emfisis(trange=['2018-11-5/10:00', '2018-11-5/15:00'], datatype='magnetometer', level='l3', time_clip=True)
   tplot(['Mag', 'Magnitude'])

.. image:: _static/rbsp_emfisis.png
   :align: center
   :class: imgborder




Electric Field and Waves Suite (EFW)
----------------------------------------------------------
.. autofunction:: pyspedas.rbsp.efw

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   efw_vars = pyspedas.rbsp.efw(trange=['2015-11-5', '2015-11-6'], level='l3')
   tplot(['efield_in_inertial_frame_spinfit_mgse', 'spacecraft_potential'])

.. image:: _static/rbsp_efw.png
   :align: center
   :class: imgborder




Radiation Belt Storm Probes Ion Composition Experiment (RBSPICE)
----------------------------------------------------------
.. autofunction:: pyspedas.rbsp.rbspice

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   rbspice_vars = pyspedas.rbsp.rbspice(trange=['2018-11-5', '2018-11-6'], datatype='TOFxEH', level='l3')
   tplot('rbspa_rbspice_l3_TOFxEH_proton_omni_spin')
   # calculate the pitch angle distributions
   from pyspedas.rbsp.rbspice_lib.rbsp_rbspice_pad import rbsp_rbspice_pad
   rbsp_rbspice_pad(probe='a', datatype='TOFxEH', level='l3')
   tplot(['rbspa_rbspice_l3_TOFxEH_proton_omni_spin',
          'rbspa_rbspice_l3_TOFxEH_proton_omni_0-1000keV_pad_spin'])

.. image:: _static/rbsp_rbspice.png
   :align: center
   :class: imgborder



Energetic Particle, Composition, and Thermal Plasma Suite (ECT) - MagEIS
----------------------------------------------------------
.. autofunction:: pyspedas.rbsp.mageis

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   mageis_vars = pyspedas.rbsp.mageis(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel04')
   tplot('I')

.. image:: _static/rbsp_mageis.png
   :align: center
   :class: imgborder




Energetic Particle, Composition, and Thermal Plasma Suite (ECT) - HOPE
----------------------------------------------------------
.. autofunction:: pyspedas.rbsp.hope

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   hope_vars = pyspedas.rbsp.hope(trange=['2018-11-5', '2018-11-6'], datatype='moments', level='l3', rel='rel04')
   tplot('Ion_density')

.. image:: _static/rbsp_hope.png
   :align: center
   :class: imgborder



Energetic Particle, Composition, and Thermal Plasma Suite (ECT) - REPT
----------------------------------------------------------
.. autofunction:: pyspedas.rbsp.rept

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   rept_vars = pyspedas.rbsp.rept(trange=['2018-11-5', '2018-11-6'], level='l3', rel='rel03')
   tplot('Tperp_e_200')

.. image:: _static/rbsp_rept.png
   :align: center
   :class: imgborder




Relativistic Proton Spectrometer (RPS)
----------------------------------------------------------
.. autofunction:: pyspedas.rbsp.rps

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   rps_vars = pyspedas.rbsp.rps(trange=['2018-11-5', '2018-11-6'], datatype='rps', level='l2')
   tplot('DOSE1')

.. image:: _static/rbsp_rps.png
   :align: center
   :class: imgborder



