MMS analysis tools
=====================

Coordinate transforms
---------------------

The MMS mission defines several coordinate systems:  BCS, DBCS, DMPA, SMPA, and DSL.
The MMS MEC data products contain quaternions enabling interconversion between these systems
and the geophysical systems GSE, GSE2000, GSM, SM, GEO, ECI, and J2000.

The MMS MEC load routine must be called to load the quaternion data before performing
coordinate transformations.

.. autofunction:: pyspedas.projects.mms.mec
   :no-index:

Once the MEC data is loaded, call mms_qcotrans to perform the transforms.

.. autofunction:: pyspedas.projects.mms.mms_qcotrans

MMS also provides a routine to transform input data to boundary-normal (LMN) coordinates.

.. autofunction:: pyspedas.projects.mms.mms_cotrans_lmn

Particle distribution tools
----------------------------

The mms_part_getspec routine can be used to calculate plasma moments and spectra from 3-D particle distributions.

.. autofunction:: pyspedas.projects.mms.mms_part_getspec

The mms_part_slice2d routine can be used to visualize 2-D slices through 3-D particle distributions, with several
choices of orientation for the slice.
