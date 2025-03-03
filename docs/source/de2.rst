Dynamics Explorer 2 (DE2)
========================================================================
The routines in this module can be used to load data from the Dynamics Explorer 2 (DE2) mission.


Magnetometer (MAG)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.mag

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   mag_vars = pyspedas.projects.de2.mag(trange=['1983-02-10', '1983-02-11'])
   tplot(['bx', 'by', 'bz'])

.. image:: _static/de2_mag.png
   :align: center
   :class: imgborder


Neutral Atmosphere Composition Spectrometer (NACS)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.nacs

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   nacs_vars = pyspedas.projects.de2.nacs(trange=['1983-02-10', '1983-02-11'])
   tplot(['O_density', 'N_density'])

.. image:: _static/de2_nacs.png
   :align: center
   :class: imgborder


Retarding Potential Analyzer (RPA)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.rpa

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   rpa_vars = pyspedas.projects.de2.rpa(trange=['1983-02-10', '1983-02-11'])
   tplot(['ionDensity', 'ionTemperature'])

.. image:: _static/de2_rpa.png
   :align: center
   :class: imgborder


Fabry-Pérot Interferometer (FPI)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.fpi

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   fpi_vars = pyspedas.projects.de2.fpi(trange=['1983-02-10', '1983-02-11'])
   tplot('TnF')

.. image:: _static/de2_fpi.png
   :align: center
   :class: imgborder


Ion Drift Meter (IDM)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.idm

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   idm_vars = pyspedas.projects.de2.idm(trange=['1983-02-10', '1983-02-11'])
   tplot(['ionVelocityZ', 'ionVelocityY'])

.. image:: _static/de2_idm.png
   :align: center
   :class: imgborder


Wind and Temperature Spectrometer (WATS)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.wats

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   wats_vars = pyspedas.projects.de2.wats(trange=['1983-02-10', '1983-02-11'])
   tplot(['density', 'Tn'])

.. image:: _static/de2_wats.png
   :align: center
   :class: imgborder


Vector Electric Field Instrument (VEFI)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.vefi

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   vefi_vars = pyspedas.projects.de2.vefi(trange=['1983-02-10', '1983-02-11'])
   tplot(['spectA', 'spectB', 'spectC'])

.. image:: _static/de2_vefi.png
   :align: center
   :class: imgborder


Langmuir Probe Instrument (LANG)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.de2.lang

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   lang_vars = pyspedas.projects.de2.lang(trange=['1983-02-10', '1983-02-11'])
   tplot(['plasmaDensity', 'electronTemp'])

.. image:: _static/de2_lang.png
   :align: center
   :class: imgborder




    