Analysis Tools
==============

Wavelet Analysis Tools
-----------------------


There are several tools in PySPEDAS for performing wavelet analysis on tplot variables or data arrays.

The wavelet98 routine implements wavelet transforms as described in Torrence & Compo (1998).  It works with bare data arrays.

Reference: Torrence, C. and G. P. Compo, 1998: A Practical Guide to Wavelet Analysis. <I>Bull. Amer. Meteor. Soc.</I>, 79, 61-78.

.. autofunction:: pyspedas.wavelet98

The wavelet2 routine is a wrapper for wavelet98.  It also works with bare data arrays.

.. autofunction:: pyspedas.wavelet2

The wavelet routine provides an interface to the external pywavelets package, and works with tplot variables.
If the wavelet scales are unspecified, they are derived using an algorithm similar to that used by the IDL SPEDAS wav_data routine.

.. autofunction:: pyspedas.wavelet

The wav_data routine is a Python implementation of the IDL SPEDAS wav_data routine.   This is the routine to use
if you want to reproduce results from IDL SPEDAS.

.. autofunction:: pyspedas.wav_data

The wave_signif routine computes significance levels for a wavelet transform.

.. autofunction:: pyspedas.wave_signif

Available wavelet definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following routines are the predefined wavelet functions used by the wavelet98 routines.

Morlet wavelet:

.. autofunction:: pyspedas.analysis.wavelet98.morlet

Paul wavelet:

.. autofunction:: pyspedas.analysis.wavelet98.paul

Difference of gaussians wavelet:

.. autofunction:: pyspedas.analysis.wavelet98.dog



Generalized 3-D Particle Distribution Tools
--------------------------------------------

The tools documented in this section are not intended to be called
directly by PySPEDAS users; rather, they are provided as building blocks
for mission-specific 3-D particle distribution tools.  Mission-specific wrappers
will generally be needed to load the particle data to be operated on,
perform any calibration, sanitization, or other preliminary steps, then
populate the data structures used by the general-purpose particle tools.

For documentation of mission-specific particle tools, see the "Mission Specific Tools" page.

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

.. autofunction:: pyspedas.moments_3d

spd_pgs_moments
^^^^^^^^^^^^^^^

Basically a wrapper around moments_3d

.. autofunction:: pyspedas.spd_pgs_moments

spd_pgs_moments_tplot
^^^^^^^^^^^^^^^^^^^^^^^^

Converts a dictionary (as returned by moments_3d) to tplot variables

.. autofunction:: pyspedas.spd_pgs_moments_tplot


Other quantities derived from 3-D particle distributions
---------------------------------------------------------

spd_pgs_do_fac
^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_do_fac.spd_pgs_do_fac

spd_pgs_regrid
^^^^^^^^^^^^^^

.. autofunction:: pyspedas.particles.spd_part_products.spd_pgs_regrid

Slices of 3-D particle distributions
----------------------------------------

This set of routines creates 1-D and 2-D slices through 3-D particle distributions.

slice1d_plot
^^^^^^^^^^^^

This routine plots the values along the x or y axis of a 2-D slice.

.. autofunction:: pyspedas.slice1d_plot

slice2d
^^^^^^^

.. autofunction:: pyspedas.slice2d

slice2d_plot
^^^^^^^^^^^^

.. autofunction:: pyspedas.slice2d_plot



Magnetic Null Finding
---------------------

For missions such as MMS or Cluster, with at least four spacecraft in a relatively close tetrahedron-like configuration,
measuring the magnetic field simultaneously at four distinct locations allows the calculation of
field gradients in each field component along the X, Y, and Z directions (in other words, a Jacobian matrix).
This information is sufficient to find the location of magnetic null points (where all three field components
are zero), and infer the topology of the magnetic field at the null point.

.. autofunction:: pyspedas.find_magnetic_nulls_fote

.. autofunction:: pyspedas.classify_null_type

.. autofunction:: pyspedas.lingradest
