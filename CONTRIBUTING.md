# How to Contribute
## Report Issues
The easiest way to contribute to pySPEDAS is to report bugs or issues that you come across; you can submit bug reports by creating a GitHub Issue, by emailing the SPEDAS email list, or by emailing one of the project maintainers directly. We prioritize issues / bug reports over all other contributions.

## Bugfixes
Fixes to bugs you come across are always welcomed, and can be added by creating a pull request. If you would like to submit a bug fix without signing up for a Github account, you can also email the SPEDAS team directly with your code. 

## Documentation
We strive to have complete, easy to understand documentation for all user-facing routines. An easy way to contribute to pySPEDAS is to improve our documentation. We use standard, numpy-style docstrings in our code to allow users to access the documentation using the help() function. As a user's guide, we use README.md (markdown) files in each project directory; this is where we show information on each mission, such as datasets available, acknowledgements and provide a few examples. 

## Tests
We use GitHub Actions to run our test suite automatically on every commit to the repository, and coveralls.io to measure code coverage. We use Python's unittest framework to implement these tests, and examples can be found in the 'tests' directory of any mission. 

## Validation Tests
We also implement validation scripts, which load data and print several data points; these files are typically stored in the 'tests/validation/' directories, and are called from our IDL test suite to validate that the data loaded/calculated in our IDL code matches that in our Python code. 

## New Missions
We have a robust, well-tested template for adding new missions to pySPEDAS. If you would like to contribute a new mission or project to pySPEDAS, please contact the SPEDAS team for the latest copy of the template. 
