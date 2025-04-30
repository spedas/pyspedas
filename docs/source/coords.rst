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
* LMN (Boundary-normal coordinates)
* MVA (Minimum-variance coordinates)


Some individual projects may include additional coordinate trasformation routines
for systems used by those missions.  Documentation for the mission-specific coordinate
transform tools and other utilities can be found on the "Mission Specific Tools" page.

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

   from pyspedas import tplot
   tplot(['gsm_data', 'sm_data', 'geo_data'])
   
Cartesian to Spherical Coordinates
-----------------------------------

.. autofunction:: pyspedas.cart2spc
.. autofunction:: pyspedas.cart_to_sphere
.. autofunction:: pyspedas.xyz_to_polar

Spherical to Cartesian Coordinates
-----------------------------------

.. autofunction:: pyspedas.spc2cart
.. autofunction:: pyspedas.sphere_to_cart

Field-Aligned Coordinates (FAC)
-------------------------------

In this coordinate system, the Z axis is aligned with the magnetic field direction.  This leaves a degree of freedom for
the orientation of the X and Y axes.  The "other_dim" parameter lets the user select a reference direction from a number of
options (some of which require an additional input variable to specify the probe position).  The output is a set of rotation
matrices versus time, suitable for use with the tvector_rotate utility.

.. autofunction:: pyspedas.fac_matrix_make


Minimum Variance (MVA) Coordinates
-----------------------------------

In this coordinate system, a set of right-handed basis vectors i,j,k representing
the maximum, intermediate, and minimum variance directions is produced from an input variable,
using a sliding window for the variance, eigenvalue, and eigenvector calculations. To resolve ambiguity
in the direction of the basis vectors, the signs are manipulated such that the Z components on the j and k
components in the j and k directions are positive, while maintaining a right-handed coordinate system. The output is a
set of rotation matrices over time, suitable for use with the tvector_rotate utility.

.. autofunction:: pyspedas.minvar_matrix_make
.. autofunction:: pyspedas.minvar

LMN Coordinates
---------------

In this coordinate system, a set of basis vectors L, M, N are produced, using the probe position, magnetic field direction,
and some solar wind parameters, using the Shue model for the magnetopause boundary location.
The N component will be normal to the magnetopause boundary with the other two components in the tangent plane.
The output is a set of rotation matrices over time, suitable for use with the tvector_rotate utility.

.. autofunction:: pyspedas.lmn_matrix_make
.. autofunction:: pyspedas.gsm2lmn

Rotate Vectors by Rotation Matrix
----------------------------------

Several of the specialized coordinate transforms (for example, FAC, LMN, or MVA)
are implemented by generating a rotation matrix to transform vectors from the original
system to the target system.  The tvector_rotate routine applies these rotation matrices to
tplot variables containing vectors in the original coordinate system, performing any necessary
interpolation of the rotation matrices to match the timestamps of the vectors being transformed.

.. autofunction:: pyspedas.tvector_rotate
   :no-index:

.. autofunction:: pyspedas.rotmat_set_coords
   :no-index:
.. autofunction:: pyspedas.rotmat_get_coords
   :no-index:

Getting/Setting the Coordinate System for tplot variables
---------------------------------------------------------
.. autofunction:: pyspedas.get_coords
   :no-index:
.. autofunction:: pyspedas.set_coords
   :no-index:

Quaternion Routines
-------------------

Quaternions can be used to represent rotations in 3-D space, much like Euler angles
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
