Ulysses
========================================================================
The routines in this module can be used to load data from the Ulysses mission.


Magnetic field (VHM)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.ulysses.vhm

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   vhm_vars = pyspedas.projects.ulysses.vhm()
   tplot('B_MAG')

.. image:: _static/ulysses_vhm.png
   :align: center
   :class: imgborder




Solar wind plasma (SWOOPS)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.ulysses.swoops

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   swoops_vars = pyspedas.projects.ulysses.swoops()
   tplot(['Density', 'Temperature', 'Velocity'])

.. image:: _static/ulysses_swoops.png
   :align: center
   :class: imgborder




Solar wind ion composition (SWICS)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.ulysses.swics

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   swics_vars = pyspedas.projects.ulysses.swics()
   tplot('Velocity')

.. image:: _static/ulysses_swics.png
   :align: center
   :class: imgborder




Energetic particles (EPAC)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.ulysses.epac

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   epac_vars = pyspedas.projects.ulysses.epac()
   tplot('Omni_Protons')

.. image:: _static/ulysses_epac.png
   :align: center
   :class: imgborder




Low-energy ions and electrons (HI-SCALE)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.ulysses.hiscale

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   hiscale_vars = pyspedas.projects.ulysses.hiscale()
   tplot('Electrons')

.. image:: _static/ulysses_hiscale.png
   :align: center
   :class: imgborder




Solar X-rays and cosmic gamma-ray bursts (GRB)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.ulysses.grb

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pyspedas import tplot
   grb_vars = pyspedas.projects.ulysses.grb()
   tplot('Count_Rate')

.. image:: _static/ulysses_grb.png
   :align: center
   :class: imgborder



