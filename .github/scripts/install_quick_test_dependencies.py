#!/usr/bin/env python3
"""Install quick-test dependencies without changing project dependency declarations.

locked: locked development groups, followed by normal pip runtime resolution.
latest: highest compatible stable versions, with a seven-day upload cutoff.
oldest: lowest direct runtime versions for the selected Python; newer transitive
        dependencies and test tools, also subject to the seven-day cutoff.
"""

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import shlex
import subprocess


def install(policy, root, python, tools_python, output_dir, runner=subprocess.run):
    """Resolve, build and install, keeping resolver tools outside the test venv."""
    if policy not in ('locked', 'latest', 'oldest'):
        raise ValueError(f'Unknown dependency policy: {policy}')
    root = Path(root).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    # Do not inherit a cutoff into the normal end-user installation policy.
    for key in ('PIP_UPLOADED_PRIOR_TO', 'UV_EXCLUDE_NEWER'):
        env.pop(key, None)
    cutoff = None
    if policy != 'locked':
        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
        env['PIP_UPLOADED_PRIOR_TO'] = cutoff
        env['UV_EXCLUDE_NEWER'] = cutoff
        env['PIP_ONLY_FINAL'] = ':all:'
    (output_dir / 'policy.json').write_text(json.dumps({
        'policy': policy, 'python': str(python), 'upload_cutoff_utc': cutoff,
        'oldest_resolution': 'lowest-direct' if policy == 'oldest' else None,
    }, indent=2) + '\n')

    def run(*args):
        command = [str(arg) for arg in args]
        print('+ ' + shlex.join(command), flush=True)
        runner(command, cwd=root, env=env, check=True)

    def pip(*args):
        run(python, '-m', 'pip', *args)

    groups = ('--group', 'lint', '--group', 'test', '--group', 'setup')
    runtime = output_dir / 'oldest-runtime.txt'
    if policy == 'locked':
        # Only development groups come from pdm.lock. Runtime dependencies below
        # intentionally follow pip's normal already-satisfied/only-if-needed rules.
        env['PDM_USE_UV'] = 'false'
        run(tools_python, '-m', 'pdm', 'use', '--first', python)
        run(tools_python, '-m', 'pdm', 'sync', '-dG', 'lint', '-dG', 'test',
            '-dG', 'setup', '--no-default', '--no-self')
        pip('install', 'coverage')
    elif policy == 'latest':
        pip('install', '--upgrade', '--upgrade-strategy', 'eager', '--group', 'setup')
    else:
        # Compile only runtime dependencies (including the existing mth5 extra).
        # Applying lowest-direct to test/build tools would test their lower bounds
        # instead of the advertised PySPEDAS runtime lower bounds.
        run(tools_python, '-m', 'uv', '--no-config', 'pip', 'compile',
            'pyproject.toml', '--extra', 'mth5', '--python', python,
            '--resolution', 'lowest-direct', '--prerelease', 'disallow',
            '--upgrade', '--output-file', runtime)
        pip('install', '-r', runtime, *groups, 'coverage',
            '--report', output_dir / 'development-install.json')

    # Build with policy-selected setup tools, without fetching unrelated tools in
    # a separate build environment. pip's dependency builds inherit the cutoff.
    run(python, '-m', 'build', '--no-isolation')
    wheels = sorted((root / 'dist').glob('*.whl'))
    if len(wheels) != 1:
        raise RuntimeError(f'Expected one built wheel in dist/, found {len(wheels)}')
    wheel = str(wheels[0]) + '[mth5]'
    report = output_dir / 'runtime-install.json'
    if policy == 'latest':
        pip('install', '--upgrade', '--upgrade-strategy', 'eager', *groups,
            'coverage', wheel, '--report', report)
    elif policy == 'oldest':
        # Preserve the runtime pins when installing the wheel, even if a dev tool
        # could otherwise cause pip to prefer a different runtime dependency.
        pip('install', '--constraint', runtime, wheel, '--report', report)
    else:
        pip('install', wheel, '--report', report)
    pip('check')
    pip('show', 'pyspedas', 'xarray', 'cdflib', 'numpy')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', choices=('locked', 'latest', 'oldest'), required=True)
    parser.add_argument('--python', required=True)
    parser.add_argument('--tools-python', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    install(args.policy, Path(__file__).resolve().parents[2], args.python,
            args.tools_python, args.output_dir)


if __name__ == '__main__':
    main()
