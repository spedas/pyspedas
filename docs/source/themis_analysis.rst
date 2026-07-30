THEMIS analysis tools
=====================

Coordinate transforms
----------------------

The THEMIS mission defines coordinate systems related to the spacecraft spin axes
(one spinning with the spacecraft, the other referenced to the sun direction).
The two ARTEMIS probes (aka THEMIS-B and THEMIS-C) are in lunar orbits, so
so a few selenocentric coordinate transforms are required.

* DSL (Despun Solar L-(angular momentum) vector)
* SSL (Spinning Solar L-(angular momentum) vector)
* SSE (Selenocentric Solar Ecliptic)
* SEL (Selenographic)

The GSE system serves as a bridge between the THEMIS-specific and selenocentric coordinates,
and the set of coordinate systems supported by pyspedas.cotrans().

Each of these transforms requires support data to be loaded from various THEMIS
datasets.


Transformations
^^^^^^^^^^^^^^^^

.. autofunction:: pyspedas.projects.themis.dsl2gse

.. autofunction:: pyspedas.projects.themis.gse2sse

.. autofunction:: pyspedas.projects.themis.sse2sel

.. autofunction:: pyspedas.projects.themis.ssl2dsl

Eclipse Spin Model Corrections
-------------------------------

The THEMIS probes rely on a sun sensor to keep track of the times when the sun crosses the sun sensor during each spin.
These crossing times are used (via a phase-locked loop in the onboard flight software) to drive an onboard spin sectoring
clock that governs the production of particle data distributions and spin fits for the EFI and FGM instruments.

On the ground, the sun sensor crossing times are used to estimate the spacecraft attitude throughout each spin of the probe.
This is crucial for transforming the data from instrument coordinates (which spin with the spacecraft) to DSL coordinates
(despun/solar/angular momentum, with the +X toward the sun. and +Z direction along the spin axis). From DSL coordinates, the
information about spin axis right ascension and declination are used to transform the data into geophysically meaningful
coordinates like GEI, GSE, GSM and others.

From time to time, the THEMIS spacecraft pass through earth or moon shadows.  During these eclipse periods, no sun sensor
crossing data is available. This upsets the onboard spin sectoring clock and spin fit algorithms, introducing a sudden,
spurious spin angle offset that persists until the probe leaves the shadow and sun sensor data becomes available again.

Another important eclipse effect pertains to the probe spin period.  During the eclipse, the probe begins to cool off.
The thermal contraction of the probe (especially the long EFI wire booms) causes the probe to spin faster, reducing the
spin period, in a rather complicated way that depends on the amount of propellant remaining, tank heater cycles, etc.

The effect in the data is that the "estimated DSL" frame begins to rotate with respect to the "true DSL" frame,
with spin phase errors accumulating during the eclipse.  Waveform data from the FGM, SCM, and EFI instruments
will show a distinct sinusoidal variation due to the accumlating spin phase errors.  Spin-based data, like EFI and FGM
spin fits, and particle data which is collected in "estimated DSL" coordinates. shows a similar coordinate frame
rotation, plus an additional phase offset from the disruption to the onboard spin sectoring clock at eclipse entry.

The FGM team has devised a procedure for modeling the evolution of the probe spin period through eclipses.
The model is used to produce a set of theoretical sun sensor crossing times based on the spin period evolution.
These artificial sun sensor crossing times can be used to supplement the pure sun sensor data, and remove most of
the spin phase errors due to the eclipse effects.

For correcting spin fit and particle data, an estimate of the constant spin phase offset is required.  This
can be obtained by comparing FGM spin fit data with FGM waveform data.  The FGL data type is only
available during fast survey time intervals, so this level of correction is only available for some
eclipses.

The eclipse spin modeling process isn't 100% successful: for some eclipses, the spin modeling fails to
converge, and no corrections are produced for that eclipse.

Therefore, during every eclipse, there are three possibilities:  no corrections at all;  partial corrections
for waveform data types, but with uncorrected spin phase offsets for spin fits and particles; or full correction
of waveform, spin fit, and particle data types.

The THEMIS L2 data products do not include any attempts to use eclipse spin model corrections.  However,
PySPEDAS includes some tools to apply the necessary corrections to the L2 data.

THEMIS spin models
^^^^^^^^^^^^^^^^^^^^

The sun sensor crossing times are incorporated into the standard "spin model" represented by a set of variables
in the THEMIS L1 STATE CDFs.  The spin model is implemented as an object with an `interp_t` method
which can be used to get the spin number, spin period. spin phase, and other diagnostic quantities
at any time.  The spin phase from the spin model, plus the spin axis right ascension and declination
from other L1 state CDF variables, completely specify the spacecraft attitude and any instant, permitting
coordinate transformations from the spinning spacecraft frame, to the despun DSL frame, and then to geophysical
coordinate frames.  For example, in the THEMIS ssl2dsl routine, we have:

.. code-block:: python

    spinmodel_obj=get_spinmodel(probe=probe, correction_level=eclipse_correction_level)

and later,

.. code-block:: python

    logging.info('Using spin model to calculate phase versus time...')
    result = spinmodel_obj.interp_t(in_times, use_spinphase_correction=use_spinphase_correction)
    spinmodel_phase = result.spinphase * pi / 180.0

.. autofunction:: pyspedas.projects.themis.get_spinmodel
.. automethod:: pyspedas.projects.themis.state_tools.spinmodel.spinmodel.Spinmodel.interp_t

Note the correction_level parameter in the get_spinmodel() call:  this value specifies the level
of eclipse spin model corrections to apply when calculating the spinmodel phase vs time. The default value
is 0 (standard model only, no eclipse corrections), 1 (correction for eclipse spin period changes,
suitable for waveform data), or 2 (full corrections including constant spin phase offset, suitable for EFI and
FGM spin fits. and particle data products).

Finding the spin model correction status of a given eclipse
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is often useful to know whether eclipse spin model corrections were partially or fully successful
for a given eclipse.  This can be done with the spinmodel method eclipse_correction_status().

.. automethod:: pyspedas.projects.themis.state_tools.spinmodel.spinmodel.Spinmodel.eclipse_correction_status

Applying eclipse spinmodel corrections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PySPEDAS users will generally not have to worry about dealing directly with the spin model objects.
Instead, we provide two more user-friendly methods to perform eclipse spin model corrections.

The first option is to use apply_eclipse_corrections=True with the THEMIS load routines when working
with THEMIS L2 data products.  Specifying this flag will apply the appropriate level of eclipse spin
model corrections to each variable loaded.

The other option, useful if the variable to be corrected is not one of the standard THEMIS L2 variables,
is to call one of the following routines, depending on whether the data to be corrected consists of vectors,
or tensors.  (Examples of tensor quantities include the pressure "ptens" and momentum flux "mftens" quantities
found in the MOM, ESA, or SST L2 CDFs.  For THEMIS, they are represented as 6-element arrays. with the remaining
three elements in the 3x3 rank 2 tensor obtained via symmetry.)

.. autofunction:: pyspedas.projects.themis.eclipse_spinmodel_corrections_vector
.. autofunction:: pyspedas.projects.themis.eclipse_spinmodel_corrections_tensor

Electron density estimates from spacecraft potential
------------------------------------------------------

.. autofunction:: pyspedas.projects.themis.scpot2dens
.. autofunction:: pyspedas.projects.themis.scpot2dens_nishimura

