PySPEDAS developers guide
============================

Coming soon
------------
The items here are mostly stubs to be filled in later.

Directory hierarchy and project layout
---------------------------------------

Stylistic guidelines
--------------------

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



