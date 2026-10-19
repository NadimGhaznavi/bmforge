"""Test lifecycle operations in isolated source and installation directories."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
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

    def test_entry_point_help_works_from_another_directory(self):
        for name in ['install.sh', 'upgrade.sh', 'uninstall.sh']:
            result = subprocess.run([str(self.checkout / 'scripts' / name), '--help'],
                                    cwd=self.root, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('--check', result.stdout)
        self.assertFalse(self.destination.exists())


if __name__ == '__main__':
    unittest.main()
