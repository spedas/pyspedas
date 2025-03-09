Mission Specific Tools
=======================

Several missions provide tools that are written specifically to work with their
datasets.  Many missions have defined custom coordinate systems pertaining to their data,
and require their own routines to transform to and from well-known geophysical coordinate frames.
Mission-specific data structures (for example, particle data representation) may require
mission-specific wrappers to format the data for use with PySPEDAS general purpose analysis tools.

.. toctree::
   :maxdepth: 1

   themis_analysis
   erg_analysis
   mms_analysis
