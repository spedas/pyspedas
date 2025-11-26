THEMIS analysis tools
=====================

Coordinate transforms
----------------------

The THEMIS mission defines coordinate systems related to the spacecraft spin axes
(one spinning with the spacecraft, the other referenced to the sun direction).
The two ARTEMIS probes (aka THEMIS-B and THEMIS-C) are in lunar orbits, so
so a few selenocentric coordinate transforms are required.

* DSL (Despun Solar Spinaxis)
* SSE (Spinning Solar SpinAxis)
* SSL (Selenocentric Solar Ecliptic)
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


Electron density estimates from spacecraft potential
------------------------------------------------------

.. autofunction:: pyspedas.projects.themis.scpot2dens
.. autofunction:: pyspedas.projects.themis.scpot2dens_nishimura

