import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import hashlib

spec=importlib.util.spec_from_file_location('jobkit',Path(__file__).resolve().parents[1]/'scripts/jobkit.py')
kit=importlib.util.module_from_spec(spec);spec.loader.exec_module(kit)

class Workflow(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.w=Path(self.tmp.name)/'private';kit.init(self.w)
    def tearDown(self): self.tmp.cleanup()
    def source(self,name,data):
        p=Path(self.tmp.name)/name;kit.write(p,data);return p
    def profile(self,auto=False,dem=None):
        p=kit.read(kit.ROOT/'assets/profile-template.json');p['identity'].update(name='Test Applicant',application_email='applicant@example.com');p['resume']['confirmed']=True
        grants={k:False for k in kit.PERMISSIONS};grants.update(save_profile=True,auto_submit=auto,use_computer=True)
        return self.source('setup.json',{'profile':p,'permissions':{'grants':grants,'max_submissions_per_day':1},'demographics':dem or {}})
    def job(self,req='1'):
        return kit.upsert(self.w,self.source('job.json',{'company':'Fictional Employer','role':'Analyst','url':'https://example.com/jobs/'+req,'requisition':req}))['id']
    def review(self,jid):
        (self.w/'resumes/test.pdf').write_bytes(b'%PDF-test-fixture-not-a-real-resume')
        with kit.connect(self.w) as db:
            j=kit.loadjob(db,jid);j['resume']='resumes/test.pdf';kit.putjob(db,j)
        r=kit.read(kit.ROOT/'assets/review-template.json')
        for k in ('official_posting_verified','matches_search','eligibility_verified','facts_verified','resume_one_page_verified','form_reviewed','host_allows_submission'):r[k]=True
        r.update(job_id=jid,permission_revision=kit.read(self.w/'permissions.json')['revision'],resume_sha256=hashlib.sha256((self.w/'resumes/test.pdf').read_bytes()).hexdigest(),answer_evidence={'name':'fictional test confirmation'})
        return self.source('review.json',r)
    def test_blank_permissions(self):self.assertFalse(any(kit.read(self.w/'permissions.json')['grants'].values()))
    def test_legacy_setup_defaults_and_pause(self):
        kit.update_permissions(self.w,self.source('pause.json',{'paused':True}),'user paused')
        path=self.profile(True)
        bundle=kit.read(path)
        bundle['permissions']['grants']={k:bundle['permissions']['grants'][k] for k in kit.LEGACY_PERMISSIONS}
        kit.write(path,bundle)
        kit.import_profile(self.w,path,'user imported existing setup')
        state=kit.read(self.w/'permissions.json')
        self.assertTrue(state['paused'])
        self.assertFalse(any(state['grants'][k] for k in ('use_computer','share_address','obsidian_export','read_chat_history')))
        self.assertEqual(kit.read(self.w/'sources.json'),[])

    def test_computer_permission_precedes_submission(self):
        kit.import_profile(self.w,self.profile(True),'user setup')
        kit.update_permissions(self.w,self.source('changes.json',{'grants':{'use_computer':False}}),'revoked')
        jid=self.job()
        self.assertFalse(kit.reserve(self.w,jid,self.review(jid))['allowed'])

    def test_history_requires_named_conversations_and_can_be_revoked(self):
        path=self.profile(); bundle=kit.read(path)
        bundle['permissions']['grants']['read_chat_history']=True
        kit.write(path,bundle)
        with self.assertRaisesRegex(ValueError,'specific conversations'):
            kit.import_profile(self.w,path,'candidate selected history')
        bundle['profile']['scope_notes']={'history':'Only the inventory project chat'}
        kit.write(path,bundle); kit.import_profile(self.w,path,'candidate selected one chat')
        self.assertTrue(kit.read(self.w/'permissions.json')['grants']['read_chat_history'])
        kit.update_permissions(self.w,self.source('changes.json',{'grants':{'read_chat_history':False}}),'setup review ended')
        self.assertFalse(kit.read(self.w/'permissions.json')['grants']['read_chat_history'])

    def test_daily_cap_uses_local_midnight(self):
        from unittest.mock import patch
        path=self.profile(True); bundle=kit.read(path)
        bundle['profile']['search']['timezone']='America/New_York'; kit.write(path,bundle)
        kit.import_profile(self.w,path,'confirmed')
        first=self.job(); second=self.job('2')
        for when,jid,expected in [('2026-10-31T23:55:00+00:00',first,True),
                                  ('2026-11-01T01:05:00+00:00',second,False),
                                  ('2026-11-01T04:05:00+00:00',second,True)]:
            with patch.object(kit,'now',return_value=when):
                self.assertEqual(kit.reserve(self.w,jid,self.review(jid))['allowed'],expected)

    def test_permission_change_preserves_profile(self):
        kit.import_profile(self.w,self.profile(True),'test');before=kit.read(self.w/'profile.json');kit.update_permissions(self.w,self.source('changes.json',{'grants':{'auto_submit':False}}),'user revoked');self.assertEqual(before,kit.read(self.w/'profile.json'));self.assertFalse(kit.read(self.w/'permissions.json')['grants']['auto_submit'])
    def test_unknown_permission_rejected(self):
        with self.assertRaises(ValueError):kit.update_permissions(self.w,self.source('changes.json',{'grants':{'accept_offers':True}}),'test')
    def test_init_no_overwrite(self):
        with self.assertRaises(ValueError):kit.init(self.w)
    def test_no_demographic_storage_without_consent(self):
        with self.assertRaises(ValueError):kit.import_profile(self.w,self.profile(dem={'gender':'Test'}),'test user choice')
    def test_dedup_requisition(self):
        j=self.job();result=kit.upsert(self.w,self.source('second.json',{'company':'FICTIONAL EMPLOYER','role':'New title','url':'https://example.com/alternate','requisition':'1'}));self.assertEqual(j,result['id']);self.assertTrue(result['duplicate'])
    def test_tracking_url_canonicalization(self):self.assertEqual(kit.canonical('https://example.com/job?utm_source=board&id=3'),kit.canonical('https://example.com/job?id=3'))
    def test_no_secret_url(self):
        with self.assertRaises(ValueError):kit.canonical('https://user:password@example.com/job')
    def test_manual_mode_blocks(self):
        kit.import_profile(self.w,self.profile(),'test');j=self.job();self.assertFalse(kit.reserve(self.w,j,self.review(j))['allowed'])
    def test_stale_permissions(self):
        kit.import_profile(self.w,self.profile(True),'test');j=self.job();r=self.review(j);p=kit.read(self.w/'permissions.json');p['revision']='changed';kit.write(self.w/'permissions.json',p);self.assertFalse(kit.reserve(self.w,j,r)['allowed'])
    def test_changed_resume_blocks(self):
        kit.import_profile(self.w,self.profile(True),'test');j=self.job();r=self.review(j);(self.w/'resumes/test.pdf').write_bytes(b'changed');self.assertFalse(kit.reserve(self.w,j,r)['allowed'])
    def test_unknown_answers_block(self):
        kit.import_profile(self.w,self.profile(True),'test');j=self.job();f=self.review(j);r=kit.read(f);r['unknown_answers']=['availability'];kit.write(f,r);self.assertFalse(kit.reserve(self.w,j,f)['allowed'])
    def test_consent_block(self):
        kit.import_profile(self.w,self.profile(True),'test');j=self.job();f=self.review(j);r=kit.read(f);r['consents_needed']=['partner_sharing'];kit.write(f,r);self.assertFalse(kit.reserve(self.w,j,f)['allowed'])
    def test_pause_blocks(self):
        kit.import_profile(self.w,self.profile(True),'test');j=self.job();r=self.review(j);p=kit.read(self.w/'permissions.json');p['paused']=True;kit.write(self.w/'permissions.json',p);self.assertFalse(kit.reserve(self.w,j,r)['allowed'])
    def test_reservation_duplicate_and_daily_limit(self):
        kit.import_profile(self.w,self.profile(True),'test');j=self.job();r=self.review(j);self.assertTrue(kit.reserve(self.w,j,r)['allowed']);self.assertFalse(kit.reserve(self.w,j,r)['allowed']);j2=self.job('2');self.assertFalse(kit.reserve(self.w,j2,self.review(j2))['allowed'])
    def test_evidence_required(self):
        with self.assertRaises(ValueError):kit.transition(self.w,self.job(),'Submitted','')
    def test_email_event_dedup(self):
        j=self.job();kit.transition(self.w,j,'Interview','User scheduled','email-1');self.assertTrue(kit.transition(self.w,j,'Interview','User scheduled','email-1')['duplicate_event'])
    def test_submission_date_preserved(self):
        j=self.job();kit.transition(self.w,j,'Submitted','User confirmed');kit.transition(self.w,j,'Interview','Invitation');
        with kit.connect(self.w) as db:self.assertTrue(kit.loadjob(db,j)['submitted_at'])
    def test_no_uncertain_reset(self):
        kit.import_profile(self.w,self.profile(True),'test');j=self.job();kit.reserve(self.w,j,self.review(j))
        with self.assertRaises(ValueError):kit.transition(self.w,j,'Ready','try again')
    def test_csv_formula_injection_and_no_pii(self):
        j=self.job();kit.upsert(self.w,self.source('job.json',{'company':'Fictional Employer','role':'=1+1','url':'https://example.com/jobs/1','requisition':'1'}));kit.export(self.w);s=(self.w/'exports/applications.csv').read_text();self.assertIn("'=1+1",s);self.assertNotIn('application_email',s)

if __name__=='__main__':unittest.main()
