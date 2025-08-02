PySPEDAS 2.0 Migration Guide
============================

Upcoming changes
----------------

In the near future, we will be releasing version 2.0.0 of PySPEDAS, and there will be
some changes that affect how PySPEDAS and PyTplot routines are imported and called in
your applications that use these packages.

PyTplot will become part of PySPEDAS
------------------------------------

There is currently a rather confusing situation with the relationship between the
PySPEDAS and PyTplot packages.  This has to do with their development history. In the original IDL version of SPEDAS,
there was no real distinction between SPEDAS and tplot, just a subdirectory of the SPEDAS source
code with a relatively self-contained set of tools for storing data as "tplot variables",
and plotting or performing various operations on them.

This subset of SPEDAS was first ported to Python by Bryan Harter and some other developers at LASP,
and became the first iteration of the PyTplot package.  PySPEDAS came a few years later, with Eric Grimes at UCLA
doing most of the initial heavy lifting.  It turned out that having PyQt as a PyTplot dependency caused some difficulty
when installing and using PySPEDAS under certain circumstances.  This led to the creation of a fork of the PyTplot
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


Converting older PySPEDAS code for version 2.0 compatibility
-------------------------------------------------------------

The changes needed to make your code work with PySPEDAS 2.0 are very straightforward, and mostly involve your import statements, and
any fully-qualified calls that include the pytplot or pyspedas.mission prefixes.
There is no need to wait until the PySPEDAS 2.0 release to update your code -- all the new constructs have
been supported by PySPEDAS versions released since early 2024.

There are several types of changes that you may need to make::

pytplot imports and calls::

   1. All imports from the `pytplot` package should be changed to import from the top level PySPEDAS namespace instead.
   2. All fully-qualified calls of the form `pytplot.some_func()` should be changed to `pyspedas.some_func()`
   3. Imports or fully qualified calls from pytplot submodules like tplot_math will no longer be supported, and should use the top-level pyspedas namespace instead.

pyspedas mission-specific imports and calls::

   1. All imports of mission-specific code should use `pyspedas.projects.mission` rather than `pyspedas.mission`.
   2. Fully qualified calls of the form `pyspedas.mission.some_func()` should be changed to `pyspedas.projects.mission.some_func()`
   3. Imports or fully qualified calls to mission-specific modules will still be supported, but will need to use `pyspedas.projects.mission.module` rather than `pyspedas.mission.module`

Obsolete wrapper routines being removed::

    1. pyspedas.cotrans_get_coord() should be replaced with pyspedas.get_coord()
    2. pyspedas.cotrans_set_coord() should be replaced with pyspedas.set_coord()

Updating pytplot imports
++++++++++++++++++++++++

Old style, pre-2.0:

.. code-block:: python

    import pytplot
    from pytplot import store_data, get_data, tplot
    from pytplot.tplot_math import subtract_average
    my_data = pytplot.get_data('my_variable')
    pytplot.importers.tplot_restore('some_file.tplot')


PySPEDAS 2.0 compatible rewrites:

.. code-block:: python

    # Use "import pyspedas" rather than "import pytplot"
    import pyspedas

    # Use "from pyspedas import some_func" rather than "from pytplot import some_func"
    from pyspedas import store_data, get_data, tplot

    # Import from top-level pyspedas namespace, rather than internal modules like tplot_math
    # There is no guarantee that pyspedas will have the same module structure as
    # pytplot -- all imports should come from the top level pyspedas namespace
    from pyspedas import subtract_average

    # Fully-qualified calls will need to be updated to use pyspedas rather than pytplot
    my_data = pyspedas.get_data('my_variable')

    # Fully-qualified calls from pytplot modules like `tplot_math` or `importers`
    # should use the top-level pyspedas namespace instead
    pyspedas.tplot_restore('some_file.tplot')


Updating mission-specific imports and calls
+++++++++++++++++++++++++++++++++++++++++++

Old style, pre-2.0:

.. code-block:: python

    from pyspedas.themis import state
    from pyspedas.mms.particles import mms_part_getspec
    pyspedas.omni.load(trange=["2013-11-5", "2013-11-6"])


PySPEDAS 2.0 compatible rewrites:

.. code-block:: python

    # Use "from pyspedas.projects.mission import some_func" rather than
    # "from pyspedas.mission import some_func"
    from pyspedas.projects.themis import state

    # Mission module structures have not changed!  Deep imports from sub-modules are still OK,
    # as long as "pyspedas.mission" is changed to "pyspedas.projects.mission"
    from pyspedas.projects.mms.particles import mms_part_getspec

    # Direct calls will also need to be updated to use pyspedas.projects
    pyspedas.projects.omni.load(trange=["2013-11-5", "2013-11-6"])


Updating references to obsolete wrapper routines
+++++++++++++++++++++++++++++++++++++++++++++++++

Old style, pre-2.0:

.. code-block:: python

    # cotrans_get_coord and cotrans_set_coord are wrapper routines, which will be removed in PySPEDAS 2.0
    from pyspedas import cotrans_get_coord, cotrans_set_coord
    coord = cotrans_get_coord('somevar')
    cotrans_set_coord('somevar', 'GSE')


PySPEDAS 2.0 compatible rewrites:

.. code-block:: python

    # Import or call set_coord and get_coord from pyspedas namespace
    from pyspedas import get_coord, set_coord
    coord = get_coord('somevar')
    set_coord('somevar', 'GSE')


Updating your environment after upgrading to PySPEDAS 2.0 or later
--------------------------------------------------------------------

After upgrading PySPEDAS to version 2.0, we recommend that you remove the pytplot package:

.. code-block:: bash

    pip uninstall pytplot


Once you install PySPEDAS 2.0, the pytplot package will no longer be needed.  Removing it ensures that you'll catch any stray
references to the old pytplot versions of pyspedas tools, which, if left in place, could lead to using obsolete code.

For a period of time after PySPEDAS 2.0 is released, we may add code to detect whether pytplot is still installed, and
remind you that we recommend uninstalling it.

If you're installing PySPEDAS 2.0 for the first time in a fresh virtual environment, you shouldn't have
to do anything special. Pytplot will no longer be listed as a package dependency for PySPEDAS, and your new
environment won't include it.
