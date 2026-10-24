"""Exercise copied templates in disposable projects and local bare remotes."""

import ast
import importlib.util
import json
import os
from pathlib import Path
import pty
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
CONSTANTS = "acmeapp/constants/DAcmeApp.py"
spec = importlib.util.spec_from_file_location("cmdb_checker", TEMPLATES / "project/scripts/check-cmdb.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def configure(text):
    return (text.replace("__PROJECT_NAME__", "AcmeApp")
            .replace("__PROJECT_SLUG__", "acmeapp")
            .replace("__PROJECT_SUBTYPE__", "Inventory"))


class MetadataTests(unittest.TestCase):
    def setUp(self):
        self.source = configure((TEMPLATES / "project/constants/DProject.py").read_text())

    def test_literals_are_read_without_executing_project_code(self):
        values = checker.validate('raise RuntimeError("never run")\n' + self.source,
                                  "AcmeApp", CONSTANTS)
        self.assertEqual(values['CMDB_TYPE'], 'application')
        self.assertEqual(values['BASE_DIR'], '/opt/prod/acmeapp')

    def test_type_name_path_and_metadata_contract(self):
        cases = [
            (self.source.replace('"application"', '"   "'), 'CMDB_TYPE'),
            (self.source.replace('"Inventory"', 'get_subtype()'), 'CMDB_SUBTYPE'),
            (self.source.replace('"Inventory"', '"__PROJECT_SUBTYPE__"'), 'CMDB_SUBTYPE'),
            (self.source.replace('/opt/prod/acmeapp', '/opt/dev/acmeapp'), 'BASE_DIR'),
            (self.source + '\nVERSION = "1.0.0"\n', 'independent assignment'),
            (self.source.replace('CMDB_COMPONENTS = ()', 'CMDB_COMPONENTS = (("Bad", "../data"),)'), 'traversal'),
            (self.source.replace('CMDB_DATABASES = ()', 'CMDB_DATABASES = (("DB", "' + 'x' * 65 + '"),)'), '64'),
        ]
        for source, error in cases:
            with self.subTest(error=error):
                with self.assertRaisesRegex(ValueError, error):
                    checker.validate(source, 'AcmeApp', CONSTANTS)
        for name, path in [('Acme-App', CONSTANTS), ('AcmeApp', 'acmeapp/constants/DACMEAPP.py')]:
            with self.assertRaises(ValueError):
                checker.validate(self.source, name, path)

    def test_declared_data_and_release_text(self):
        source = self.source.replace('CMDB_COMPONENTS = ()', 'CMDB_COMPONENTS = (("Uploads", "/srv/acme/uploads"),)')
        source = source.replace('CMDB_DATABASES = ()', 'CMDB_DATABASES = (("Main", "AcmeDb"),)')
        checker.validate(source, 'AcmeApp', CONSTANTS, 'Beacon "two"', '1.0.0-rc.1+build.01')
        for message in ('a\nb', 'x' * 256, '\x7f', '   '):
            with self.assertRaises(ValueError):
                checker.validate(source, 'AcmeApp', CONSTANTS, message)

    def test_classification_vocabulary_is_not_restricted(self):
        for classification in ('application', 'Application', 'DBMS', 'Custom Software'):
            with self.subTest(classification=classification):
                source = self.source.replace('"application"', repr(classification))
                values = checker.validate(source, 'AcmeApp', CONSTANTS)
                self.assertEqual(values['CMDB_TYPE'], classification)

    def test_network_literals_and_legacy_omission(self):
        declaration = 'CMDB_NETWORK: Final[tuple[tuple[str, str, int], ...]] = ()'
        source = self.source.replace(declaration, '')
        checker.validate(source, 'AcmeApp', CONSTANTS)
        source = self.source.replace(declaration, 'CMDB_NETWORK = (("http", "0.0.0.0", 18080), ("backend", "127.0.0.1", 18081))')
        checker.validate('raise RuntimeError("never run")\n' + source, 'AcmeApp', CONSTANTS)
        # Confirm both the release template and installed project's checker agree.
        self.assertEqual((ROOT / 'scripts/check-cmdb.py').read_bytes(),
                         (TEMPLATES / 'project/scripts/check-cmdb.py').read_bytes())

    def test_invalid_network_declarations_are_rejected(self):
        declaration = 'CMDB_NETWORK: Final[tuple[tuple[str, str, int], ...]] = ()'
        cases = (
            ('get_network()', None),
            ('"http"', 'literal tuple or list'),
            ('(("http", "127.0.0.1"),)', 'listener|entries'),
            ('(("", "127.0.0.1", 80),)', 'use'),
            ('((" http ", "127.0.0.1", 80),)', 'use'),
            ('(("http", "127.0.0.1", 80), ("http", "0.0.0.0", 81))', 'duplicate'),
            ('(("http", "localhost", 80),)', 'IPv4'),
            ('(("http", "::1", 80),)', 'IPv4'),
            ('(("http", 123, 80),)', 'IPv4'),
            ('(("http", "127.0.0.1", True),)', 'port'),
            ('(("http", "127.0.0.1", "80"),)', 'port'),
            ('(("http", "127.0.0.1", 0),)', 'port'),
            ('(("http", "127.0.0.1", 65536),)', 'port'),
        )
        for value, error in cases:
            with self.subTest(value=value):
                source = self.source.replace(declaration, 'CMDB_NETWORK = ' + value)
                with self.assertRaisesRegex(ValueError, error or 'malformed'):
                    checker.validate(source, 'AcmeApp', CONSTANTS)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory(prefix='bmforge-release-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_TERMINAL_PROMPT='0', GIT_AUTHOR_NAME='Release Test',
                        GIT_AUTHOR_EMAIL='test@example.invalid', GIT_COMMITTER_NAME='Release Test',
                        GIT_COMMITTER_EMAIL='test@example.invalid', PYTHONDONTWRITEBYTECODE='1',
                        NO_COLOR='1', TERM='dumb')
        self.git('init', '-b', 'main')
        self.git('init', '--bare', str(self.root / 'remote.git'))
        self.git('remote', 'add', 'origin', str(self.root / 'remote.git'))
        for name in ['scripts/new-release.sh', 'scripts/check-cmdb.py', 'scripts/install.sh',
                     'scripts/upgrade.sh', 'scripts/uninstall.sh', 'scripts/install.py', 'CHANGELOG.md']:
            self.write(name, configure((TEMPLATES / 'project' / name).read_text()))
            if name.endswith('.sh'):
                (self.repo / name).chmod(0o755)
        self.write(CONSTANTS, configure((TEMPLATES / 'project/constants/DProject.py').read_text()).replace(
            'class DProject:', 'class DAcmeApp:').replace('"0.0.0"', '"0.0.1"'))
        self.git('add', '.')
        self.git('commit', '-m', 'Initial project')
        self.git('branch', 'dev')
        self.git('push', 'origin', 'main', 'dev')
        self.git('switch', '-c', 'feat/maint-0.1.0')
        self.write('CHANGELOG.md', '# Changelog\n\n## [Unreleased]\n\n### Added\n\n- First feature.\n')
        self.commit('Add feature')

    def write(self, name, text):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def command(self, *args, check=True):
        return subprocess.run(args, cwd=self.repo, env=self.env, text=True,
                              capture_output=True, check=check, timeout=30)

    def git(self, *args):
        return self.command('git', *args).stdout.strip()

    def commit(self, message):
        self.git('add', '.')
        self.git('commit', '-m', message)

    def release(self, *args, answer='y', terminal=True):
        command = ['bash', 'scripts/new-release.sh', *args]
        if not terminal:
            return self.command(*command, check=False)
        master, slave = pty.openpty()
        try:
            with subprocess.Popen(command, cwd=self.repo, env=self.env, stdin=slave,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
                os.close(slave)
                slave = None
                os.write(master, (answer + '\n').encode())
                try:
                    stdout, stderr = process.communicate(timeout=30)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate()
                    raise
                return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
        finally:
            os.close(master)
            if slave is not None:
                os.close(slave)

    def assert_rejected(self, args, error, **options):
        before = self.git('show-ref')
        branch = self.git('branch', '--show-current')
        constants = (self.repo / CONSTANTS).read_bytes()
        result = self.release(*args, **options)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(error, result.stderr, result.stdout)
        self.assertEqual(self.git('show-ref'), before)
        self.assertEqual(self.git('branch', '--show-current'), branch)
        self.assertEqual((self.repo / CONSTANTS).read_bytes(), constants)

    def test_release_publishes_metadata_and_matching_refs(self):
        source = (self.repo / CONSTANTS).read_text().replace('class DAcmeApp:', 'raise RuntimeError("never execute")\n\nclass DAcmeApp:')
        source = source.replace('"0.0.1"', '"0.0.1"  # preserved comment')
        self.write(CONSTANTS, source)
        self.commit('Keep annotated literal metadata')
        message = 'Beacon "quoted" and café'
        result = self.release('0.1.0', message)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(self.git('branch', '--show-current'), 'feat/maint-0.1.1')
        tip = self.git('rev-parse', 'HEAD')
        for ref in ('main', 'dev', 'origin/main', 'origin/dev', 'v0.1.0^{commit}'):
            self.assertEqual(self.git('rev-parse', ref), tip)
        self.assertEqual(self.git('cat-file', '-t', 'v0.1.0'), 'tag')
        constants = (self.repo / CONSTANTS).read_text()
        values = checker.validate(constants, 'AcmeApp', CONSTANTS)
        self.assertEqual(values['VERSION'], '0.1.0')
        self.assertEqual(values['CMDB_CODENAME'], message)
        self.assertIn('# preserved comment', constants)
        changelog = (self.repo / 'CHANGELOG.md').read_text()
        self.assertEqual(changelog.count('## [Unreleased]'), 1)
        self.assertIn('## [0.1.0] - ', changelog)
        self.assertIn('- First feature.', changelog)
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertNotIn('refs/heads/feat/maint-0.1.1', self.git('ls-remote', 'origin'))

    def test_optional_pyproject_version_advances_with_application_version(self):
        self.write('pyproject.toml', (
            '[build-system]\nrequires = ["setuptools"]\n'
            '[project]\nname = "acmeapp"\nversion = "0.0.1" # preserve\n'
            '[project.scripts]\nacmeapp = "acmeapp.cli:main"\n'
        ))
        self.commit('Declare packaged application version')
        result = self.release('0.1.0', 'Package version sync')
        self.assertEqual(result.returncode, 0, result.stderr)
        contents = (self.repo / 'pyproject.toml').read_text()
        self.assertIn('version = "0.1.0" # preserve', contents)
        self.assertIn('acmeapp = "acmeapp.cli:main"', contents)
        self.assertEqual(self.git('show', 'main:pyproject.toml'), contents)
        self.assertEqual(self.git('show', 'v0.1.0:pyproject.toml'), contents)
        self.assertIn('VERSION: Final[str] = "0.1.0"', (self.repo / CONSTANTS).read_text())

    def test_pyproject_version_drift_blocks_release_before_merges(self):
        self.write('pyproject.toml', '[project]\nname = "acmeapp"\nversion = "2.3.4"\n')
        self.commit('Add inconsistent package metadata')
        self.assert_rejected(('0.1.0', 'Release'), 'Package version')
        self.assertEqual(self.git('show', 'HEAD:pyproject.toml'),
                         (self.repo / 'pyproject.toml').read_text())

    def test_dynamic_pyproject_version_is_not_silently_ignored(self):
        self.write('pyproject.toml', '[project]\nname = "acmeapp"\ndynamic = ["version"]\n')
        self.commit('Use unsupported dynamic version')
        self.assert_rejected(('0.1.0', 'Release'), 'must define exactly one literal version')

    def test_tool_only_pyproject_does_not_add_package_metadata(self):
        self.write('pyproject.toml', '[tool.ruff]\nline-length = 100\n')
        self.commit('Configure an unrelated build tool')
        result = self.release('0.1.0', 'Tool-only metadata')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.repo / 'pyproject.toml').read_text(),
                         '[tool.ruff]\nline-length = 100\n')

    def test_prerelease_and_explicit_next_branch(self):
        result = self.release('0.1.0-rc.1+build.01', '-Candidate', 'feat/next')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git('branch', '--show-current'), 'feat/next')

    def test_invalid_versions_messages_and_next_branch_are_rejected(self):
        for version in ('v0.1.0', '01.2.3', '0.1.0-01', '0.1.0-rc.01', '0.1.0/evil'):
            self.assert_rejected((version, 'Release'), 'Use a version')
        self.assert_rejected(('0.1.0', '   '), 'message is required')
        self.assert_rejected(('0.1.0', 'a\nb'), 'Release codename')
        self.assert_rejected(('0.1.0', 'x' * 256), 'Release codename')
        self.assert_rejected(('0.1.0', 'Release', 'dev'), 'already exists')

    def test_dirty_tree_main_and_invalid_cmdb_type_are_rejected(self):
        self.write('pending.txt', 'Pending')
        self.assert_rejected(('0.1.0', 'Release'), 'Commit or stash')
        (self.repo / 'pending.txt').unlink()
        self.git('switch', 'main')
        self.assert_rejected(('0.1.0', 'Release'), 'Run from a feature branch')
        self.git('switch', 'feat/maint-0.1.0')
        self.write(CONSTANTS, (self.repo / CONSTANTS).read_text().replace('"application"', '""'))
        self.commit('Invalid metadata')
        self.assert_rejected(('0.1.0', 'Release'), 'CMDB_TYPE')

    def test_cancellation_and_noninteractive_invocation_do_not_release(self):
        before = self.git('show-ref')
        result = self.release('0.1.0', 'Release', answer='n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('cancelled', result.stdout)
        self.assertEqual(self.git('show-ref'), before)
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assert_rejected(('0.1.0', 'Release'), 'interactive terminal', terminal=False)

    def test_tag_collision_and_branch_ancestry_are_rejected(self):
        self.git('tag', 'v0.1.0')
        self.assert_rejected(('0.1.0', 'Release'), 'Tag v0.1.0 already exists')
        self.git('tag', '-d', 'v0.1.0')
        self.git('switch', 'main')
        self.write('main-change.txt', 'Change on main')
        self.commit('Advance main')
        self.git('switch', 'feat/maint-0.1.0')
        self.assert_rejected(('0.1.0', 'Release'), 'Merge main into dev')

    def test_missing_or_nonexecutable_lifecycle_script_is_rejected(self):
        path = self.repo / 'scripts/upgrade.sh'
        path.chmod(0o644)
        self.commit('Remove upgrade executable permission')
        self.assert_rejected(('0.1.0', 'Release'), 'Missing executable scripts/upgrade.sh')

    def test_rejected_atomic_push_preserves_remote_refs(self):
        before = self.git('ls-remote', 'origin')
        hook = self.root / 'remote.git/hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        result = self.release('0.1.0', 'Rejected remotely')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git('ls-remote', 'origin'), before)
        self.assertEqual(self.git('cat-file', '-t', 'v0.1.0'), 'tag')

    def enable_deployment(self):
        shutil.copytree(TEMPLATES / 'deployment_tools', self.repo / 'deployment_tools',
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for path in (TEMPLATES / 'project/deployment').iterdir():
            self.write('deployment/' + path.name, configure(path.read_text()))
        self.write('acmeapp/__init__.py', '')
        self.write('acmeapp/constants/__init__.py', '')
        self.write('acmeapp/__main__.py', 'from acmeapp.constants.DAcmeApp import DAcmeApp\n')
        script = (self.repo / 'scripts/new-release.sh').read_text()
        script = script.replace('readonly dependency_rules=""', 'readonly dependency_rules="deployment/rules.json"')
        script = script.replace('readonly deployment_config=""', 'readonly deployment_config="deployment.config"')
        self.write('scripts/new-release.sh', script)
        self.tools('--rules', 'deployment/rules.json')
        self.history('initialize', '0.0.1')
        self.commit('Configure deployment baseline')

    def tools(self, *args, check=True):
        return self.command(sys.executable, '-B', '-m', 'deployment_tools', *args, check=check)

    def history(self, *args, check=True):
        return self.command(sys.executable, '-B', '-m', 'deployment_tools.release', '--config', 'deployment.config', *args, check=check)

    def test_release_with_optional_deployment_and_skipped_release_planning(self):
        self.enable_deployment()
        self.write('acmeapp/__main__.py', 'from acmeapp.constants.DAcmeApp import DAcmeApp\n# first change\n')
        self.commit('Change application')
        result = self.release('0.1.0', 'Beacon')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        history = json.loads((self.repo / 'deployment/releases.json').read_text())
        self.assertEqual(history['releases'][-1], {'version': '0.1.0', 'targets': ['application', 'filesystem']})
        self.assertEqual(self.history('upgrade', '0.0.1', '0.1.0').stdout.splitlines(), ['application', 'filesystem'])
        config = self.repo / 'deployment/config.py'
        config.write_text(config.read_text() + '\n# setup changed\n')
        self.commit('Change setup')
        result = self.release('0.1.1', 'Second')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        targets = self.history('upgrade', '0.0.1', '0.1.1').stdout.splitlines()
        self.assertEqual(targets, ['application', 'filesystem'])
        self.assertNotEqual(self.history('upgrade', '0.0.0', '0.1.1', check=False).returncode, 0)

    def test_stale_map_and_existing_history_are_rejected(self):
        self.enable_deployment()
        before = (self.repo / 'deployment/releases.json').read_bytes()
        result = self.history('initialize', '0.0.1', check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.repo / 'deployment/releases.json').read_bytes(), before)
        self.write('acmeapp/unused.py', 'VALUE = 1\n')
        self.commit('Unowned artifact')
        self.assert_rejected(('0.1.0', 'Release'), 'unreachable')


if __name__ == '__main__':
    unittest.main()
