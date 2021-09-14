.. PySPEDAS documentation master file, created by
   sphinx-quickstart on Fri Sep 10 21:11:38 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Magnetospheric Multiscale (MMS)
====================================
The routines in this module can be used to load data from the Magnetospheric Multiscale (MMS) mission.

Fluxgate Magnetometer (FGM)
-----------------------------
.. autofunction:: pyspedas.mms.fgm

FGM Example
^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.mms.fgm(trange=['2015-10-16/12:45', '2015-10-16/13:00'], time_clip=True)
   tplot(['mms1_fgm_b_gsm_srvy_l2_btot', 'mms1_fgm_b_gsm_srvy_l2_bvec'])

.. image:: _static/mms_fgm.png
   :scale: 75 %
   :align: center

Search-coil Magnetometer (SCM)
--------------------------------
.. autofunction:: pyspedas.mms.scm

SCM Example
^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.mms.scm(trange=['2015-10-16/13:06', '2015-10-16/13:07'], time_clip=True)
   tplot('mms1_scm_acb_gse_scsrvy_srvy_l2')

.. image:: _static/mms_scm.png
   :scale: 75 %
   :align: center

Level 3 FGM+SCM Data (FSM)
-----------------------------
.. autofunction:: pyspedas.mms.fsm

FSM Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_fsm.png
   :scale: 75 %
   :align: center

Electric field Double Probe (EDP)
-----------------------------------
.. autofunction:: pyspedas.mms.edp

EDP Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_edp.png
   :scale: 75 %
   :align: center

Electron Drift Instrument (EDI)
---------------------------------
.. autofunction:: pyspedas.mms.edi

EDI Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_edi.png
   :scale: 75 %
   :align: center

Fly's Eye Energetic Particle Sensor (FEEPS)
--------------------------------------------
.. autofunction:: pyspedas.mms.feeps

FEEPS Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_feeps.png
   :scale: 75 %
   :align: center

Energetic Ion Spectrometer (EIS)
-----------------------------------
.. autofunction:: pyspedas.mms.eis

EIS Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_eis.png
   :scale: 75 %
   :align: center

Active Spacecraft Potential Control (ASPOC)
--------------------------------------------
.. autofunction:: pyspedas.mms.aspoc

ASPOC Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_aspoc.png
   :scale: 75 %
   :align: center

Fast Plasma Investigation (FPI)
--------------------------------
.. autofunction:: pyspedas.mms.fpi

FPI Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_fpi.png
   :scale: 75 %
   :align: center

Hot Plasma Composition Analyzer (HPCA)
---------------------------------------
.. autofunction:: pyspedas.mms.hpca

HPCA Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_hpca.png
   :scale: 75 %
   :align: center

Magnetic Ephemeris Coordinates (MEC)
-------------------------------------
.. autofunction:: pyspedas.mms.mec

MEC Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_mec.png
   :scale: 75 %
   :align: center

.. autofunction:: pyspedas.mms.state

State Example
^^^^^^^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   pyspedas.ace.mfi(trange=['2018-11-5', '2018-11-6'])
   tplot(['BGSEc', 'Magnitude'])

.. image:: _static/mms_state.png
   :scale: 75 %
   :align: center
