Geostationary Operational Environmental Satellite (GOES)
========================================================================
The routines in this module can be used to load data from the Geostationary Operational Environmental Satellite (GOES) mission.


Magnetometer (FGM)
----------------------------------------------------------
.. autofunction:: pyspedas.projects.goes.fgm

Example
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   from pytplot import tplot
   mag_vars = pyspedas.projects.goes.fgm(trange=['2013-11-5', '2013-11-6'], datatype='512ms')
   tplot(['BX_1', 'BY_1', 'BZ_1'])

.. image:: _static/goes_fgm.png
   :align: center
   :class: imgborder

EPS
----------------------------------------------------------
.. autofunction:: pyspedas.projects.goes.eps

EPEAD
----------------------------------------------------------
.. autofunction:: pyspedas.projects.goes.epead

EUVS
----------------------------------------------------------
.. autofunction:: pyspedas.projects.goes.euvs

HEPAD
----------------------------------------------------------
.. autofunction:: pyspedas.projects.goes.hepad

MAG
----------------------------------------------------------

.. autofunction:: pyspedas.projects.goes.mag

MPSH
----------------------------------------------------------

.. autofunction:: pyspedas.projects.goes.mpsh

MAGED
----------------------------------------------------------

.. autofunction:: pyspedas.projects.goes.maged

MAGPD
----------------------------------------------------------

.. autofunction:: pyspedas.projects.goes.magpd

ORBIT
----------------------------------------------------------

.. autofunction:: pyspedas.projects.goes.orbit

SGPS
----------------------------------------------------------

.. autofunction:: pyspedas.projects.goes.sgps

