"""Verify BMForge's own scripts in an isolated project with a local remote."""

from pathlib import Path
import unittest

import test_release_templates as fixtures


ROOT = Path(__file__).resolve().parents[1]
CONSTANTS = 'bmforge/constants/DBMForge.py'


class BMForgeReleaseTests(unittest.TestCase):
    def test_project_release_preserves_changelog_and_publishes_consistent_metadata(self):
        fixture = fixtures.ReleaseTests()
        self.addCleanup(fixture.doCleanups)
        fixture.setUp()
        for name in ['scripts/new-release.sh', 'scripts/check-cmdb.py', CONSTANTS,
                     'bmforge/__init__.py', 'bmforge/constants/__init__.py', 'CHANGELOG.md']:
            fixture.write(name, (ROOT / name).read_text())
        fixture.commit('Configure BMForge release files')
        before = (fixture.repo / 'CHANGELOG.md').read_text()
        metadata = fixtures.checker.validate((fixture.repo / CONSTANTS).read_text(), 'BMForge', CONSTANTS)
        major, minor, patch = map(int, metadata['VERSION'].split('-', 1)[0].split('+', 1)[0].split('.'))
        patch += 1
        while f'## [{major}.{minor}.{patch}]' in before:
            patch += 1
        version = f'{major}.{minor}.{patch}'
        result = fixture.release(version, 'BMForge test release')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        values = fixtures.checker.validate((fixture.repo / CONSTANTS).read_text(), 'BMForge', CONSTANTS)
        self.assertEqual(values['VERSION'], version)
        self.assertEqual(values['CMDB_TYPE'], 'Application')
        self.assertEqual(values['CMDB_CODENAME'], 'BMForge test release')
        self.assertEqual(values['BASE_DIR'], '/opt/prod/bmforge')
        released = (fixture.repo / 'CHANGELOG.md').read_text()
        self.assertEqual(released.split('## [Unreleased]', 1)[0], before.split('## [Unreleased]', 1)[0])
        self.assertTrue(released.endswith(before.split('## [Unreleased]', 1)[1]))
        self.assertIn(f'## [{version}] - ', released)
        tip = fixture.git('rev-parse', 'HEAD')
        for ref in ['main', 'dev', 'origin/main', 'origin/dev', f'v{version}^{{commit}}']:
            self.assertEqual(fixture.git('rev-parse', ref), tip)
        self.assertEqual(fixture.git('cat-file', '-t', f'v{version}'), 'tag')
        self.assertEqual(fixture.git('branch', '--show-current'), f'feat/maint-{major}.{minor}.{patch + 1}')
        self.assertEqual(fixture.git('status', '--porcelain'), '')


if __name__ == '__main__':
    unittest.main()
