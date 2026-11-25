import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import jobkit
import export_obsidian as vault

class VaultTests(unittest.TestCase):
    def allow_export(self,w,enabled=True):
        changes=w/'change.json'
        jobkit.write(changes,{'grants':{'obsidian_export':enabled}})
        jobkit.update_permissions(w,changes,'test user choice')

    def test_export_needs_opt_in_even_for_existing_vault(self):
        with tempfile.TemporaryDirectory() as t:
            w=Path(t)/'workspace'; jobkit.init(w)
            with self.assertRaisesRegex(ValueError,'export is off'): vault.export(w)
            self.assertFalse((w/'obsidian').exists())
            self.allow_export(w); vault.export(w)
            home=w/'obsidian/Home.md'; before=home.stat().st_mtime_ns
            self.allow_export(w,False)
            with self.assertRaisesRegex(ValueError,'export is off'): vault.export(w)
            self.assertEqual(home.stat().st_mtime_ns,before)

    def test_refresh_preserves_notes_and_counts_rejection_as_submitted(self):
        with tempfile.TemporaryDirectory() as t:
            w=Path(t)/'workspace';jobkit.init(w);self.allow_export(w)
            p=Path(t)/'job.json';p.write_text(json.dumps({'company':'Example','role':'Analyst','url':'https://example.com/jobs/1'}))
            jid=jobkit.upsert(w,p)['id']
            jobkit.transition(w,jid,'Submitted','fictional receipt')
            jobkit.transition(w,jid,'Rejected','fictional response')
            vault.export(w)
            note=w/'obsidian/Applications'/f'{jid}.md';note.write_text(note.read_text()+'Personal study notes\n')
            vault.export(w)
            self.assertIn('Personal study notes',note.read_text())
            self.assertIn('1 submitted',(w/'obsidian/Home.md').read_text())
            self.assertNotIn('application_email',(w/'obsidian/Home.md').read_text())

    def test_reschedule_cancel_and_duplicate(self):
        with tempfile.TemporaryDirectory() as t:
            w=Path(t)/'workspace';jobkit.init(w);self.allow_export(w)
            p=w/'interviews/event.json'
            m={'id':'test','company':'Example','role':'Analyst','status':'Scheduled','start':'2099-06-10T14:00:00-04:00','end':'2099-06-10T14:30:00-04:00'}
            p.write_text(json.dumps(m));self.assertEqual(vault.export(w)['upcoming_interviews'],1)
            m['start']='2099-06-11T14:00:00-04:00';m['end']='2099-06-11T14:30:00-04:00';p.write_text(json.dumps(m));vault.export(w)
            self.assertEqual((w/'obsidian/Interviews.ics').read_text().count('BEGIN:VEVENT'),1)
            q=w/'interviews/duplicate.json';q.write_text(json.dumps(m))
            with self.assertRaises(ValueError):vault.export(w)
            q.unlink();m['status']='Cancelled';p.write_text(json.dumps(m))
            self.assertEqual(vault.export(w)['upcoming_interviews'],0)

    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):vault.stamp('2099-06-10T14:00:00')
