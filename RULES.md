# PySPEDAS repository rules

These rules apply to every change in this repository, whether a person or a
coding agent makes it. Every AGENTS.md points here, and the developer guide
(`docs/source/devguide.rst`) summarizes them for readers of the documentation.

## Breaking changes and deprecations

People run PySPEDAS from scripts, notebooks, tutorials and processing software
that we never see. A change that breaks their previously correct code has to be
phased in, so they have time to adapt.

### What counts

A breaking change is any change to the interface of a user-facing routine that
can break existing, previously correct workflows, for example:

- removing or renaming a user-facing routine;
- removing or renaming a user-facing configuration parameter;
- removing or renaming a parameter;
- removing a previously valid option for a parameter value;
- changing the interpretation of a parameter, or the internal logic of a
  user-facing routine, in a way that is inconsistent with the old behavior;
- adding or changing dependencies or dependency versions in a way that
  prevents installation on platforms or Python versions documented as
  supported.

These are not covered:

- changes to internal helper or support routines that users are not meant to
  call;
- bug fixes where the old behavior is clearly undesirable.

If it isn't clear whether a change is covered, consult the developer team
before going ahead. A coding agent asks the human it works for.

### Phasing one in

If a breaking change is necessary, keep the old construct working for a
transition period of at least several months. Remove it only in a major
release (for example, PySPEDAS 2.x to 3.0), never before. During the
transition period:

- **Warning.** Every use of the old construct logs a warning with
  `logging.warning`. The message names the deprecated construct and its
  replacement, if there is one, and contains "deprecate" or "deprecated" (in
  any case) so deprecations can be found by searching. Then translate the old
  input to the new one and continue. A Python `DeprecationWarning` may be
  raised as well, but not instead: Python shows it only when the call comes
  directly from `__main__`.
- **Tests.** CI tests call the old construct, check that it still gives the
  expected results, and check that the warning is logged (`assertLogs`).
- **Docstring.** The docstring of a deprecated routine or parameter says it is
  deprecated, using the word "deprecate" or "deprecated", and names the
  replacement.
- **Migration guide.** If a migration guide for the next major version is
  being maintained, it explains how to update code that uses the old
  construct. `docs/source/pyspedas_2_migration.rst`, the 2.0 guide, shows how
  this was done before.

Also:

- When you rename something, follow established PySPEDAS naming conventions
  where they apply; otherwise use the name from the matching IDL SPEDAS
  routine, if there is one, so that IDL workflows convert easily to Python.
- List every breaking change and deprecation in the pull request description.
- Reviewers, people and agents alike, check every pull request against
  "What counts" above.

### Example

`pyspedas.projects.themis.gmag()` replaced its `sampling_rate` parameter with
`time_resolution`. `pyspedas/projects/themis/ground/gmag.py` keeps the old
parameter working:

```python
if sampling_rate is not None:
    logging.warning('The keyword argument "sampling_rate" is deprecated. Please use "time_resolution" (specified using a string) instead. ...')

    if sampling_rate == 10:
        time_resolution = "100ms"
```

and `pyspedas/projects/themis/tests/test_themis.py` checks both the warning
and the data:

```python
def test_load_gmag_variometer_10_hz_data_notag_deprecated_param(self):
    """Load gmag variometer 10 Hz data using the deprecated sampling_rate argument and not the time_resolution argument."""
    with self.assertLogs(level=logging.WARNING) as captured:
        pyspedas.projects.themis.gmag(
            varnames=['thg_mag_s61a_100ms'],
            sites='s61a',
            sampling_rate=10,
            trange=['2026-02-24', '2026-02-25'],
        )
    self.assertTrue(any(
        record.filename == 'gmag.py'
        and 'The keyword argument "sampling_rate" is deprecated.'
        in record.getMessage()
        for record in captured.records
    ))
    self.assertTrue(data_exists('thg_mag_s61a_100ms'))
```

### Finding deprecations that don't follow these rules

`python .github/scripts/scan_deprecations.py` lists every routine whose
docstring or code mentions a deprecation, with its warnings, tests and
internal callers, and flags what is missing. Its matching is heuristic;
`.agents/skills/deprecation-scan/SKILL.md` says how to check and report the
results.

## Porting IDL SPEDAS code

When a feature being added to PySPEDAS has a counterpart in IDL SPEDAS:

- **Interface.** Give the PySPEDAS version an interface similar to the IDL
  version. Parameter and keyword names follow established PySPEDAS naming
  conventions where they apply; otherwise use the IDL SPEDAS names. If in
  doubt, consult a PySPEDAS maintainer. A coding agent asks the human it works
  for.
- **Documentation.** Name the IDL SPEDAS equivalent and clearly call out any
  differences in its API or function, for IDL SPEDAS users converting their
  workflows to Python.
- **Tests.** A new tool ported from IDL SPEDAS has tests that compare its
  results with those of the IDL version.

A common way to write those tests:

1. Write IDL SPEDAS code that performs the computation, and save its input and
   output variables in a CDF or tplot save file.
2. Commit that file to the
   [spedas/test_data](https://github.com/spedas/test_data) repository.
3. In a PySPEDAS test, download the file, run the equivalent PySPEDAS
   computation on the saved input, and compare the results with the saved IDL
   output.

IDL and Python differ in their library implementations and floating-point
behavior, so the results may not be bit-for-bit identical. It is up to the
developer to set reasonable tolerances for the comparison. For examples, see
`pyspedas/geopack/tests/test_geopack_idl_validation.py` and
`pyspedas/utilities/tests/test_tinterpol_mxn.py`.

## Clarity and simplicity

For all but the most processing-intensive tasks, prefer clarity and simplicity
to efficiency. The code should be straightforward and understandable to our
users, who may not have extensive computer science backgrounds or detailed
knowledge of Python libraries.

For example, NumPy's `einsum()` may be the most numerically efficient way to
do a computation, but a user who hasn't seen it before may find its notation
cryptic. It is almost always better to write an explicit outer loop that calls
more familiar NumPy routines on smaller chunks.

If the most concise solution uses algorithms or data structures that an
experienced heliophysics researcher might not know, consider pointing to
reference material in the documentation.

If an existing PySPEDAS routine meets most, but not all, of the requirements
for a new task, consider extending it instead of writing a new tool, if that
can be done without making it excessively complicated. Any change to how the
routine already behaves follows the breaking-change rules above.

## Dependencies

If an external package gives a clean solution to a problem but is not already
a direct or indirect PySPEDAS dependency, consider using it, but weigh the
convenience against the risks of adding a dependency:

- Is the package actively maintained?
- Does it support the same platforms and Python versions as PySPEDAS?
- Can it be installed easily with pip?

If only a small subset of users is likely to need the package, consider making
it an optional extra rather than a required dependency, like the `maps` and
`vires` extras under `[project.optional-dependencies]` in `pyproject.toml`.

A dependency change that prevents installation on a supported platform or
Python version is a breaking change and follows the rules above.

## Changing these rules

Changes to this file need a maintainer's approval. If you move or rename it,
update the pointer under the title of every AGENTS.md and the links in
`CONTRIBUTING.md` and `docs/source/devguide.rst`.
