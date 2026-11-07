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

- When you rename something, prefer the name used by the matching IDL SPEDAS
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

## Changing these rules

Changes to this file need a maintainer's approval. If you move or rename it,
update the pointer under the title of every AGENTS.md and the links in
`CONTRIBUTING.md` and `docs/source/devguide.rst`.
