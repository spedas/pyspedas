Coordinate Systems
====================================

PySPEDAS can transform between many of the standard coordinate systems used in heliophysics:

* GSE (Geocentric Solar Ecliptic)
* GSM (Geocentric Solar Magnetic)
* GEI (Geocentric Equatorial Inertial)
* SM (Solar Magnetic)
* GEO (Geographic)
* J2000

There are also routines for working with other specialized coordinate systems

* FAC (Field alignned coordinates)
* LMN (Boundary-aligned coordinates)
* MVA (Minimum-variance coordinates)


Some individual projects may include additional coordinate trasformation routines
for systems used by those missions.  For example, the THEMIS module includes some additional
transforms for:

* DSL (Despun Solar Spinaxis)
* SSL (Spinning Solar SpinAxis)
* SSL (Selenocentric Solar Ecliptic)
* SEL (Selenographic)

Transformations
------------------------------------
.. autofunction:: pyspedas.cotrans

Examples
^^^^^^^^^

.. code-block:: python
   
   import pyspedas
   pyspedas.projects.themis.state(trange=['2015-10-16', '2015-10-17'], probe='c')

   from pyspedas import cotrans
   cotrans(name_in='thc_pos_gse', name_out='gsm_data', coord_in='gse', coord_out='gsm')
   cotrans(name_in='thc_pos_gse', name_out='sm_data', coord_in='gse', coord_out='sm')
   cotrans(name_in='thc_pos_gse', name_out='geo_data', coord_in='gse', coord_out='geo')

   from pytplot import tplot
   tplot(['gsm_data', 'sm_data', 'geo_data'])
   
Cartesian to Spherical Coordinates
-----------------------------------

.. autofunction:: pyspedas.cart2spc

Spherical to Cartesian Coordinates
-----------------------------------

.. autofunction:: pyspedas.spc2cart

Field-Aligned Coordinates (FAC)
-------------------------------

.. autofunction:: pyspedas.fac_matrix_make


Minimum Variance (MVA) Coordinates
-----------------------------------

.. autofunction:: pyspedas.minvar_matrix_make
.. autofunction:: pyspedas.minvar

LMN Coordinates
---------------

.. autofunction:: pyspedas.gsm2lmn

Rotate Vectors by Rotation Matrix
----------------------------------

.. autofunction:: pyspedas.tvector_rotate

Getting/Setting the Coordinate System for tplot variables
---------------------------------------------------------
.. autofunction:: pyspedas.get_coords
.. autofunction:: pyspedas.set_coords

Quaternion Routines
-------------------

Quaternions can be used to represent rotations in 3-D space, much like Euler Angles
or rotation matrices.  They are often more computationally convenient and efficient.
They are represented in PySPEDAS as 4-element floating point arrays, which can be thought
of as a scalar component encoding the rotation angle, and 3 vector components encoding the rotation axis.

Convertiong to/from axis-angle rotation specification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autofunction:: pyspedas.qcompose
.. autofunction:: pyspedas.qdecompose

Converting to/from rotation matrices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.mtoq
.. autofunction:: pyspedas.qtom

Combining quaternions (by multiplying)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.qmult

Interpolating rotations (Quaternion Spherical Linear intERPolation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.qslerp

Other operations
^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.qnorm
.. autofunction:: pyspedas.qnormalize
.. autofunction:: pyspedas.qvalidate
.. autofunction:: pyspedas.qconj



Support Routines
------------------------

The routines listed here are generally not called directly
by users. They are listed here for completeness.

.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.get_time_parts
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.csundir_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.cdipdir
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.cdipdir_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.tgeigse_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgei2gse
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.tgsegei_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgse2gei
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.tgsegsm_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgse2gsm
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.tgsmgse_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgsm2gse
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.tgsmsm_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgsm2sm
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.tsmgsm_vect
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subsm2gsm
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgei2geo
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgeo2gei
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgeo2mag
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.submag2geo
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.ctv_mm_mult
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.j2000_matrix_vec
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.ctv_mx_vec_rot
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subgei2j2000
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subj20002gei
.. autofunction:: pyspedas.cotrans_tools.cotrans_lib.subcotrans
