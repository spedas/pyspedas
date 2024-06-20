Analysis Tools
==============

Generalized 3-D Particle Distribution Tools
--------------------------------------------

The tools documented in this section are not intended to be called
directly by PySPEDAS users; rather, they are provided as building blocks
for mission-specific 3-D particle distribution tools.  Mission-specific wrappers
will generally be needed to load the particle data to be operated on,
perform any calibration, sanitization, or other preliminary steps, then
populate the data structures used by the general-purpose particle tools.

Plasma Moments
--------------

This group of routines calculates plasma moments (density, velocity, fluxes, pressure tensors, etc.) from
3-D particle distributions (with two dimensions being azimuthal and elevation angles, and the third dimension
representing energy bins).

moments_3d
^^^^^^^^^^

This routine takes a data structure containing the particle distribution function,
and other information like angle and energy bin definitions and sizes, and returns
a dictionary containing plasma moments generated from the particle distributions.

.. autofunction:: pyspedas.particles.moments.moments_3d.moments_3d

moments_3d_omega_weights
^^^^^^^^^^^^^^^^^^^^^^^^

This routine takes an array defining angular bins, and calculates
an array of weights based on the solid angles subtended by each bin,
to be used in the plasma moment calculations.

.. autofunction:: pyspedas.particles.moments.moments_3d_omega_weights.moments_3d_omega_weights

spd_pgs_moments
^^^^^^^^^^^^^^^

Basically a wrapper around moments_3d

.. autofunction:: pyspedas.particles.moments.spd_pgs_moments.spd_pgs_moments

spd_pgs_moments_tplot
^^^^^^^^^^^^^^^^^^^^^^^^

Converts a dictionary (as returned by moments_3d) to tplot variables

.. autofunction:: pyspedas.particles.moments.spd_pgs_moments_tplot.spd_pgs_moments_tplot


Other quantities derived from 3-D particle distributions
---------------------------------------------------------

spd_pgs_do_fac
^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_do_fac.spd_pgs_do_fac

spd_pgs_limit_range
^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_limit_range.spd_pgs_limit_range

spd_pgs_make_e_spec
^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_make_e_spec.spd_pgs_make_e_spec

spd_pgs_make_phi_spec
^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_make_phi_spec.spd_pgs_make_phi_spec

spd_pgs_make_theta_spec
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_make_theta_spec.spd_pgs_make_theta_spec

spd_pgs_make_tplot
^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_make_tplot.spd_pgs_make_tplot

spd_pgs_progress_update
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_progress_update.spd_pgs_progress_update

Slices of 3-D particle distributions
----------------------------------------

This set of routines creates 1-D and 2-D slices through 3-D particle distributions.

slice1d_plot
^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_slice2d.slice1d_plot.plot

slice2d
^^^^^^^

.. autofunction:: pyspedas.particles.spd_slice2d.slice2d.slice2d



Other analysis tools
---------------------

The tools in this section perform various operations on tplot variables.

.. toctree::
   :maxdepth: 2

   avg_data
   clean_spikes
   tcrossp
   tdotp 
   tdpwrspc
   interpolation
   tnormalize
   subtract_average
   subtract_median
   twavpol