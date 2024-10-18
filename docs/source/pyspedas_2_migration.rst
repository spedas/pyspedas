PySPEDAS 2.0 Migration Guide
============================

Upcoming changes
----------------

In the near future, we will be releasing version 2.0.0 of PySPEDAS, and there will be
some changes that affect how PySPEDAS and PyTplot routines are imported and called in
your applications that use these packages.

PyTplot will become part of PySPEDAS
------------------------------------

There is currently a rather confusing situation with the relastionship between the
PySPEDAS and PyTplot packages.  This has to do with the development history of the Python
packages.  In the original IDL version of SPEDAS, there was no
real distinction between SPEDAS and tplot, just a subdirectory of the SPEDAS source
code with a relatively self-contained set of tools for storing data as "tplot variables",
and plotting or performing various operations on them.

This subset of SPEDAS was first ported to Python by Bryan Harter and some other developers at LASP,
and became the first iteration of the PyTplot package.  PySPEDAS came a few years later, with Eric Grimes at UCLA
doing most of the initial heavy lifting.  It turned out that having PyQt as a dependency caused some difficulty
when installing and using PySPEDAS under certain circumstances.  This led to a fork of the PyTplot
package that used matplotlib, rather than QT, as the back end plotting toolkit.  The forked version was
released as the pytplot-mpl-temp package, and this is what PySPEDAS now uses.

This is an ongoing source of confusion and problems for PySPEDAS users.  It is very easy
to make the mistake of doing 'pip install pytplot' rather than 'pip install pytplot-mpl-temp'
when setting up or upgrading one's PySPEDAS environment, especially since the pytplot-mpl-temp
is also imported as 'import pytplot'.

To eliminate this source of confusion, the pytplot-mpl-temp routines will be
incorporated directly into the PySPEDAS package, beginning with version 2.0.0.
It will no longer be necessary to 'import pytplot' -- all the pytplot tools will
be available directly from the pyspedas namespace.


PySPEDAS mission-specific code moved to 'projects' directory
-------------------------------------------------------------

We have moved the load routines and other tools for individual missions (MMS, THEMIS, GOES, OMNI, etc.)
to a 'projects' subdirectory and module.   For backward compatibility, we
have set up the pyspedas import structure so that "from pyspedas import mms"
or "pyspedas.themis.fgm()" still work as before, but the workaround isn't
perfect -- this involves some runtime management of the available modules,
and some IDEs (e.g. PyCharm) will mark them as potential errors because they
only do static analysis of the import structures, even though they work perfectly
at runtime.

In a future release, this workaround may be removed, and users will need to import
and call these routines from the 'pyspedas.projects' namespace:  "from pyspedas.projects import mms"
or "pyspedas.projects.themis.fgm()"
