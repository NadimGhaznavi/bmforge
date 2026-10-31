"""Test lifecycle operations in isolated source and installation directories."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load('bmforge_installation', ROOT / 'scripts/install.py')
starter = load('starter_installation', ROOT / 'templates/project/scripts/install.py')


class InstallationTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory(prefix='bmforge-install-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.checkout = self.root / 'checkout'
        self.destination = self.root / 'installed'
        self.checkout.mkdir()
        for name in installer.COPY_TREES:
            shutil.copytree(ROOT / name, self.checkout / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for name in installer.COPY_FILES:
            shutil.copy2(ROOT / name, self.checkout / name)
        self.constants = self.checkout / 'bmforge/constants/DBMForge.py'
        self.version = self.operation().metadata['VERSION']

    def operation(self):
        return installer.Installation(self.checkout, destination=self.destination)

    def marker(self):
        return (self.destination / installer.VERSION_MARKER).read_text().strip()

    def change_version(self):
        text = self.constants.read_text().replace(f'VERSION: Final[str] = "{self.version}"',
                                                  'VERSION: Final[str] = "9.9.9"')
        self.constants.write_text(text)

    def test_checks_do_not_create_installation(self):
        self.operation().apply('install', check=True)
        self.assertFalse(self.destination.exists())
        self.operation().apply('uninstall', check=True)
        self.assertFalse(self.destination.exists())

    def test_install_and_reinstall_publish_readable_cmdb_metadata(self):
        self.operation().apply('install')
        self.operation().apply('install')
        constants = self.destination / 'bmforge/constants/DBMForge.py'
        self.assertEqual(constants.read_bytes(), self.constants.read_bytes())
        self.assertEqual(constants.stat().st_mode & 0o777, 0o644)
        self.assertEqual(constants.parent.stat().st_mode & 0o777, 0o755)
        self.assertEqual(self.marker(), self.version)
        self.assertTrue(os.access(self.destination / 'scripts/install.sh', os.X_OK))
        self.assertFalse((self.destination / '.git').exists())
        self.assertFalse((self.destination / 'tests').exists())

    def test_upgrade_removes_obsolete_managed_files_and_preserves_data(self):
        old = self.checkout / 'pages/obsolete.md'
        old.write_text('Old managed documentation')
        self.operation().apply('install')
        saved = self.destination / 'conf/local-settings.json'
        saved.parent.mkdir()
        saved.write_text('Keep this')
        old.unlink()
        self.change_version()
        self.operation().apply('upgrade')
        self.assertEqual(self.marker(), '9.9.9')
        self.assertFalse((self.destination / 'pages/obsolete.md').exists())
        self.assertEqual(saved.read_text(), 'Keep this')

    def test_uninstall_preserves_unowned_files_and_allows_repeat(self):
        self.operation().apply('install')
        saved = self.destination / 'saved.txt'
        saved.write_text('Keep this')
        self.operation().apply('uninstall')
        self.assertEqual(saved.read_text(), 'Keep this')
        self.assertFalse((self.destination / 'bmforge/constants/DBMForge.py').exists())
        manifest = json.loads((self.destination / installer.MANIFEST).read_text())
        self.assertTrue(manifest['removed'])
        self.assertEqual(manifest['files'], [])
        self.operation().apply('uninstall')
        with self.assertRaisesRegex(ValueError, 'run install.sh first'):
            self.operation().apply('upgrade')
        self.operation().apply('install')
        self.assertEqual(saved.read_text(), 'Keep this')
        self.assertEqual(self.marker(), self.version)

    def test_complete_removal_is_repeatable(self):
        self.operation().apply('install')
        self.operation().apply('uninstall')
        self.operation().apply('uninstall')
        self.assertFalse(self.destination.exists())

    def test_upgrade_without_install_and_foreign_directory_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'run install.sh first'):
            self.operation().apply('upgrade')
        self.destination.mkdir()
        saved = self.destination / 'foreign.txt'
        saved.write_text('Keep this')
        with self.assertRaisesRegex(ValueError, 'without an ownership manifest'):
            self.operation().apply('install')
        self.assertEqual(saved.read_text(), 'Keep this')

    def test_new_managed_file_cannot_overwrite_unowned_content(self):
        self.operation().apply('install')
        target = self.destination / 'pages/local.md'
        target.write_text('Keep this')
        (self.checkout / 'pages/local.md').write_text('New source')
        with self.assertRaisesRegex(ValueError, 'unowned file'):
            self.operation().apply('upgrade')
        self.assertEqual(target.read_text(), 'Keep this')
        self.assertEqual(self.marker(), self.version)

    def test_source_and_destination_symlinks_are_rejected(self):
        outside = self.root / 'outside.txt'
        outside.write_text('Keep this')
        source = self.checkout / 'pages/unsafe.md'
        source.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symbolic link'):
            self.operation().apply('install')
        self.assertFalse(self.destination.exists())
        source.unlink()
        self.operation().apply('install')
        managed = self.destination / 'README.md'
        managed.unlink()
        managed.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symbolic link'):
            self.operation().apply('uninstall')
        self.assertEqual(outside.read_text(), 'Keep this')

    def test_self_deployment_and_forged_parent_paths_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'separate checkout'):
            installer.Installation(self.checkout, destination=self.checkout / 'installed')
        self.operation().apply('install')
        manifest = self.destination / installer.MANIFEST
        data = json.loads(manifest.read_text())
        data['files'].append('../outside.txt')
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'Invalid managed path'):
            self.operation().apply('uninstall')

    def test_copy_failure_preserves_success_marker_and_can_be_retried(self):
        self.operation().apply('install')
        self.change_version()
        operation = self.operation()
        original = operation.atomic_write

        def interrupted(path, content, mode=0o644):
            if path == self.destination / 'README.md':
                raise OSError('Simulated copy failure')
            return original(path, content, mode)

        with patch.object(operation, 'atomic_write', side_effect=interrupted):
            with self.assertRaisesRegex(OSError, 'Simulated copy failure'):
                operation.apply('upgrade')
        self.assertEqual(self.marker(), self.version)
        constants = (self.destination / 'bmforge/constants/DBMForge.py').read_text()
        self.assertIn(f'VERSION: Final[str] = "{self.version}"', constants)
        self.operation().apply('upgrade')
        self.assertEqual(self.marker(), '9.9.9')

    def test_starter_stops_before_modifying_the_host(self):
        with patch.object(starter, 'PROJECT_NAME', 'BMForge'):
            operation = starter.Installation(self.checkout, destination=self.destination)
            with self.assertRaisesRegex(ValueError, 'Deployment is not configured'):
                operation.apply('install')
        self.assertFalse(self.destination.exists())

    def test_minimal_library_install_always_records_version_and_identity(self):
        """Reuse the existing file installer for a small metadata-only footprint."""
        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)):
            source = 'bmforge/constants/DBMForge.py'
            operation = starter.Installation(self.checkout, destination=self.destination)
            operation.apply('install', check=True)
            self.assertFalse(self.destination.exists())
            operation.apply('install')
            self.assertEqual((self.destination / starter.VERSION_MARKER).read_text().strip(), self.version)
            self.assertEqual((self.destination / source).read_bytes(), self.constants.read_bytes())
            manifest = json.loads((self.destination / starter.MANIFEST).read_text())
            self.assertEqual(manifest['files'], [source])
            self.assertFalse((self.destination / 'scripts').exists())
            self.assertFalse((self.destination / 'systemd').exists())
            retained = self.destination / 'conf/preferences.json'
            retained.parent.mkdir(parents=True)
            retained.write_text('{"locale":"fr"}')
            self.change_version()
            operation = starter.Installation(self.checkout, destination=self.destination)
            operation.apply('upgrade')
            self.assertEqual((self.destination / starter.VERSION_MARKER).read_text().strip(), '9.9.9')
            self.assertEqual(retained.read_text(), '{"locale":"fr"}')
            operation.apply('uninstall')
            self.assertFalse((self.destination / starter.VERSION_MARKER).exists())
            self.assertFalse((self.destination / source).exists())
            self.assertEqual(retained.read_text(), '{"locale":"fr"}')
            manifest = json.loads((self.destination / starter.MANIFEST).read_text())
            self.assertTrue(manifest['removed'])
            self.assertEqual(manifest['files'], [])


    def test_starter_production_venv_is_optional_and_managed(self):
        requirements = self.checkout / 'requirements.txt'
        requirements.write_text('example-package==1.0\n')
        calls = []
        python = self.destination / '.venv/bin/python'

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            if command[:3] == [starter.SYSTEM_PYTHON, '-m', 'venv']:
                python.parent.mkdir(parents=True)
                python.write_text('fake interpreter')
                (self.destination / '.venv/pyvenv.cfg').write_text('home = /usr/bin\n')
            return subprocess.CompletedProcess(command, 0)

        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)), \
             patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'), \
             patch.object(starter, 'RUNTIME_IMPORTS', ('bmforge', 'example_package')), \
             patch.object(starter.subprocess, 'run', side_effect=fake_run), \
             patch.dict(os.environ, {'PYTHONPATH': '/opt/dev/unwanted',
                                     'PYTHONHOME': '/opt/dev/unwanted',
                                     'VIRTUAL_ENV': '/opt/dev/unwanted'}):
            operation = starter.Installation(self.checkout, destination=self.destination)
            operation.apply('install', check=True)
            self.assertFalse(self.destination.exists())
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][0][1:], ['-B', '-c', 'import venv, ensurepip'])
            self.assertNotIn('PYTHONPATH', calls[0][1]['env'])
            self.assertNotIn('PYTHONHOME', calls[0][1]['env'])

            operation.apply('install')
            self.assertEqual([command[1:3] for command, _ in calls].count(['-m', 'venv']), 1)
            installs = [command for command, _ in calls if command[1:4] == ['-m', 'pip', 'install']]
            self.assertEqual(len(installs), 1)
            self.assertEqual(installs[0][-2:], ['-r', str(self.destination / 'requirements.txt')])
            self.assertIn('--upgrade', installs[0])
            self.assertEqual((self.destination / starter.VERSION_MARKER).read_text().strip(), self.version)
            manifest = json.loads((self.destination / starter.MANIFEST).read_text())
            self.assertTrue(manifest['venv_owned'])
            self.assertIn('requirements.txt', manifest['files'])
            self.assertTrue(any(command[1:4] == ['-m', 'pip', 'check'] for command, _ in calls))
            self.assertTrue(any(command[-2:] == ['bmforge', 'example_package'] for command, _ in calls))

            calls.clear()
            operation.apply('upgrade', check=True)
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0][0][1:], ['-B', '-c', 'import venv, ensurepip'])
            operation.apply('upgrade')
            self.assertFalse(any(command[1:3] == ['-m', 'venv'] for command, _ in calls))
            self.assertEqual(sum(command[1:4] == ['-m', 'pip', 'install'] for command, _ in calls), 1)
            operation.apply('uninstall')
            self.assertFalse((self.destination / '.venv').exists())

    def test_failed_dependency_install_keeps_marker_and_owned_environment(self):
        (self.checkout / 'requirements.txt').write_text('example-package==1.0\n')
        def fake_run(command, **kwargs):
            if command[1:3] == ['-m', 'venv']:
                venv = self.destination / '.venv'
                (venv / 'bin').mkdir(parents=True)
                (venv / 'bin/python').write_text('fake')
                (venv / 'pyvenv.cfg').write_text('home = /usr/bin\n')
            if command[1:4] == ['-m', 'pip', 'install']:
                raise subprocess.CalledProcessError(1, command)
            return subprocess.CompletedProcess(command, 0)

        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)), \
             patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'), \
             patch.object(starter.subprocess, 'run', side_effect=fake_run):
            operation = starter.Installation(self.checkout, destination=self.destination)
            with self.assertRaises(subprocess.CalledProcessError):
                operation.apply('install')
            self.assertFalse((self.destination / starter.VERSION_MARKER).exists())
            self.assertTrue(json.loads((self.destination / starter.MANIFEST).read_text())['venv_owned'])
            self.assertTrue((self.destination / '.venv').exists())
            operation.apply('uninstall')
            self.assertFalse((self.destination / '.venv').exists())

    def test_upgrade_dependency_failure_preserves_last_successful_version(self):
        (self.checkout / 'requirements.txt').write_text('example-package==1.0\n')
        calls = []
        fail_pip = False

        def fake_run(command, **kwargs):
            calls.append(command)
            if command[1:3] == ['-m', 'venv']:
                venv = self.destination / '.venv'
                (venv / 'bin').mkdir(parents=True)
                (venv / 'bin/python').write_text('fake')
                (venv / 'pyvenv.cfg').write_text('home = /usr/bin\n')
            if fail_pip and command[1:4] == ['-m', 'pip', 'install']:
                raise subprocess.CalledProcessError(1, command)
            return subprocess.CompletedProcess(command, 0)

        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)), \
             patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'), \
             patch.object(starter.subprocess, 'run', side_effect=fake_run):
            operation = starter.Installation(self.checkout, destination=self.destination)
            operation.apply('install')
            original_version = (self.destination / starter.VERSION_MARKER).read_text()
            self.change_version()
            fail_pip = True
            with self.assertRaises(subprocess.CalledProcessError):
                starter.Installation(self.checkout, destination=self.destination).apply('upgrade')
            self.assertEqual((self.destination / starter.VERSION_MARKER).read_text(), original_version)
            self.assertTrue((self.destination / '.venv').exists())
            fail_pip = False
            starter.Installation(self.checkout, destination=self.destination).apply('upgrade')
            self.assertEqual((self.destination / starter.VERSION_MARKER).read_text().strip(), '9.9.9')
            self.assertEqual(sum(command[1:3] == ['-m', 'venv'] for command in calls), 1)

    def test_missing_venv_support_fails_check_before_changes(self):
        (self.checkout / 'requirements.txt').write_text('example-package==1.0\n')
        def no_venv(command, **kwargs):
            raise subprocess.CalledProcessError(1, command)
        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)), \
             patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'), \
             patch.object(starter.subprocess, 'run', side_effect=no_venv):
            operation = starter.Installation(self.checkout, destination=self.destination)
            for check in (True, False):
                with self.assertRaises(subprocess.CalledProcessError):
                    operation.apply('install', check=check)
                self.assertFalse(self.destination.exists())

    def test_unowned_venv_cannot_be_adopted_or_removed(self):
        (self.checkout / 'requirements.txt').write_text('example-package==1.0\n')
        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)):
            operation = starter.Installation(self.checkout, destination=self.destination)
            operation.apply('install')
            outside = self.destination / '.venv'
            outside.mkdir()
            (outside / 'important').write_text('unowned')
            with patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'):
                for check in (True, False):
                    with self.assertRaisesRegex(ValueError, 'unowned virtual environment'):
                        operation.apply('install', check=check)
            operation.apply('uninstall')
            self.assertEqual((outside / 'important').read_text(), 'unowned')

    def test_editable_or_checkout_requirements_are_rejected(self):
        requirements = self.checkout / 'requirements.txt'
        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)), \
             patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'):
            operation = starter.Installation(self.checkout, destination=self.destination)
            for entry in ('-e .', '--editable /tmp/project', 'pkg @ file:///opt/dev/app/wheel.whl'):
                requirements.write_text(entry + '\n')
                with self.subTest(entry=entry), self.assertRaisesRegex(ValueError, 'editable or /opt/dev'):
                    operation.apply('install', check=True)
                self.assertFalse(self.destination.exists())

    def test_real_venv_runs_with_source_checkout_unavailable(self):
        """Create a local dummy wheel; never contact a package index or production host."""
        requirements = self.checkout / 'requirements.txt'
        wheels = self.root / 'wheels'
        wheels.mkdir()
        version = '1.0.0'
        dist = f'forge_smoke-{version}.dist-info'
        contents = {
            'forge_smoke/__init__.py': 'VERSION = "1.0.0"\n',
            f'{dist}/METADATA': f'Metadata-Version: 2.1\nName: forge-smoke\nVersion: {version}\n',
            f'{dist}/WHEEL': 'Wheel-Version: 1.0\nGenerator: bmforge-tests\nRoot-Is-Purelib: true\nTag: py3-none-any\n',
        }
        with zipfile.ZipFile(wheels / f'forge_smoke-{version}-py3-none-any.whl', 'w') as archive:
            for name, content in contents.items():
                archive.writestr(name, content)
            archive.writestr(f'{dist}/RECORD',
                             ''.join(f'{name},,\n' for name in (*contents, f'{dist}/RECORD')))
        requirements.write_text('forge-smoke==1.0.0\n')
        with patch.dict(os.environ, {'PIP_FIND_LINKS': str(wheels), 'PIP_NO_INDEX': '1',
                                     'PYTHONPATH': str(self.checkout)}), \
             patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)), \
             patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'), \
             patch.object(starter, 'RUNTIME_IMPORTS', ('bmforge', 'forge_smoke')):
            operation = starter.Installation(self.checkout, destination=self.destination)
            operation.apply('install', check=True)
            operation.apply('install')
            # A pinned dependency upgrade must update the production environment.
            version = '2.0.0'
            dist = f'forge_smoke-{version}.dist-info'
            upgrade_contents = {
                'forge_smoke/__init__.py': 'VERSION = "2.0.0"\n',
                f'{dist}/METADATA': f'Metadata-Version: 2.1\nName: forge-smoke\nVersion: {version}\n',
                f'{dist}/WHEEL': 'Wheel-Version: 1.0\nGenerator: bmforge-tests\nRoot-Is-Purelib: true\nTag: py3-none-any\n',
            }
            with zipfile.ZipFile(wheels / f'forge_smoke-{version}-py3-none-any.whl', 'w') as archive:
                for name, content in upgrade_contents.items():
                    archive.writestr(name, content)
                archive.writestr(f'{dist}/RECORD',
                                 ''.join(f'{name},,\n' for name in (*upgrade_contents, f'{dist}/RECORD')))
            requirements.write_text('forge-smoke==2.0.0\n')
            operation.apply('upgrade')
            self.checkout.rename(self.root / 'checkout-gone')
            environment = starter.Installation.python_environment()
            python = self.destination / '.venv/bin/python'
            result = subprocess.run(
                [str(python), '-B', '-c',
                 'import bmforge, forge_smoke; print(forge_smoke.__file__); print(forge_smoke.VERSION)'],
                cwd=self.destination, env=environment, check=True, capture_output=True,
                text=True, timeout=30)
            installed_path, installed_version = result.stdout.strip().splitlines()
            self.assertTrue(Path(installed_path).is_relative_to(self.destination / '.venv'))
            self.assertEqual(installed_version, '2.0.0')
            operation.apply('uninstall')
            self.assertFalse((self.destination / '.venv').exists())

    def test_failed_runtime_import_keeps_success_marker_unpublished(self):
        (self.checkout / 'requirements.txt').write_text('example-package==1.0\n')
        def fake_run(command, **kwargs):
            if command[1:3] == ['-m', 'venv']:
                venv = self.destination / '.venv'
                (venv / 'bin').mkdir(parents=True)
                (venv / 'bin/python').write_text('fake')
                (venv / 'pyvenv.cfg').write_text('home = /usr/bin\n')
            if command[1:3] == ['-B', '-c'] and 'import_module(name)' in command[3]:
                raise subprocess.CalledProcessError(1, command)
            return subprocess.CompletedProcess(command, 0)
        with patch.object(starter, 'PROJECT_NAME', 'BMForge'), \
             patch.object(starter, 'DEPLOYMENT_READY', True), \
             patch.object(starter, 'COPY_TREES', ()), \
             patch.object(starter, 'COPY_FILES', ('bmforge/constants/DBMForge.py',)), \
             patch.object(starter, 'REQUIREMENTS_FILE', 'requirements.txt'), \
             patch.object(starter, 'RUNTIME_IMPORTS', ('bmforge', 'example_package')), \
             patch.object(starter.subprocess, 'run', side_effect=fake_run):
            operation = starter.Installation(self.checkout, destination=self.destination)
            with self.assertRaises(subprocess.CalledProcessError):
                operation.apply('install')
            self.assertFalse((self.destination / starter.VERSION_MARKER).exists())
            operation.apply('uninstall')
            self.assertFalse((self.destination / '.venv').exists())

    def test_starter_declares_installation_component_marker(self):
        self.assertEqual(starter.BMFORGE_COMPONENT,
                         {"id": "bmforge.installation", "spec_version": "0.1.3"})

    def test_entry_point_help_works_from_another_directory(self):
        for name in ['install.sh', 'upgrade.sh', 'uninstall.sh']:
            result = subprocess.run([str(self.checkout / 'scripts' / name), '--help'],
                                    cwd=self.root, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('--check', result.stdout)
        self.assertFalse(self.destination.exists())


if __name__ == '__main__':
    unittest.main()
