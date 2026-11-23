---
name: deprecation-scan
description: Scan PySPEDAS for deprecated routines and parameters that don't follow the breaking-change rules in RULES.md - no deprecation warning, a warning logged below WARNING, a Python warning instead of a log warning, no test of the old usage, or package code still calling a deprecated routine. Use when asked to audit deprecations or check consistency with RULES.md, before a major release, or when reviewing a pull request that deprecates something.
---

# Deprecation scan

`RULES.md` (Breaking changes and deprecations) says what a deprecated construct
needs during its transition period: a `logging.warning` that contains
"deprecate", CI tests of the old usage that check the warning, a docstring that
marks it deprecated, and, if one is being maintained, an entry in the next major
version's migration guide. This skill finds code that falls short.

## Establish release status and scope

Standard deprecation requirements apply to stable APIs that have appeared in a
release published to production PyPI (`pypi.org`). New APIs present only on master
or development branches are experimental by default. Released APIs explicitly
marked experimental before their first production release are also exempt from
the standard transition period. Check published distributions and release
records for the actual routine, parameter, setting or behavior being assessed.
A change on master does not make a previously released stable contract
experimental, and a stable API cannot be reclassified to avoid deprecation.
Ask a maintainer if the status remains unclear after checking release evidence.

Experimental changes still require tests, documentation and release notes when
published, as described in RULES.md. A standard "Experimental API" notice says
"without the standard deprecation period"; the scanner's keyword matching can
mistake this notice for a deprecated API. Confirm the affected construct's scope
and release status before treating a flag as a policy violation. The script
does not establish release history or experimental eligibility automatically.

## Run the scan

From the repository root:

    python .github/scripts/scan_deprecations.py          # readable report
    python .github/scripts/scan_deprecations.py --json   # the same, for tools

It reads the source with `ast`, never imports pyspedas and downloads nothing.
It lists every routine in `pyspedas/` (test folders excluded) whose docstring
mentions "deprecat" or whose code emits a deprecation message, then flags:

- `no-warning`: the docstring marks something deprecated, but nothing warns.
- `low-level`: the deprecation message is logged below WARNING, for example
  with `logging.info`, so users don't see it at the default level.
- `python-warning-only`: `warnings.warn()` is used and nothing is logged at
  WARNING.
- `no-test`: no test function names the routine, mentions "deprecat" in code
  and checks a log or warning (`assertLogs`, `assertWarns`,
  `warnings.catch_warnings`).
- `internal-caller`: package code outside the routine's own file still calls
  a routine whose docstring's first line says it is deprecated.

The report also names any `docs/source/*migration*.rst` page that mentions the
routine. A mention is only a lead: the page may name it for another reason.

## Check every finding by hand

The matching is heuristic. Before you report a finding, open the routine and
the tests the scan names:

- A docstring line that says "deprecated" may refer to one parameter or to
  the whole routine. Name the actual construct (parameter or routine) and its
  replacement in your report.
- A matching test may check a different warning, or only check that no
  warning is raised. Confirm that it calls the old construct and checks the
  deprecation message.
- A test that only calls the old construct, or mentions it in a comment, does
  not count; the scan already ignores comments.
- Some deprecated routines no longer work at all (for example, one that only
  logs an error and returns). Report these as already removed, not as in
  transition.
- A routine can warn through a helper the scan doesn't follow. Read the code
  before reporting `no-warning`.

## Report

Give the human a table of the confirmed findings: the construct, what it lacks
under `RULES.md`, the replacement, and `file:line`. Don't change code as part of
the scan; fixes go in separate pull requests. If the human asks for an issue,
list each construct with its missing items so each can be checked off.
