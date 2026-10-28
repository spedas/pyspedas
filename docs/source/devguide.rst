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

Use NumPy-style docstrings for user-facing functions. Describe parameters and
accepted data types, return values, usage notes and examples. Update the docstring
whenever the interface or behavior changes. These docstrings support both
Python's ``help()`` and the HTML documentation generated by Sphinx.

Documentation
^^^^^^^^^^^^^

The definitive documentation is at
`pyspedas.readthedocs.io <https://pyspedas.readthedocs.io/>`_. We build it with
Sphinx and the Read the Docs theme. The ``docs/`` directory contains the RST
sources, indices, images and build scripts. Pushing to ``master`` triggers a
rebuild on Read the Docs.

Pages under ``docs/source/`` follow the package structure: mission pages describe
load routines, while other pages cover coordinate transforms, field modeling,
utilities and analysis tools. ``docs/source/index.rst`` is the main index;
``docs/source/projects.rst`` indexes mission pages.

Documenting a function
~~~~~~~~~~~~~~~~~~~~~~

RST pages use Sphinx's ``autofunction`` directive extensively to render function
docstrings. For a new user-facing routine, add an ``autofunction`` entry to an
appropriate page, as well as a complete NumPy-style docstring in the source code.
Sphinx's autodoc extension imports the function and extracts its docstring;
Napoleon formats the NumPy-style sections.

For example, an RST section documenting the THEMIS search-coil magnetometer
loader can begin with:

.. code-block:: rst

   Search-coil magnetometer (SCM)
   -----------------------------
   .. autofunction:: pyspedas.projects.themis.scm

Loader docstrings often include example code. A mission page may repeat that
example in a Python code block and display a static sample plot. For example,
``docs/source/themis.rst`` includes:

.. code-block:: rst

   .. code-block:: python

      import pyspedas
      from pyspedas import tplot
      scm_vars = pyspedas.projects.themis.scm(
          probe='d', trange=['2013-11-05', '2013-11-06'])
      tplot(['thd_scf_btotal', 'thd_scf_gse'])

   .. image:: _static/themis_scm.png
      :align: center
      :class: imgborder

Keep examples repeated in docstrings and RST pages synchronized. Place plot
images in ``docs/source/_static/`` and ensure they illustrate the corresponding
example. Sphinx includes these static files; it does not execute these code
blocks to regenerate plots.

Every new mission needs its own RST page and an entry in the toctree in
``docs/source/projects.rst``. Add new analysis tools to an appropriate existing
page. For a new group of tools, create a dedicated page and add it to a toctree
reachable from ``docs/source/index.rst``.

Building the HTML locally
~~~~~~~~~~~~~~~~~~~~~~~~~

Install PySPEDAS and its runtime dependencies in your development environment,
plus the additional tools in the ``doc`` dependency group in ``pyproject.toml``:
Sphinx and the Read the Docs theme. Autodoc needs the package dependencies because
it imports the source code. With that environment active, run:

.. code-block:: bash

   cd docs
   make html

On Windows, use ``make.bat html`` from ``docs/``. Open
``docs/build/html/index.html`` and inspect the affected pages. Review build
warnings for unresolved references, missing images and docstring formatting
problems before requesting review.

The hosted build is configured by ``.readthedocs.yaml``, which points to
``docs/source/conf.py`` and installs ``docs/requirements.txt``. Keep the local
``doc`` group and hosted requirements consistent with their respective roles
when changing documentation build dependencies.


Linters
^^^^^^^

External dependencies
---------------------

Things to consider before adding a new dependency to the project requirements

Testing and CI/CD
------------------

Adding and running tests
^^^^^^^^^^^^^^^^^^^^^^^^

Every new feature or bug fix should include one or more tests using Python's
``unittest`` framework. For a bug fix, add a regression test that exercises the
original failure. Test modules normally live in a ``tests/`` directory beside
the relevant source code. Use nearby suites as examples and run the relevant
modules locally before submitting a pull request, for example:

.. code-block:: bash

   python -m pyspedas.utilities.tests.test_utilities_misc

Most mission tests download real data, so they need network access. Configure
``SPEDAS_DATA_DIR`` or the relevant mission-specific data directory for your test
environment. For functionality shared with IDL SPEDAS, also consider validation
tests that compare results between implementations.

Choosing a CI workflow and shard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The testing workflows are YAML files under ``.github/workflows/``.
They list test modules explicitly; creating a new module does not automatically
include it in CI.

* ``quick_tests.yml`` runs selected modules in sequence on pushes and pull
  requests, and can also be triggered manually. It provides relatively quick,
  reliable feedback rather than complete coverage. Leave out tests requiring
  lengthy calculations, large downloads or slow or unreliable data servers.
* ``full_coverage.yml`` is triggered manually. It runs groups of tests in parallel
  jobs called shards, with related tests often grouped by data server or
  functionality. Examples include MMS, MAVEN and SPDF/THEMIS shards. This keeps
  long suites manageable and isolates transient data server failures. One failed
  shard does not cancel the others.

Always add a new test module to ``full_coverage.yml``, preferably in a shard that
already tests the same server or related functionality. Include it in
``quick_tests.yml`` only if it fits the runtime and reliability criteria. All
quick-test dependency policies share one module list, so register each module
only once. If you add tests to an existing module, check that the module is
already listed in the intended workflows; no additional entry is needed for
each test method.

Quick-test dependency policies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pushes and pull requests always use ``locked``. To select another policy, open
``quick_tests`` in GitHub Actions, choose **Run workflow**, select the branch,
and choose ``dependency_policy`` and ``python_version``. Python choices are
3.11, 3.12, 3.13, 3.14 and 3.15, with 3.14 as the default. Pushes and pull requests
always use Python 3.14. Availability in this menu does not guarantee that every
dependency supports that interpreter.

The dependency policies are:

* ``locked`` installs the lint, test and setup groups from ``pdm.lock``, then
  lets pip resolve runtime dependencies when installing the built wheel with
  the ``mth5`` extra. This preserves normal pip installation behavior; runtime
  versions are not forced to match the lockfile.
* ``latest`` ignores the lockfile and eagerly upgrades direct and transitive
  dependencies to their newest compatible stable releases, including test and
  build tools, subject to a seven-day upload cutoff.
* ``oldest`` ignores the lockfile and uses uv's ``lowest-direct`` resolution for
  direct runtime dependencies and the ``mth5`` extra. Transitive dependencies
  and test tools use newer compatible releases. The seven-day upload cutoff
  also applies to this policy. Runtime pins remain constrained during wheel
  installation so development tools cannot silently upgrade them.

All three policies use the selected Python version and the same test list.
Oldest-version resolution respects that interpreter and package compatibility
metadata; it may select versions above declared lower bounds, and old
distributions that cannot build or run on the selected Python can still fail
the job. Such failures should be
investigated rather than bypassed by automatically switching to newer versions.

The two unlocked policies compute one UTC cutoff per job for resolution,
installation and dependency builds. Resolver tools are installed separately
from the test environment. The workflow uploads policy metadata, installation
reports, installed versions and, for ``oldest``, resolved runtime pins even when
tests fail. Dependency resolution must succeed; there is no fallback to the
lockfile. The repository lockfile and dependency declarations are not rewritten.

When a shard fails because of a transient data server failure, manually rerun
the failed jobs in the same workflow run. Successful shards need not be rerun.
The workflow does not retry failures automatically. Investigate code or assertion
failures rather than treating them as server outages. Once all shards succeed,
the workflow combines their coverage data and uploads the report to Coveralls.

Submitting a pull request
-------------------------

Start work in a separate branch from up-to-date ``master``, using a personal fork
if you do not have push access to the repository. The ``master`` branch is
protected; changes must arrive through a pull request and receive human review
from a package maintainer.

Before requesting review:

#. Run the relevant tests and describe the results, including any failures or
   tests you could not run.
#. Register new test modules in the appropriate CI workflows and shards.
#. Update docstrings and RST pages for new or changed user-facing functionality,
   build the HTML and inspect the affected pages.
#. Review ``git status`` and the diff. Stage intended new source files, tests,
   documentation pages and images with ``git add``. This includes files created
   by a coding assistant; untracked files will not be included in a commit unless
   staged. Keep downloaded data, local environments and scratch files out of the
   commit.
#. Commit and push your branch, then create a pull request targeting ``master``.
   Explain the problem, the resulting behavior, and how you tested and documented
   the change.

If the change fully resolves a GitHub issue, use a closing keyword such as
``Fixes #123`` in the pull request description to close it when the PR is merged
into ``master``. A branch name or ordinary issue mention alone does not establish
that closing relationship. See GitHub's
`issue linking guidance <https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue>`_.

A maintainer reviews and squash-merges approved pull requests. Once merged, the
issue branch can be deleted. Start subsequent work in a fresh branch from
updated ``master``, even if the issue is reopened; reusing a squash-merged branch
can complicate subsequent PR history and may cause merge conflicts.


Build and release process
--------------------------

Release preparation uses two Zenodo workflows:

#. Run ``zenodo_draft`` manually on the release branch.  It creates or reuses a
   draft in the configured concept, reserves a version DOI, updates
   ``project.urls.Versioned_DOI`` in ``pyproject.toml``, and commits the change.
#. Complete testing, merge the branch, publish to PyPI, and publish the GitHub
   release in the usual way.
#. After publishing the GitHub release, run ``zenodo_upload`` manually and
   provide its release tag.  It verifies that the DOI in the tagged source
   matches the open draft, replaces the draft payload with GitHub's tagged
   source zip, and leaves the record unpublished.  Once the production workflow
   has been validated, this manual trigger can be replaced with a
   ``release: types: [published]`` trigger.
#. Inspect and update the metadata and files on Zenodo, then publish the record
   manually.  This final step is the irreversible QA gate.

The production token is stored as the ``ZENODO_API_KEY`` Actions secret.  For
sandbox testing, also configure ``ZENODO_SANDBOX_API_KEY`` and supply the
sandbox concept record ID when dispatching ``zenodo_draft``.  The older secret
names ``ZENODO_API_TOKEN`` and ``ZENODO_SANDBOX_API_TOKEN`` are accepted as
fallbacks.

Both workflows use ``pyspedas.utilities.zenodo_draft.ZenodoDraftClient`` rather
than an external Zenodo action.  The client retries read-only requests during
transient service failures, but never automatically retries writes whose result
may be ambiguous.  It deliberately provides no record-publication operation;
publication remains a manual QA decision.

DOI management
--------------

The concept DOI (all versions) is |concept_doi|.  The DOI for this version is
|versioned_doi|.  Both values come from ``[project.urls]`` in
``pyproject.toml``; do not maintain duplicate DOI constants.

At runtime, ``pyspedas.get_doi()`` returns the versioned DOI and
``pyspedas.get_doi("concept")`` returns the concept DOI.  It reads installed
package metadata from a wheel, or ``pyproject.toml`` when run in a Git checkout.
