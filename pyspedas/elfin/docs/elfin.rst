Electron Losses and Fields Investigation (ELFIN)
========================================================================
The routines in this module can be used to load data from the Electron Losses and Fields Investigation (ELFIN) mission.


Fluxgate Magnetometer (FGM)
----------------------------------------------------------
.. autofunction:: pyspedas.elfin.fgm

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   elfin_vars = pyspedas.elfin.fgm(trange=['2020-11-5', '2020-11-6'])
   tplot('ela_fgs')

.. image:: _static/elfin_fgm.png
   :align: center
   :class: imgborder


Energetic Particle Detector (EPD)
----------------------------------------------------------
.. autofunction:: pyspedas.elfin.epd

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   elfin_vars = pyspedas.elfin.epd(trange=['2020-11-5', '2020-11-6'])
   tplot(['ela_pef_nflux', 'ela_pif_cps'])

.. image:: _static/elfin_epd.png
   :align: center
   :class: imgborder


Magneto Resistive Magnetometer (MRMa)
----------------------------------------------------------
.. autofunction:: pyspedas.elfin.mrma

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   elfin_vars = pyspedas.elfin.mrma(trange=['2020-11-5', '2020-11-6'])
   tplot('ela_mrma')

.. image:: _static/elfin_mrma.png
   :align: center
   :class: imgborder


Magneto Resistive Magnetometer (MRMi)
----------------------------------------------------------
.. autofunction:: pyspedas.elfin.mrmi

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   elfin_vars = pyspedas.elfin.mrmi(trange=['2020-11-5', '2020-11-6'])
   tplot('ela_mrmi')

.. image:: _static/elfin_mrmi.png
   :align: center
   :class: imgborder


State data (state)
----------------------------------------------------------
.. autofunction:: pyspedas.elfin.state

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   elfin_vars = pyspedas.elfin.state(trange=['2020-11-5', '2020-11-6'])
   tplot('ela_pos_gei')

.. image:: _static/elfin_state.png
   :align: center
   :class: imgborder


Engineering (ENG)
----------------------------------------------------------
.. autofunction:: pyspedas.elfin.eng

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   elfin_vars = pyspedas.elfin.eng(trange=['2020-11-5', '2020-11-6'])
   tplot('ela_eng_tplot')

.. image:: _static/elfin_eng.png
   :align: center
   :class: imgborder




    