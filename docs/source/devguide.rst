PySPEDAS developers guide
============================

Coming soon
------------
The items here are mostly stubs to be filled in later.

Setting up a development environment for PySPEDAS maintainers and contributors is a little different than the type
of setup an end user might do.   You will want to clone PySPEDAS from the GitHub repository, rather than installing some
PyPI release.   This lets you either commit your changes to the official repo (PySPEDAS core maintainers), or a personal fork
of the official repo (outside contributors).

PySPEDAS uses pdm and uv to manage your virtual environment.  These tools will need to be installed and configured in your environment
before completing the rest of the setup.  The PySPEDAS pyproject.toml file also defines a number of developer dependencies you might find
useful for formatting, linting, and building PySPEDAS.

Setting up a PyCharm development environment for PySPEDAS
----------------------------------------------------------

1) Create a new environment in Anaconda to use with your new PySPEDAS development project.  Use a descriptive name, e.g. pyspedas_pycharm_dev_310

2) Open PyCharm and choose File->Project from Version Control

3)  Select GitHub from the left pane (assuming you've already set up your
    GitHub credentials), then select the spedas/pyspedas repository (PySPEDAS
    team members) or your fork of the repo (outside contributors).   PyCharm
    will automatically populate the "Directory" control.  You should probably
    change the name to match the Conda environment you set up in step 1.

4) Click the "Clone" button.  PyCharm will clone the PySPEDAS repo into the directory you specified.

5) When the clone operation completes, open your new PyCharm project in a new PyCharm window.

6)  Depending on your PyCharm settings, it may create a project interpreter for your project.  We
    need to replace it with the Conda environment you created in step 1.  Delete any .venv or venv folder it
    might have created for you.  Near the bottom right corner of the PyCharm window is a control
    that will let you set up the project interpeter.  Click on that, then click "Add new interpreter"
    in the menu that appears, then click "Add local interpreter".   An "Add Python interpreter" dialog
    An "Add Python interpreter" dialog will appear.  For the "Environment" control, click on "Select existing".
    In the "Type:" dropdown, select "Conda".  In the "Environment" dropdown, you should see the Conda environment
    you created in step 1.  Select it, then click "OK" to
    create the environment.

7)  PySPEDAS uses the pdm package management tool to manage the pyspedas environment.  We also recommend using 'uv'
    to install dependencies.  Your new Conda environment should already have 'pip' installed, so we'll use pip to
    install pdm and uv. Open a terminal window and run the following pip commands:

    pip install pdm

    pip install uv

8)  Ensure that the PyCharm terminal is using the pdm and uv installations you just created, rather than some installation
    in a different, isolated environment.  Closing and reopening the terminal window, or closing and reopening the PyCharm
    project should accomplish this.

8)  After successfully installing pdm and uv, configure pdm to use uv:

    pdm config use_uv true

9)  Now you are ready to install the dependencies needed for PySPEDAS.  Do this in the terminal window with:

    pdm sync

    This should install all the runtime, optional, and development dependencies.

10) If any package dependencies failed to install cleanly with 'pdm sync', you may need to install
    them with conda instead.  This is rare on Linux or Windows, but may happen on Mac, depending on what MacOS and
    Python versions you're using.  For any packages that failed to install, try installing them with conda instead:


    conda install -c conda-forge netcdf4

    Repeat for each package that failed to install.  Then try 'pdm sync' again to see if any other installation failures occurred.

11) Once you've successfully installed all the PySPEDAS dependencies, you
    should be ready to test your installation!

    Quick "smoke check": open a Python  console window and "import pyspedas".  There should be no
    errors.

    If that works, I would recommend running the tests in the mth, projects/secs,
    and vires directories.  There are the ones most likely to suffer from
    dependenciy installation issues.   If any of those tests fail, there should
    be some indication of which package caused it.  Try installing it with

    conda install -c conda-forge <package>

    then retest.

    If that set of tests all work, congratualtions!  Your PySPEDAS installation
    should be in good shape to start developing!

    One last thing: you might want to check your project-specific PyCharm settings
    to make sure they're correct.  For example:

    In Python->Plots, the "show plots in tool window" option should probably be
    unchecked.

    In Python->Integrated Tools, the docstring format should be set to "NumPy".

Setting up a PySPEDAS development environment in Visual Studio Code
--------------------------------------------------------------------

TBD

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



