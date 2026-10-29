"""Regression tests for quick_tests dependency-policy isolation and failures."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'install_quick_test_dependencies.py'
spec = importlib.util.spec_from_file_location('quick_test_dependencies', SCRIPT)
policy_installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy_installer)


class DependencyPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / 'dist').mkdir()
        (self.root / 'dist' / 'pyspedas-1.0-py3-none-any.whl').touch()
        self.lock = self.root / 'pdm.lock'
        self.lock.write_text('sentinel: never rewrite the project lockfile\n')
        self.calls = []

    def record(self, args, **kwargs):
        self.calls.append((args, dict(kwargs['env'])))

    def install(self, policy, runner=None):
        policy_installer.install(policy, self.root, '/test/bin/python',
                                 '/tools/bin/python', self.root / 'diagnostics',
                                 runner=runner or self.record)
        self.assertEqual(self.lock.read_text(), 'sentinel: never rewrite the project lockfile\n')

    def test_default_keeps_runtime_pip_resolution_unconstrained(self):
        with patch.dict(os.environ, {'PIP_UPLOADED_PRIOR_TO': '2000-01-01',
                                     'UV_EXCLUDE_NEWER': '2000-01-01'}):
            self.install('default')
        runtime, env = next((a, e) for a, e in self.calls
                            if 'install' in a and any(v.endswith('.whl[mth5]') for v in a))
        self.assertNotIn('--constraint', runtime)
        self.assertNotIn('--upgrade', runtime)
        self.assertNotIn('PIP_UPLOADED_PRIOR_TO', env)
        self.assertNotIn('UV_EXCLUDE_NEWER', env)
        self.assertTrue(any('sync' in a and '--no-default' in a for a, _ in self.calls))

    def test_latest_cutoff_is_shared_by_build_and_install(self):
        self.install('latest')
        cutoffs = {e['PIP_UPLOADED_PRIOR_TO'] for _, e in self.calls}
        self.assertEqual(len(cutoffs), 1)
        self.assertFalse(any('pdm' in a for a, _ in self.calls))
        runtime = next(a for a, _ in self.calls if any(v.endswith('.whl[mth5]') for v in a))
        self.assertIn('eager', runtime)

    def test_oldest_runtime_pins_survive_development_and_wheel_installs(self):
        self.install('oldest')
        compile_args = next(a for a, _ in self.calls if 'compile' in a)
        self.assertIn('lowest-direct', compile_args)
        self.assertNotIn('--group', compile_args)
        self.assertFalse(any('pdm' in a for a, _ in self.calls))
        runtime = self.root / 'diagnostics' / 'oldest-runtime.txt'
        self.assertTrue(any('-r' in a and str(runtime) in a for a, _ in self.calls))
        final = next(a for a, _ in self.calls if any(v.endswith('.whl[mth5]') for v in a))
        self.assertEqual(final[final.index('--constraint') + 1], str(runtime))

    def test_resolution_failure_stops_before_build_or_install(self):
        def fail(args, **kwargs):
            self.record(args, **kwargs)
            raise subprocess.CalledProcessError(1, args)
        with self.assertRaises(subprocess.CalledProcessError):
            self.install('oldest', fail)
        self.assertEqual(len(self.calls), 1)
        self.assertNotIn('build', self.calls[0][0])
        metadata = json.loads((self.root / 'diagnostics' / 'policy.json').read_text())
        self.assertEqual(metadata['policy'], 'oldest')

    def test_invalid_policy_never_runs_commands(self):
        with self.assertRaises(ValueError):
            self.install('arbitrary')
        self.assertFalse(self.calls)


if __name__ == '__main__':
    unittest.main()
