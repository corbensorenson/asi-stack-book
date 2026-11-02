"""Release channels retain a complete prior tree until one installation step."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_release_channels as channels


class ReleaseChannelTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name).resolve() / 'rendered'
        (self.site / 'status').mkdir(parents=True)
        (self.site / channels.STATUS_REL).write_text(json.dumps({
            'source_commit': 'a' * 40, 'source_tree_state': 'clean',
            'build_context': 'tested_commit', 'status_id': 'channel-fixture',
        }))
        (self.site / 'index.html').write_text('complete old root')
        self.policy = channels.load_json(channels.POLICY)
        channels.build_channels(self.site, self.policy, allow_local=False)
        self.before = channels.file_rows(self.site)

    def test_complete_installation_and_read_only_check(self):
        (self.site / 'index.html').write_text('complete new root')
        with self.assertRaisesRegex(ValueError, 'differs'):
            channels.build_channels(self.site, self.policy, allow_local=False, check=True)
        channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertEqual('complete new root', (self.site / 'latest/index.html').read_text())
        before = {path: path.stat().st_mtime_ns for path in self.site.rglob('*')}
        channels.build_channels(self.site, self.policy, allow_local=False, check=True)
        self.assertEqual(before, {path: path.stat().st_mtime_ns for path in self.site.rglob('*')})

    def test_interrupted_copy_preserves_all_previous_files(self):
        (self.site / 'index.html').write_text('complete new root')
        before = channels.file_rows(self.site)
        with patch.object(channels.shutil, 'copytree', side_effect=OSError('copy interrupted')):
            with self.assertRaises(OSError):
                channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertEqual(before, channels.file_rows(self.site))

    def test_changed_source_does_not_install_a_mixed_mirror(self):
        (self.site / 'index.html').write_text('complete new root')
        real_copy = shutil.copytree
        def changed_copy(*args, **kwargs):
            if Path(args[0]).resolve() == self.site.resolve():
                (self.site / 'index.html').write_text('concurrent root edit')
            return real_copy(*args, **kwargs)
        with patch.object(channels.shutil, 'copytree', side_effect=changed_copy):
            with self.assertRaisesRegex(ValueError, 'source changed'):
                channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertEqual('complete old root', (self.site / 'latest/index.html').read_text())

    def test_unknown_version_content_and_symlinks_are_preserved(self):
        sentinel = self.site / 'versions/personal.txt'
        sentinel.write_text('retain')
        with self.assertRaisesRegex(ValueError, 'unrecognized'):
            channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertEqual('retain', sentinel.read_text())
        sentinel.unlink()
        (self.site / 'link').symlink_to(self.site / 'index.html')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertTrue((self.site / 'link').is_symlink())

    def test_unknown_latest_files_and_empty_directories_are_preserved(self):
        sentinel = self.site / 'latest/personal.txt'
        sentinel.write_text('retain')
        with self.assertRaisesRegex(ValueError, 'unrecognized latest'):
            channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertEqual('retain', sentinel.read_text())
        sentinel.unlink()
        empty = self.site / 'latest/personal-empty'
        empty.mkdir()
        identity = (empty.stat().st_dev, empty.stat().st_ino)
        with self.assertRaisesRegex(ValueError, 'directory'):
            channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertEqual(identity, (empty.stat().st_dev, empty.stat().st_ino))

    def test_exception_after_exchange_retains_complete_previous_channels(self):
        (self.site / 'index.html').write_text('complete new root')
        exchange = channels.exchange_directories
        def interrupted(left, right):
            exchange(left, right)
            raise OSError('authored post-swap exception')
        with patch.object(channels, 'exchange_directories', side_effect=interrupted):
            with self.assertRaisesRegex(OSError, 'post-swap'):
                channels.build_channels(self.site, self.policy, allow_local=False)
        stage = list(self.site.parent.glob('.asi-stack-release-channels-*'))[0]
        self.assertEqual('complete old root', (stage / 'site/latest/index.html').read_text())
        self.assertEqual('complete new root', (self.site / 'latest/index.html').read_text())
        self.assertEqual('installation_outcome_unconfirmed', json.loads((stage / 'staging.json').read_bytes())['state'])

    def test_fsync_uncertainty_and_last_moment_prior_edit_keep_displaced_tree(self):
        (self.site / 'index.html').write_text('complete new root')
        exchange = channels.exchange_directories
        def changed(left, right):
            (right / 'personal-empty').mkdir()
            exchange(left, right)
        with patch.object(channels, 'exchange_directories', side_effect=changed):
            with self.assertRaisesRegex(ValueError, 'directory'):
                channels.build_channels(self.site, self.policy, allow_local=False)
        stage = list(self.site.parent.glob('.asi-stack-release-channels-*'))[0]
        self.assertTrue((stage / 'site/personal-empty').is_dir())
        self.assertEqual('complete old root', (stage / 'site/latest/index.html').read_text())
        # Return only the owned fixture to a known state for a separate fsync fault.
        (self.site / 'index.html').write_text('third root')
        sync = channels.sync_directory
        def fail(directory):
            if directory == self.site.parent:
                raise OSError('authored durability failure')
            sync(directory)
        with patch.object(channels, 'sync_directory', side_effect=fail):
            with self.assertRaisesRegex(OSError, 'durability'):
                channels.build_channels(self.site, self.policy, allow_local=False)
        stages = list(self.site.parent.glob('.asi-stack-release-channels-*'))
        self.assertEqual(2, len(stages))
        self.assertTrue(any((item / 'site/latest/index.html').read_text() == 'complete new root' for item in stages))
        self.assertEqual('third root', (self.site / 'latest/index.html').read_text())

    def test_failed_exchange_and_competing_writer_preserve_previous(self):
        (self.site / 'index.html').write_text('complete new root')
        before = channels.file_rows(self.site)
        with patch.object(channels, 'exchange_directories', side_effect=OSError('unsupported')):
            with self.assertRaises(OSError):
                channels.build_channels(self.site, self.policy, allow_local=False)
        with channels.bundle_lock(self.site):
            with self.assertRaisesRegex(ValueError, 'another builder'):
                channels.build_channels(self.site, self.policy, allow_local=False)
        self.assertEqual(before, channels.file_rows(self.site))

    def test_process_exit_at_exchange_exposes_only_complete_channels(self):
        (self.site / 'index.html').write_text('complete new root')
        script = '''
import os, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import build_release_channels as c
exchange = c.exchange_directories
def interrupted(left, right):
    if sys.argv[3] == 'before':
        os._exit(90)
    exchange(left, right)
    os._exit(91)
c.exchange_directories = interrupted
c.build_channels(Path(sys.argv[2]), c.load_json(c.POLICY), allow_local=False)
'''
        for phase, code, content in [('before', 90, 'complete old root'), ('after', 91, 'complete new root')]:
            with self.subTest(phase=phase):
                result = subprocess.run([sys.executable, '-c', script, str(Path(channels.__file__).parent),
                                         str(self.site), phase], capture_output=True, timeout=30)
                self.assertEqual(code, result.returncode, result.stderr.decode())
                self.assertEqual(content, (self.site / 'latest/index.html').read_text())
                self.assertTrue((self.site / channels.INDEX_REL).is_file())


if __name__ == '__main__':
    unittest.main()
