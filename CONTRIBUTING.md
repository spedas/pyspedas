# Useful resources
* Email point of contact for PySPEDAS developers: <jwl@ssl.berkeley.edu>
* PySPEDAS code: [PySPEDAS Github repository](https://github.com/spedas/pyspedas)
* Documentation: [SPEDAS and PySPEDAS wiki](https://spedas.org/wiki)
* PySPEDAS example repositories, including many Jupyter notebooks
  * [PySPEDAS examples](https://github.com/spedas/pyspedas_examples)
  * [THEMIS examples](https://github.com/spedas/themis-examples)
  * [MMS examples](https://github.com/spedas/mms-examples)

# How to Contribute

The PySPEDAS project welcomes contributions from users, developers, and community members at any experience level.  We strive to create a welcoming, respectful, safe, and inclusive environment, as embodied in our Code of Conduct.

__Impostor syndrome disclaimer__: Yes, this includes you! Even if you're new to the heliophysics field, new to Python programming, or just a little nervous about getting involved, we are grateful for any effort you are willing to
undertake in order to make PySPEDAS a more powerful, easier to use, and better documented package. 

Contributions may take many forms other than coding or bug fixing!

## Ask Questions
Are you having trouble downloading, installing, or using PySPEDAS?  Do you have questions about how the various tools work?  Are you wondering how to accomplish a certain workflow in PySPEDAS, or if there's some other package that might 
be a better fit?  Let us know!  In addition to helping you with your specific issue, asking questions helps PySPEDAS developers see where our documentation might need improvement, or our design might need to be adjusted to make things easier
or more clear.  You can ask a question by opening a new issue on our Github repository and tagging it with the "question" label, or by emailing the PySPEDAS team directly.


## Report Issues
The easiest way to contribute to pySPEDAS is to report bugs or issues that you come across; you can submit bug reports by opening an issue on our Github repository (the preferred channel, if you are already on Github), or by emailing one of the project maintainers directly.   

Try to include as much information as possible about your environment (operating system, Python version, PySPEDAS version), what you were trying to do (code snippet that we can use to reproduce the issue), what you expected to happen, and what actually happened (log output or error messages, system crashed or stopped responding, plots didn't look right...)

## Fix bugs
Fixes to bugs you come across are always welcomed, and can be added by creating a pull request. If you would like to submit a bug fix without signing up for a Github account, you can also email the SPEDAS team directly with your code. 

## Suggest enhancements
Is there a capability or tool you'd like to see included in PySPEDAS?  If you already have some code that does what you want, fantastic!  Send us a pull request and we'll take a look!  Otherwise, please feel free to open a Github issue, or email the developers directly, and let us know what you'd like us to add. 

## Add, update, edit, or translate documentation
We strive to have complete, easy to understand documentation for all user-facing routines. An easy way to contribute to pySPEDAS is to improve our documentation. We use standard, numpy-style docstrings in our code to allow users to access the documentation using the help() function. As a user's guide, we use README.md (markdown) files in each project directory; this is where we show information on each mission, such as datasets available, acknowledgements and provide a few examples.

We some (rather sparse, at the moment) documentation available on the SPEDAS wiki.  It takes a fair amount of effort to keep this up to date with new PySPEDAS features, and we can always use some help in that department.

If you're fluent enough in another language to help translate some of our documentation, that would be an outstanding act of service to the PySPEDAS user community!

We like to provide lots of code examples of how to use individual PySPEDAS tools, perform larger workflows using several different tools, or use PySPEDAS in conjunction with other PyHC packages.  Our preferred way of sharing examples is via Jupyter notebooks.  We maintain several Github repositories (under the SPEDAS Github organization) for notebooks focusing on
the THEMIS/ARTEMIS and MMS missions, and general PySPEDAS and PyTplot capabilities.  

If you've created something that might interest or help other PySPEDAS users, please feel free to share it (preferably as a Github pull request, or by emailing the maintainers) and we'll be happy to take a look.

## Add Unit Tests
We use GitHub Actions to run our test suite automatically on every commit to the repository, and coveralls.io to measure code coverage. We use Python's unittest framework to implement these tests, and examples can be found in the 'tests' directory of any mission. 

## Add Cross-Validation Tests
We also implement validation scripts, which load data and print/compare some subset of the test outputs with results from IDL SPEDAS or other relevant tools.
These files are typically stored in the 'tests/validation/' directories, and (for example) might be called from our IDL test suite to validate that the data loaded/calculated in our IDL code matches that in our Python code. 

## Add Support for New Missions
We have a robust, well-tested template for adding new missions to pySPEDAS. If you would like to contribute a new mission or project to pySPEDAS, please contact the SPEDAS team for the latest copy of the template, or just code it up on your own (hopefully as consistent as possible with the conventions followed by other missions), and send us a PR on Github.