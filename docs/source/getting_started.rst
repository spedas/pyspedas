Getting Started
====================================

PySPEDAS supports Windows, macOS and Linux.

Requirements
--------------
Python 3.9 or later is required.

We recommend Anaconda, which comes with a suite of packages useful for scientific data analysis. Step-by-step instructions for installing Anaconda can be found at: `Windows <https://docs.anaconda.com/anaconda/install/windows/>`_, `macOS <https://docs.anaconda.com/anaconda/install/mac-os/>`_, `Linux <https://docs.anaconda.com/anaconda/install/linux/>`_

Installation
--------------
To get started, install the pyspedas package using PyPI:

.. code-block:: bash

   pip install pyspedas


To upgrade to the latest version of pySPEDAS, include the '--upgrade' option when calling pip, e.g.,

.. code-block:: bash

   pip install pyspedas --upgrade


Local Data Directories
------------------------
By default, the data is stored in your pyspedas directory in a folder named 'pydata'. The recommended way of setting your local data directory is to set the **SPEDAS_DATA_DIR** environment variable. **SPEDAS_DATA_DIR** acts as a root data directory for all missions, and will also be used by IDL (if you’re running a recent copy of the bleeding edge).

Mission specific data directories (e.g., **MMS_DATA_DIR** for MMS, **THM_DATA_DIR** for THEMIS) can also be set, and these will override **SPEDAS_DATA_DIR**.

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


Accessing the Data and Timestamps
-----------------------------------
Once the data are loaded into tplot variables, you can access them using the get_data function from pytplot. e.g., 

.. code-block:: python

   from pytplot import get_data

   mag_data = get_data('mms1_fgm_b_gse_srvy_l2_bvec')

   # get_data returns a namedtuple with 'times' and 'y':
   mag_data.times # the unix times, stored as a numpy array
   mag_data.y # the data values

Note: some types of data (spectrograms, DFs) have higher dimensions; e.g., spectra have a 'v' with the y-axis values for the data stored in 'y', and some data can have several dimensions: 'v1', 'v2', and 'v3'

