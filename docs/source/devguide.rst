PySPEDAS developers guide
============================


Setting up a PySPEDAS development environment
-----------------------------------------------

In order to contribute to PySPEDAS development, you will need a Python installation compatible with PySPEDAS,
and a Python development environment (most likely PyCharm or Visual Studio Code) configured to use your
personal Github credentials to operate on the Github repository.

Install Python
^^^^^^^^^^^^^^

PySPEDAS itself is compatible with Python versions 3.10 through 3.14.  (Some dependencies for PySPEDAS extras, e.g. basemap
which is used for SECS/EICS map plots, are not quite ready for Python 3.14 yet.)  As a developer, you might want
to install several versions of Python, and set up separate development projects for each version, to ensure
that any new features or bug fixes pass their tests under all supported versions of Python.

We recommend using Anaconda to manage Python installations to be used with PySPEDAS. If some PySPEDAS dependency
(now or in the future) turns out to be difficult to install on your OS and CPU architecture, starting with
an Anaconda Python installation gives you the option of trying 'conda install' if 'pip install' fails due
to lack of a binary wheel for your platform.  (Linux or Windows installations usually don't have to worry
about this as much.  But for Macs, this is a recurring headache.)

For detailed instructions on installing Python, please refer to :ref:`Installing Python <installing-python>` on the :ref:`Getting Started <getting-started>` page.
This guide will assume that you called your new Anaconda virtual environment 'pyspedas_dev_py310'.

Install and Configure a Python Interactive Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We expect that most PySPEDAS developers, like most PySPEDAS end users, will want to use an IDE like PyCharm or Visual Studio Code to do most
of their development.   There are a few considerations for setting up a project for PySPEDAS development that
end users don't have to worry about.  Instead of installing a PySPEDAS release via 'pip', a developer install
will start with a git clone from either the main GitHub repository for PySPEDAS, or (for outside contributors)
a personal fork of the PySPEDAS repo.   In order to interact with the origin repository (pulling updated code from the repo,
committing and pushing local changes back to the repo), your development environment will need to be configured with
the appropriate GitHub credentials. You will need to install some additional utilities to manage the project dependencies,
linters to identify and fix minor errors and stylistic issues, and additional Python packages to support some of the
test scripts.

For detailed instructions on setting up a PySPEDAS development project, see :ref:`PyCharm developer install <dev-pycharm>`
or (coming soon) :ref:`Installing Visual Studio Code <dev-vscode>` .

Set PySPEDAS environment variables for local data directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may already have configured SPEDAS_DATA_DIR and other SPEDAS or PySPEDAS environment variables.
Your PySPEDAS install can use those same environment variables, so you don't end up with multiple
copies of data files for IDL SPEDAS, or different PySPEDAS development projects.

There may be situations where you might actually prefer to separate the data directories for PySPEDAS development,
and the data directories you might be using for actual science work. For example, if you're working on the
PySPEDAS download utilities or other load-routine-related code, you might need to clean out previously downloaded
files for testing purposes.  You may not want to have to do that with your 'production' data directories.
In that case, you might want to set up your Python IDE to associate some different SPEDAS/PySPEDAS environment
variables for each of your PySPEDAS development projects.

Verify that you have a working PySPEDAS installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you've successfully installed all the PySPEDAS dependencies, you
should be ready to test your installation!

For a quick "smoke check": open a Python console window and enter "import pyspedas".  The import
should work without any errors due to missing dependencies.

If that works, I would recommend running the tests in the mth, projects/secs,
and vires directories.  There are the ones most likely to suffer from
dependency installation issues.   If any of those tests fail, there should
be some indication of which package caused it.  Try installing it with

.. code-block:: bash

    conda install -c conda-forge <package>

then retest.

If that set of tests all work, congratulations!  Your PySPEDAS installation
should be in good shape to start developing!


Directory hierarchy and project layout
---------------------------------------

TBD

Stylistic guidelines
--------------------

Docstrings
^^^^^^^^^^

We use the numpy formatting conventions, and automatically generate documentation pages for pyspedas.readthedocs.io using Sphinx.

Documentation
^^^^^^^^^^^^^

Sphinx documentation at pyspedas.readthedocs.io, much of it autogenerated
from code docstrings.  Numpy comment style with some RST features to keep things
looking nice on readthedocs.


Linters
^^^^^^^

External dependencies
---------------------

Things to consider before adding a new dependency to the project requirements

Testing and CI/CD
------------------

We use the unittest framework.  Tests are triggered by pushes to the Github repo,
and are defined as yaml workflow files in the .github directory.

Ideally, features that are common to both IDL SPEDAS and PySPEDAS should have
validation tests to ensure that both platforms give reasonably comparable results.

We use coveralls.io to generate test coverage reports in some of our CI workflows.
Ideally we would maintain at least 90% code coverage for a green badge.


Build and release process
--------------------------

pyproject.toml, setuptools, semantic versioning, frequent releases, releasing via Github vs pypi

DOI management
--------------

How DOIs are minted and used in PySPEDAS metadata, code, and documentation.



