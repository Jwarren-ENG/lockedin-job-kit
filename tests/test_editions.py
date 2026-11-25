import hashlib
import json
import posixpath
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from package import package


class EditionTests(unittest.TestCase):
    def test_editions_ship_the_right_entrypoints_and_valid_checksums(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            outputs = package(out)
            expected = {}
            for tier, starter in [('lite', 'CHAT_STARTER.txt'), ('local', 'LOCAL_STARTER.txt'),
                                  ('advanced', 'editions/ADVANCED_STARTER.txt')]:
                archive = out / f'lockedin-{tier}.zip'
                with zipfile.ZipFile(archive) as bundle:
                    files = set(bundle.namelist())
                    self.assertIn(starter, files)
                    self.assertIn(starter, bundle.read('START HERE.txt').decode())
                    self.assertIn('README.md', files)
                    self.assertIn('OPTIONAL_OBSIDIAN.md', files)
                    self.assertEqual('scripts/jobkit.py' in files, tier == 'advanced')
                    self.assertIsNone(bundle.testzip())
                    if tier == 'advanced':
                        manifest = json.loads(bundle.read('.codex-plugin/plugin.json'))
                        self.assertEqual(manifest['interface']['displayName'], '#LOCKEDIN Job Kit')
                        self.assertIn('assets/setup.html', files)
                    for name in files:
                        if name.endswith('.md'):
                            body = bundle.read(name).decode()
                            for target in re.findall(r'\]\((?![a-z]+:|#)([^)\s]+)\)', body):
                                relative = target.split('#')[0]
                                if not relative:
                                    continue
                                path = posixpath.normpath(str(PurePosixPath(name).parent / relative))
                                self.assertIn(path, files, f'{tier}: {name} links to {target}')
            for path in outputs:
                expected[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            manifest = dict(line.split('  ')[::-1] for line in (out/'SHA256SUMS.txt').read_text().splitlines())
            self.assertEqual(expected, manifest)
            self.assertEqual(expected['lockedin-advanced.zip'], expected['job-search-kit.plugin'])
            self.assertLess((out/'lockedin-lite.zip').stat().st_size,(out/'lockedin-advanced.zip').stat().st_size)
