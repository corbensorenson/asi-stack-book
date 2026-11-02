from datetime import date
from pathlib import Path
import sys
import unittest
import tempfile
from unittest.mock import patch
from datetime import datetime, timezone


sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from chapter_freshness import declarations, rendered_errors, UNRECORDED_REVIEW
import sync_scaffold
from projection_files import ProjectionFiles

TODAY=date(2026,10,3)
def source(fields):
    return '---\n'+fields+'\n---\n\n## Chapter status\n\n| Field | Value |\n|---|---|\n| Last updated | 1999-12-31 |\n'
def html(rows):
    return '<section id="chapter-status"><h2>Chapter status</h2><table>'+''.join('<tr><td>'+k+'</td><td>'+v+'</td></tr>' for k,v in rows)+'</table></section>'

class ChapterFreshnessTests(unittest.TestCase):
    def test_new_scaffold_dates_creation_in_utc_and_has_one_date_owner(self):
        chapter={'id':'new-owner','title':'New owner','file':'chapters/new-owner.qmd','_part_id':'part','_part_title':'Part'}
        with tempfile.TemporaryDirectory() as directory, patch.object(sync_scaffold,'ROOT',Path(directory).resolve()), patch.object(sync_scaffold,'datetime') as clock:
            clock.now.return_value=datetime(2026,10,3,0,1,tzinfo=timezone.utc)
            files=ProjectionFiles(write=False)
            self.assertTrue(sync_scaffold.write_chapter_stub(chapter,[],files=files))
            body=files.text(Path(directory).resolve()/chapter['file'])
            self.assertEqual({'last_updated':'2026-10-03'},declarations(body,as_of=TODAY))
            clock.now.assert_called_once_with(timezone.utc)
            self.assertNotIn('| Last updated |',body)
            self.assertFalse((Path(directory).resolve()/chapter['file']).exists())
            self.assertFalse(sync_scaffold.write_chapter_stub(chapter,[],files=files))
            self.assertEqual(body,files.text(Path(directory).resolve()/chapter['file']))
    def test_existing_scaffold_sync_and_explicit_rewrite_preserve_declared_events(self):
        chapter={'id':'existing-owner','title':'Existing owner','file':'chapters/existing-owner.qmd','_part_id':'part','_part_title':'Part'}
        fields='last_updated: "2026-07-16"\nsource_reviewed_on: "2026-08-09"\nsource_review_scope: "Only two assigned passages"'
        with tempfile.TemporaryDirectory() as directory, patch.object(sync_scaffold,'ROOT',Path(directory).resolve()), patch.object(sync_scaffold,'datetime') as clock:
            path=Path(directory).resolve()/chapter['file'];path.parent.mkdir();path.write_text(source(fields));before=path.read_bytes();stamp=path.stat().st_mtime_ns
            files=ProjectionFiles(write=False)
            self.assertFalse(sync_scaffold.write_chapter_stub(chapter,[],files=files))
            self.assertTrue(sync_scaffold.write_chapter_stub(chapter,[],rewrite=True,files=files))
            self.assertEqual(declarations(before.decode(),as_of=TODAY),declarations(files.text(path),as_of=TODAY))
            clock.now.assert_not_called()
            self.assertEqual(before,path.read_bytes());self.assertEqual(stamp,path.stat().st_mtime_ns)
    def test_revision_and_scoped_source_review_are_distinct_events(self):
        fields='last_updated: "2026-07-16"\nsource_reviewed_on: "2026-08-09"\nsource_review_scope: "Reviewed the two assigned mechanism passages"'
        value=declarations(source(fields),as_of=TODAY)
        self.assertEqual({'last_updated':'2026-07-16','source_reviewed_on':'2026-08-09','source_review_scope':'Reviewed the two assigned mechanism passages'},value)
        changed=declarations(source(fields.replace('2026-07-16','2026-09-01')),as_of=TODAY)
        self.assertEqual(value['source_reviewed_on'],changed['source_reviewed_on'])
        self.assertEqual('2026-09-01',changed['last_updated'])
    def test_invalid_dates_and_future_events_refuse(self):
        for raw in ('true','20261002','"2026-W40-5"','"2026-02-30"','"2027-01-01"','2026-10-02T12:00:00Z'):
            with self.subTest(raw=raw),self.assertRaises(ValueError):declarations(source('last_updated: '+raw),as_of=TODAY)
        self.assertEqual('2026-02-28',declarations(source('last_updated: 2026-02-28'),as_of=TODAY)['last_updated'])
    def test_duplicate_dates_and_unscoped_review_refuse(self):
        for fields in ('last_updated: "2026-07-16"\nlast_updated: "2026-08-09"',
                       'last_updated: "2026-07-16"\nsource_reviewed_on: "2026-08-09"',
                       'last_updated: "2026-07-16"\nsource_review_scope: "Review scope without an event"',
                       'last_updated: "2026-07-16"\nsource_reviewed_on: "2026-08-09"\nsource_review_scope: " "'):
            with self.subTest(fields=fields),self.assertRaises(ValueError):declarations(source(fields),as_of=TODAY)
    def test_date_display_must_match_actual_declared_owner(self):
        expected={'last_updated':'2026-07-16'}
        rows=[('Chapter revision','2026-07-16'),('Source review',UNRECORDED_REVIEW)]
        self.assertEqual([],rendered_errors(html(rows),expected))
        self.assertTrue(rendered_errors(html([('Chapter revision','2026-08-09'),rows[1]]),expected))
        self.assertTrue(rendered_errors(html(rows+[rows[0]]),expected))
        self.assertTrue(rendered_errors(html(rows+[('Last updated','1999-12-31')]),expected))
    def test_source_review_date_and_scope_cannot_be_laundered_by_revision(self):
        expected={'last_updated':'2026-07-16','source_reviewed_on':'2026-08-09','source_review_scope':'Only the assigned mechanism passages'}
        rows=[('Chapter revision','2026-07-16'),('Source review','2026-08-09'),('Source review scope',expected['source_review_scope'])]
        self.assertEqual([],rendered_errors(html(rows),expected))
        for bad in ([rows[0],('Source review','2026-07-16'),rows[2]],rows[:2],rows+[rows[2]]):
            self.assertTrue(rendered_errors(html(bad),expected))
    def test_hidden_or_outside_status_dates_do_not_satisfy_display_contract(self):
        rows=[('Chapter revision','2026-07-16'),('Source review',UNRECORDED_REVIEW)]
        good=html(rows);expected={'last_updated':'2026-07-16'}
        for bad in (good.replace('<table>','<table hidden>'),good.replace('id="chapter-status"','id="unrelated"'),good.replace('2026-07-16','<span hidden>2026-07-16</span>')):
            with self.subTest(bad=bad):self.assertTrue(rendered_errors(bad,expected))

if __name__=='__main__':unittest.main()
