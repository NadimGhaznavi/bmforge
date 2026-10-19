"""Check selective copies and successful-version bookkeeping in temp trees."""

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "templates"))
from deployment_tools.DeploymentConfig import DeploymentConfig
from deployment_tools.DeploymentFiles import DeploymentFiles
from deployment_tools.ReleaseFiles import ReleaseFiles


class DeploymentFilesTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory(prefix='bmforge-deployment-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / 'source'
        self.installed = self.root / 'installed'
        self.owners = {
            'acme/web.py': ['web'], 'acme/worker.py': ['worker'],
            'acme/shared.py': ['web', 'worker'],
            'acme/version.py': ['web', 'worker', 'setup'],
        }
        self.config = DeploymentConfig(
            targets={'web': ('acme/web.py',), 'worker': ('acme/worker.py',), 'setup': ()},
            dependencies={name: () for name in self.owners},
            manifest='deployment/releases.json', version_marker='.deployment-version',
            version_file='acme/version.py', version_pattern=rb'(VERSION = )"[^"\n]+"',
            scan_roots=('acme',), package_roots=('acme',),
            setup_files=('requirements.txt',), full_setup_target='setup',
        )
        for folder, content in [(self.source, 'new'), (self.installed, 'old')]:
            for name in [*self.owners, 'requirements.txt']:
                path = folder / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            ReleaseFiles(folder, self.config).write({
                'releases': [{'version': '1.0.0', 'targets': []}],
                'artifacts': {name: {'digest': 'a' * 64, 'targets': owners}
                              for name, owners in self.owners.items()},
            })
        (self.installed / self.config.version_marker).write_text('1.0.0\n')
        self.files = DeploymentFiles(self.source, self.installed, self.config)

    def test_selected_copy_preserves_other_services_data_and_success_marker(self):
        data = self.installed / 'uploads/saved.txt'
        data.parent.mkdir()
        data.write_text('User data')
        self.files.copy_application(frozenset({'web'}))
        self.assertEqual((self.installed / 'acme/web.py').read_text(), 'new')
        self.assertEqual((self.installed / 'acme/shared.py').read_text(), 'new')
        self.assertEqual((self.installed / 'acme/worker.py').read_text(), 'old')
        self.assertEqual((self.installed / 'requirements.txt').read_text(), 'old')
        self.assertEqual((self.installed / self.config.version_marker).read_text(), '1.0.0\n')
        self.assertEqual(data.read_text(), 'User data')

    def test_removed_files_are_limited_to_selected_target(self):
        files = ReleaseFiles(self.installed, self.config)
        previous = files.read()
        for name, owner in [('acme/old_web.py', 'web'), ('acme/old_worker.py', 'worker')]:
            previous['artifacts'][name] = {'digest': 'b' * 64, 'targets': [owner]}
            (self.installed / name).write_text('Old')
        files.write(previous)
        self.files.copy_application(frozenset({'web'}))
        self.assertFalse((self.installed / 'acme/old_web.py').exists())
        self.assertTrue((self.installed / 'acme/old_worker.py').exists())

    def test_full_setup_and_completion(self):
        self.files.copy_application(frozenset({'setup'}))
        self.files.copy_setup()
        self.assertEqual((self.installed / 'acme/worker.py').read_text(), 'new')
        self.assertEqual((self.installed / 'requirements.txt').read_text(), 'new')
        self.files.complete('1.0.1')
        self.assertEqual((self.installed / self.config.version_marker).read_text(), '1.0.1\n')
        self.assertEqual((self.installed / self.config.manifest).read_bytes(),
                         (self.source / self.config.manifest).read_bytes())

    def test_missing_source_cannot_advance_success_marker(self):
        (self.source / 'acme/web.py').unlink()
        with self.assertRaises(FileNotFoundError):
            self.files.copy_application(frozenset({'web'}))
        self.assertEqual((self.installed / self.config.version_marker).read_text(), '1.0.0\n')

    def test_manifest_cannot_name_parent_paths(self):
        path = self.installed / self.config.manifest
        metadata = json.loads(path.read_text())
        metadata['artifacts']['acme/../../outside.py'] = {'digest': 'a' * 64, 'targets': ['web']}
        path.write_text(json.dumps(metadata))
        with self.assertRaisesRegex(ValueError, 'artifact path'):
            self.files.copy_application(frozenset({'web'}))


if __name__ == '__main__':
    unittest.main()
