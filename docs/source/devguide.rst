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

1) Use Anaconda to install the version of Python you'd like to use, and set up a virtual environment to be used for your PySPEDAS development.

For detailed instructions on installing Python, please refer to :ref:`Installing Python <installing-python>` on the :ref:`Getting Started <getting-started>` page.
This guide will assume that you called your new Anaconda virtual environment 'pyspedas_dev_py310'.


2) If you don't already have it, download and install the PyCharm Interactive Development Environment (IDE).  For detailed instructions,
please refer to :ref:`Installing PyCharm <installing-python>` on the :ref:`Getting Started <getting-started>` page, or PyCharm's
own installation guide at https://www.jetbrains.com/help/pycharm/installation-guide.html .

3) Set up a GitHub access token to give PyCharm access to perform actions using your GitHub account.  Open the PyCharm settings
and navigate to Setting->Version Control->Github:

.. image:: _static/pycharm_github_credentials1.png
   :align: center
   :class: imgborder

Click on the '+' control to add your Github credentials.

.. image:: _static/pycharm_github_login_token.png
   :align: center
   :class: imgborder

Select the "Log in with Token" option:

.. image:: _static/pycharm_generate_access_token.png
   :align: center
   :class: imgborder

then click "Generate".

This will take you to a GitHub authentication page.  Once you've authenticated yourself, it should automatically
take you to a token generation page with many options which can be set for the access privileges that will be enabled with this
token.

.. image:: _static/github_new_token_page.png
   :align: center
   :class: imgborder


Take the defaults, then scroll down to the bottom of the page and click the "Generate" button.


.. image:: _static/github_generate_token.png
   :align: center
   :class: imgborder


This should bring you to a page showing the token value.   Be sure to copy it to your clipboard here -- once you leave this page, there's
no way to get back to it and you'll need to start over!


.. image:: _static/github_token_value.png
   :align: center
   :class: imgborder


When you've copied the generated token, navigate back to the PyCharm dialog and paste the token value into the control.

.. image:: _static/pycharm_generate_access_token.png
   :align: center
   :class: imgborder

Now that you've connected PyCharm to your GitHub account, you can create a PyCharm project from the GitHub repo.

.. image:: _static/pycharm_project_from_version_control.png
   :align: center
   :class: imgborder

4) Open PyCharm and choose File->Project from Version Control...


.. image:: _static/pycharm_clone_repo.png
   :align: center
   :class: imgborder


5)  Select GitHub from the left pane, then select the spedas/pyspedas repository (PySPEDAS
    team members) or your fork of the repo (outside contributors).   PyCharm
    will automatically populate the "Directory" control.  You should probably
    change the name to match the Conda environment you set up in step 1 (here, 'pyspedas_dev_py310').
    See the screenshot above showing where to make these selections.

6) Click the "Clone" button.  PyCharm will clone the PySPEDAS repo into the directory you specified.

7) When the clone operation completes, open your new PyCharm project in a new PyCharm window.

8)  Depending on your PyCharm settings, it may have already created a project interpreter for your project.  We
    need to replace it with the Conda environment you created in step 1.  Delete any .venv or venv folder it
    might have created for you in the top level project directory.  Near the bottom right corner of the PyCharm window is a control
    that will let you set up the project interpeter:

.. image:: _static/pycharm_python_environment.png
   :align: center
   :class: imgborder

Click on that, then click "Add new interpreter" in the menu that appears, then click "Add local interpreter".

.. image:: _static/pycharm_change_project_environment.png
   :align: center
   :class: imgborder

An "Add Python interpreter" dialog will appear.

.. image:: _static/pycharm_add_conda_interpreter.png
   :align: center
   :class: imgborder

For the "Environment" control, click on "Select existing".
In the "Type:" dropdown, select "Conda".  In the "Environment" dropdown, you should see the Conda environment
you created in step 1.  Select it, then click "OK" to create the environment.   See the above screenshot highlighting
the locations of the PyCharm controls.

It may take a few minutes for PyCharm to set up and index the project environment.

Next, you'll need to install some development tools to manage your PySPEDAS project.

9)  PySPEDAS uses the pdm package management tool to manage the pyspedas environment.  We also recommend using 'uv'
    to install dependencies.  Your new Conda environment should already have 'pip' installed, so we'll use pip to
    install pdm and uv. Open a terminal window and run the following pip commands:

.. code-block:: bash

    pip install pdm
    pip install uv



10)  Ensure that the PyCharm terminal is using the pdm and uv installations you just created, rather than some installation
    in a different, isolated environment.  Closing and reopening the terminal window, or closing and reopening the PyCharm
    project should accomplish this.

11)  After successfully installing pdm and uv, configure pdm to use uv:

.. code-block:: bash

    pdm config use_uv true

12)  Now you are ready to install the dependencies needed for PySPEDAS.  Do this in the terminal window with:

.. code-block:: bash

    pdm sync

This should install all the runtime, optional, and development dependencies.

13) If any package dependencies failed to install cleanly with 'pdm sync', you may need to install
    them with conda instead.  This is rare on Linux or Windows, but may happen on Mac, depending on what MacOS and
    Python versions you're using.  For any packages that failed to install, try installing them with conda instead:


.. code-block:: bash

    conda install -c conda-forge netcdf4


Repeat for each package that failed to install.  Then try 'pdm sync' again to see if any other installation failures occurred.

14) Once you've successfully installed all the PySPEDAS dependencies, you
    should be ready to test your installation!

    Quick "smoke check": open a Python  console window and "import pyspedas".  There should be no
    errors.

    If that works, I would recommend running the tests in the mth, projects/secs,
    and vires directories.  There are the ones most likely to suffer from
    dependency installation issues.   If any of those tests fail, there should
    be some indication of which package caused it.  Try installing it with

.. code-block:: bash

    conda install -c conda-forge <package>

then retest.

If that set of tests all work, congratulations!  Your PySPEDAS installation
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



