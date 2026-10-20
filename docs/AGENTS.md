---
related_files:
  - AGENTS.md
  - pyproject.toml
  - .readthedocs.yaml
  - docs/requirements.txt
  - docs/Makefile
  - docs/make.bat
  - docs/source/conf.py
  - docs/source/index.rst
  - docs/source/devguide.rst
  - docs/source/contributing.rst
  - CONTRIBUTING.md
  - README.md
  - docs/source/projects.rst
  - docs/source/coords.rst
  - docs/source/geopack.rst
  - docs/source/utilities.rst
  - docs/source/analysis.rst
  - docs/source/akebono.rst
  - docs/source/_static
maintenance: |
  Update when documentation layout, Sphinx configuration, build dependencies,
  publishing workflow or conventions for documenting new tools change. Keep the
  parent AGENTS.md overview consistent with this guidance.
---

# PySPEDAS documentation

The definitive documentation is at
[pyspedas.readthedocs.io](https://pyspedas.readthedocs.io/). Pushing to `master`
triggers a rebuild on Read the Docs.

## Source layout

- `docs/source/` contains the reStructuredText (RST) pages and indices.
  `docs/source/index.rst` is the main index; it links to the mission index in
  `docs/source/projects.rst` and to pages for other features and developer guides.
- Mission pages follow the mission package structure. Other pages cover groups
  of tools, including coordinate transforms (`docs/source/coords.rst`), field
  modeling (`docs/source/geopack.rst`), utilities (`docs/source/utilities.rst`)
  and analysis (`docs/source/analysis.rst`).
- `docs/source/_static/` holds static assets, including example plot images.
- `docs/source/conf.py` configures Sphinx with `sphinx_rtd_theme`, autodoc and
  Napoleon; Napoleon processes NumPy-style docstrings.
- `docs/Makefile` and `docs/make.bat` provide local build commands.

## Building and publishing

The `doc` dependency group in `pyproject.toml` lists the additional local build
tools: Sphinx and the Read the Docs theme. Install these alongside PySPEDAS and
its runtime dependencies, since autodoc imports the package to read docstrings.
With the build environment active, run `make html` from `docs/` (or
`make.bat html` on Windows). The HTML output is written to `docs/build/html/`.

`.readthedocs.yaml` points Read the Docs to `docs/source/conf.py` and installs the
requirements from `docs/requirements.txt`. That requirements file includes the
Sphinx tools and package dependencies needed for the hosted build. When changing
build dependencies, keep the local `doc` group and the hosted requirements
consistent with their respective roles.

## Documenting functions and examples

Use `.. autofunction::` with the function's import path to render its docstring
in an RST page. This is used extensively for function arguments, return values,
usage notes and examples. Update the function's NumPy-style docstring when its
interface or behavior changes; the RST page draws that content from the code.

Loader docstrings often include example code. Mission RST pages may repeat an
example in a `.. code-block:: python` block and include a static sample plot with
an `.. image::` or `.. figure::` directive. `docs/source/akebono.rst` demonstrates
this pattern. Keep repeated examples synchronized with their docstrings and
ensure any plot image matches the example it illustrates. Sphinx includes these
static images; it does not regenerate the plots from those code blocks.

## Developer and contributor guidance

`docs/source/devguide.rst` holds the detailed human development process.
`CONTRIBUTING.md` provides a contributor checklist and `README.md` a brief
introduction with links. Keep `docs/source/contributing.rst` consistent with
those documents and link to the developer guide for details. When changing
workflow guidance, check the actual CI configuration and keep these summaries
and the parent AGENTS.md consistent.

## Adding documentation

- Every new mission must have its own RST page under `docs/source/` and an entry
  in the toctree in `docs/source/projects.rst`, which is linked from the main
  index. Include the relevant loader functions and useful examples.
- Add new analysis tools to an appropriate existing RST page. For a new group
  of tools, create a dedicated RST page and add it to the appropriate toctree
  reachable from `docs/source/index.rst`.
- Build the HTML after changing RST, docstrings or Sphinx configuration. Review
  build warnings and inspect the affected pages for missing references,
  incorrectly rendered docstrings, examples and images.
