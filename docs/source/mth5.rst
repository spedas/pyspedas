Magnetometer Data from Seismological Networks (mth5)
====================================================

This module converts the magnetometer data from the EarthScope `USArray magnetotelluric
<http://www.usarray.org/researchers/obs/magnetotelluric>`_ (MT) program using the `International Federation of Digital
Seismographic Networks <https://www.fdsn.org/networks/>`_ (FDSN) standards into high-level data products and provides
access to the data via PySPEDAS. It utilizes the `MTH5 <https://mth5.readthedocs.io/>`_ and `mt_metadata
<https://mt-metadata.readthedocs.io/>`_ packages that were developed at the USGS (U.S. Geological Survey).

Installation requirements
----------------------------------------------------------

The MTH5 package is not included as a default dependency in PySPEDAS. To use this module (`pyspedas.mth5`), please install MTH5:

.. code-block:: bash

   pip install mth5

This module downloads cache h5 files using the `EarthScope (formerly IRIS) Data Management Center
<http://service.iris.edu/fdsnws/dataselect/1/>`_, which provides FDSN-compliant access to a variety of information,
including data and metadata. Note that in 2023, Incorporated Research Institutions for Seismology (IRIS) became part of
the EarthScope Consortium, which explains the domain name of the data center. The cache files are stored in the `mth5`
folder, with the parent folder specified by the environment variable `SPEDAS_DATA_DIR`.

Load FDSN data
----------------------------------------------------------

To load data, the user must specify FDSN `network` and `station`. Currently, the module supports only magnetotelluric
data from MTArray. The stations can be explored using a browsable `Gmap <https://ds.iris.edu/gmap/>`_. Additional
examples are available via Jupyter notebooks of `PySPEDAS MTH5 examples
<https://github.com/spedas/pyspedas_examples/tree/master/pyspedas_examples/notebooks/mth5>`_ and a comprehensive guide
on `Accessing Magnetic Field Data from EarthScope Using MTH5
<https://github.com/simpeg/aurora/blob/main/docs/examples/earthscope_magnetic_data_tutorial.ipynb>`_.

.. autofunction:: pyspedas.mth5.load_fdsn.load_fdsn

Example
^^^^^^^^^

.. code-block:: python

    from pyspedas.mth5.load_fdsn import load_fdsn
    import pytplot
    load_fdsn(network="4P", station="ALW48", trange=['2015-06-22', '2015-06-24'])
    pytplot.tplot('fdsn_4P_ALW48')

.. image:: _static/mth5_4p_alw48.png
   :align: center
   :class: imgborder


Datasets availability
----------------------------------------------------------
.. autofunction:: pyspedas.mth5.utilities.datasets

Example
^^^^^^^^^

.. code-block:: python

   from pyspedas.mth5.utilities import datasets
   valid_dataset = datasets(trange=["2015-06-22", "2015-06-23"])
   print(valid_dataset)

.. code-block:: text

    {'4P': {'ALW48': {('2015-06-18T15:00:36.0000', '2015-07-09T13:45:10.0000'): ['LFE', 'LFN', 'LFZ']}, ...
    ...
    More entries
    }

