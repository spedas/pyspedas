Getting Started
====================================

Requirements
--------------
Python 3.7 or later is required.

Installation
--------------
pySPEDAS supports Windows, macOS and Linux. To get started, install the pyspedas package using PyPI:

.. code-block:: bash

   pip install pyspedas


To upgrade to the latest version of pySPEDAS, include the '--upgrade' option when calling pip, e.g.,

.. code-block:: bash

   pip install pyspedas --upgrade


Local Data Directories
------------------------
The recommended way of setting your local data directory is to set the SPEDAS_DATA_DIR environment variable. SPEDAS_DATA_DIR acts as a root data directory for all missions, and will also be used by IDL (if you’re running a recent copy of the bleeding edge).

Mission specific data directories (e.g., MMS_DATA_DIR for MMS, THM_DATA_DIR for THEMIS) can also be set, and these will override SPEDAS_DATA_DIR

Loading and Plotting Data
---------------------------
You can load data into tplot variables by calling pyspedas.mission.instrument(), e.g.,

.. code-block:: python

   import pyspedas
   pyspedas.mms.fgm()


The load routines support several keywords to control which data products are loaded (datatype, level, etc). 

To plot the tplot variables that were loaded, use tplot from pytplot, e.g., 

.. code-block:: python

   from pytplot import tplot
   tplot(['mms1_fgm_b_gse_srvy_l2_btot', 'mms1_fgm_b_gse_srvy_l2_bvec'])



