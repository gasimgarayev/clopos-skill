"""Offline regression tests; all mutations stay in temporary directories."""
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from install import files, install
from validate import validate


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / 'repo'
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        self.refs = self.repo / 'skills/clopos/references'
        self.registry = self.refs / 'sources.json'

    def change_registry(self, change):
        data = json.loads(self.registry.read_text(encoding='utf-8'))
        change(data)
        self.registry.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return validate(self.repo)

    def test_current_package(self):
        self.check()

    def test_new_guide_citation_requires_registry_location(self):
        data = json.loads(self.registry.read_text(encoding='utf-8'))
        article = next(a for a in data['help_articles'] if a['used_in'])
        (self.refs / 'new-guide.md').write_text(f"[Source]({article['url']})\n", encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Article citation drift'):
            self.check()

    def test_stale_registry_location_rejected(self):
        def change(data):
            next(a for a in data['help_articles'] if a['used_in'])['used_in'].append('missing-guide.md')
        self.change_registry(change)
        with self.assertRaisesRegex(ValueError, 'Article citation drift'):
            self.check()

    def test_coverage_count_mismatch_rejected(self):
        self.change_registry(lambda d: d['coverage'].update(unique_videos=0))
        with self.assertRaisesRegex(ValueError, 'Coverage totals'):
            self.check()

    def test_recheck_cannot_predate_retrieval(self):
        self.change_registry(lambda d: d['help_articles'][0].update(last_checked_at='2000-01-01'))
        with self.assertRaisesRegex(ValueError, 'Recheck precedes retrieval'):
            self.check()

    def test_broken_guide_link_rejected(self):
        (self.refs / 'new-guide.md').write_text('[Missing](missing.md)\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Broken local link'):
            self.check()


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        (self.source / 'SKILL.md').write_text('original', encoding='utf-8')
        self.dest = self.root / 'skills/clopos'

    def test_dry_run_does_not_create_destination(self):
        install(self.source, self.dest, dry_run=True)
        self.assertFalse(self.dest.parent.exists())

    def test_install_and_repeat_preserve_exact_contents(self):
        install(self.source, self.dest)
        self.assertEqual(files(self.source), files(self.dest))
        install(self.source, self.dest)
        self.assertEqual(files(self.source), files(self.dest))

    def test_local_edits_are_never_overwritten(self):
        install(self.source, self.dest)
        edited = self.dest / 'SKILL.md'
        edited.write_text('local edits', encoding='utf-8')
        with self.assertRaises(ValueError):
            install(self.source, self.dest)
        self.assertEqual(edited.read_text(encoding='utf-8'), 'local edits')

    def test_symlink_destination_is_not_followed(self):
        link = self.root / 'link'
        link.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError):
            install(self.source, link)
        self.assertEqual((self.source / 'SKILL.md').read_text(encoding='utf-8'), 'original')


if __name__ == '__main__':
    unittest.main()
