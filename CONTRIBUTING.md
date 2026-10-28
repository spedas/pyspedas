# Useful resources
* Email point of contact for PySPEDAS developers: <jwl@ssl.berkeley.edu>
* PySPEDAS code: [PySPEDAS Github repository](https://github.com/spedas/pyspedas)
* Definitive documentation: [PySPEDAS on Read the Docs](https://pyspedas.readthedocs.io/)
* Development process and setup: [PySPEDAS developer guide](https://pyspedas.readthedocs.io/en/latest/devguide.html)
* Additional resources: [SPEDAS and PySPEDAS wiki](https://spedas.org/wiki)
* PySPEDAS example repositories, including many Jupyter notebooks
  * [PySPEDAS examples](https://github.com/spedas/pyspedas_examples)
  * [THEMIS examples](https://github.com/spedas/themis-examples)
  * [MMS examples](https://github.com/spedas/mms-examples)

# How to Contribute

The PySPEDAS project welcomes contributions from users, developers, and community members at any experience level.  We strive to create a welcoming, respectful, safe, and inclusive environment, as embodied in our Code of Conduct.

__Impostor syndrome disclaimer__: Yes, this includes you! Even if you're new to the heliophysics field, new to Python programming, or just a little nervous about getting involved, we are grateful for any effort you are willing to
undertake toward making PySPEDAS a more powerful, easier to use, and better documented package. 

Contributions may take many forms other than coding or bug fixing!

## Preparing a code contribution

Work in a separate branch, starting from an up-to-date `master`, or in a branch
in your personal fork. The `master` branch is protected; all changes require a
pull request and human review by a package maintainer.

Before requesting review:

1. Add one or more `unittest` tests for each new feature or bug fix. For a bug
   fix, include a regression test that exercises the original failure. Run the
   relevant test modules locally and report the results.
2. If you create a new test module, add it to
   `.github/workflows/full_coverage.yml` in a suitable shard. Add it to
   `.github/workflows/quick_tests.yml` only if it runs quickly and reliably.
   All dependency policies use the same quick-test module list; register each
   module only once in that workflow.
   Tests added to an existing module use its existing workflow entries; check
   that the module is included in the intended workflows.
3. Update NumPy-style docstrings and the RST documentation for new user-facing
   routines or changed parameters, data types, return values, or behavior. Build
   the HTML locally and inspect the affected pages.
4. Check `git status` and the diff. Stage intended new source files, tests, RST
   pages and images with `git add`, including files created by a coding assistant.
   Keep downloaded data, local environments and scratch files out of the commit.
5. Commit and push the branch, then open a pull request targeting `master`.
   Describe the change, tests and documentation updates. To close an issue on
   merge, use a closing keyword such as `Fixes #123` in the PR description when
   the change fully resolves that issue; merely mentioning an issue is not enough.

A maintainer reviews and squash-merges approved pull requests. After merging,
you can delete the issue branch. Start follow-up work in a fresh branch from
updated `master`, even if an issue is reopened.

See the [developer guide](https://pyspedas.readthedocs.io/en/latest/devguide.html)
for detailed testing, documentation and pull request guidance.

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
The definitive documentation lives at
[pyspedas.readthedocs.io](https://pyspedas.readthedocs.io/). We build it with Sphinx
and the Read the Docs theme from RST pages in `docs/source/`. Pushing to `master`
triggers a rebuild on Read the Docs. Mission README files and the SPEDAS wiki
provide additional resources.

Use NumPy-style docstrings for public functions and add an `.. autofunction::`
directive to the appropriate RST page so Sphinx renders the parameters, return
values, usage notes and examples. Keep docstrings current when the interface or
behavior changes. Loader examples may also appear in RST code blocks with static
sample plots; keep the repeated examples and images consistent.

New missions need their own RST page and an entry in `docs/source/projects.rst`.
Add new analysis tools to an appropriate existing page, or create a page and
index entry for a new group of tools. The `doc` dependency group in
`pyproject.toml` supplies Sphinx and its theme for local builds, alongside the
package's runtime dependencies. Run `make html` from `docs/` (`make.bat html` on
Windows), then inspect the output in `docs/build/html/` and review build warnings.
Read the Docs uses `.readthedocs.yaml` and `docs/requirements.txt` for hosted builds.

If you're fluent enough in another language to help translate some of our documentation, that would be an outstanding act of service to the PySPEDAS user community!

We like to provide lots of code examples of how to use individual PySPEDAS tools, perform larger workflows using several different tools, or use PySPEDAS in conjunction with other PyHC packages.  Our preferred way of sharing examples is via Jupyter notebooks.  We maintain several Github repositories (under the SPEDAS Github organization) for notebooks focusing on
the THEMIS/ARTEMIS and MMS missions, and general PySPEDAS and PyTplot capabilities.  

If you've created something that might interest or help other PySPEDAS users, please feel free to share it (preferably as a Github pull request, or by emailing the maintainers) and we'll be happy to take a look.

## Add Unit Tests
We use Python's `unittest` framework, with test modules in `tests/` directories
beside the source code. New features and bug fixes should include tests. Most
mission tests download real data and require network access.

The GitHub Actions workflows list the test modules to run explicitly:

- `quick_tests.yml` runs a selected sequence of tests on pushes and pull requests,
  and can also be run manually. It provides relatively quick, reliable feedback;
  it does not cover the entire package.
  Pushes and PRs use the `locked` policy: development groups come from
  `pdm.lock`, while pip resolves the wheel's runtime dependencies normally.
  Manual runs offer `locked`, `latest`, or `oldest`. The latter two use a
  seven-day release cutoff; `oldest` minimizes direct runtime dependencies,
  including the `mth5` extra, while keeping transitive dependencies and test
  tools current where compatible. Manual runs can also select Python 3.11
  through 3.15 via `python_version`, defaulting to 3.14; pushes and PRs always
  use 3.14. All policies and Python versions share the same test-module list.
  These are compatible-version resolutions, not a promise that every declared
  lower bound can be installed on the selected Python version.
- `full_coverage.yml` is run manually. It groups tests into parallel shards,
  often by data server or related functionality. Failed shards do not cancel the
  others. For transient data server failures, manually rerun failed jobs in the
  same workflow run. Once all shards succeed, coverage data is combined and
  uploaded to Coveralls.

Always register new test modules in full coverage. Include them in quick tests
only when they avoid lengthy calculations, large downloads and unreliable data
providers. Register each module once in `quick_tests.yml`; all dependency
policies share that entry. Adding a test to an existing module does not require
another workflow entry if that module is already listed in the intended workflows.

## Add Cross-Validation Tests
We also implement validation scripts, which load data and print/compare some subset of the test outputs with results from IDL SPEDAS or other relevant tools.
These files are typically stored in the 'tests/validation/' directories, and (for example) might be called from our IDL test suite to validate that the data loaded/calculated in our IDL code matches that in our Python code. 

