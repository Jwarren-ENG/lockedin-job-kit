#!/usr/bin/env python3
"""Local state for an agent-operated job search. No network calls or credentials."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
PERMISSIONS = ('save_profile','save_demographics','auto_submit','read_email','daily_runs',
               'create_accounts','recruitment_privacy','talent_pool','partner_sharing','ai_notes',
               'answer_demographics')
LEGACY_PERMISSIONS = PERMISSIONS
PERMISSIONS = LEGACY_PERMISSIONS + ('use_computer', 'share_address', 'obsidian_export', 'read_chat_history')
STATES = ('Discovered','Shortlisted','Preparing','Ready','Submitting','Submitted',
          'Submission uncertain','Interview','Assessment','Rejected','Offer','Withdrawn','Closed')
TERMINAL = ('Submitted','Interview','Assessment','Rejected','Offer','Withdrawn')
FIELDS = ('id','company','role','location','url','requisition','salary_min','salary_max',
          'currency','pay_period','posted_at','first_seen','status','submitted_at','next_action',
          'deadline','contact','resume','notes','skills_to_learn','evidence')

def now():
    return datetime.now(timezone.utc).isoformat()

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.tmp-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)

def canonical(url):
    p = urlsplit(url)
    if p.scheme not in ('https','http') or not p.hostname or p.username or p.password:
        raise ValueError('Provide a public http(s) application URL without credentials')
    query = [(k,v) for k,v in parse_qsl(p.query) if not k.lower().startswith('utm_') and k.lower() not in ('source','ref','gh_src','lever-source')]
    return urlunsplit((p.scheme,p.netloc.lower(),p.path.rstrip('/'),urlencode(sorted(query)),''))

def key(job):
    company = ' '.join(job['company'].casefold().split())
    identity = company+'|'+str(job['requisition']).casefold() if job.get('requisition') else canonical(job['url'])
    return hashlib.sha256(identity.encode()).hexdigest()[:20]

class ClosingConnection(sqlite3.Connection):
    def __exit__(self,*args):
        try: return super().__exit__(*args)
        finally: self.close()

def connect(workspace):
    db = sqlite3.connect(Path(workspace)/'applications.sqlite', timeout=15, factory=ClosingConnection)
    db.row_factory = sqlite3.Row
    db.execute('CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, data TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, event_key TEXT UNIQUE, at TEXT NOT NULL, job_id TEXT, kind TEXT NOT NULL, data TEXT NOT NULL)')
    db.commit()
    return db

def event(db, kind, data, job_id=None, event_key=None):
    db.execute('INSERT INTO events(event_key,at,job_id,kind,data) VALUES(?,?,?,?,?)',
               (event_key,now(),job_id,kind,json.dumps(data)))

def loadjob(db, jid):
    r = db.execute('SELECT data FROM jobs WHERE id=?',(jid,)).fetchone()
    if not r: raise ValueError('Unknown application ID')
    return json.loads(r[0])

def putjob(db, j):
    db.execute('INSERT OR REPLACE INTO jobs VALUES(?,?)',(j['id'],json.dumps(j)))

def init(workspace):
    w = Path(workspace).expanduser().resolve()
    if w == ROOT or ROOT in w.parents: raise ValueError('Private workspace must be outside the shared plugin')
    if (w/'profile.json').exists(): raise ValueError('Workspace already exists; initialization will not overwrite it')
    w.mkdir(parents=True, exist_ok=True, mode=0o700)
    for d in ('resumes','applications','interviews','exports'): (w/d).mkdir(exist_ok=True)
    profile = read(ROOT/'assets/profile-template.json')
    write(w/'profile.json',profile)
    write(w/'permissions.json',{'version':1,'revision':now(),'paused':False,'max_submissions_per_day':3,
          'grants':{p:False for p in PERMISSIONS},'evidence':None})
    write(w/'demographics.json',{})
    write(w/'sources.json',[])
    write(w/'schedule.json',{'status':'not_configured','host_id':None,'timezone':None,'time':'08:00','last_successful_run':None})
    (w/'resumes/base.tex').write_text((ROOT/'assets/resume-template.tex').read_text(),encoding='utf-8')
    (w/'.gitignore').write_text('*\n!.gitignore\n',encoding='utf-8')
    with connect(w): pass
    export(w)
    return {'workspace':str(w),'status':'onboarding_required'}

def import_profile(w, source, evidence):
    bundle = read(source)
    p = bundle['profile']
    grants = bundle['permissions']['grants']
    if set(grants) == set(LEGACY_PERMISSIONS):
        grants = {key: grants.get(key, False) for key in PERMISSIONS}
    if set(grants) != set(PERMISSIONS) or any(type(v) is not bool for v in grants.values()):
        raise ValueError('Permission keys must exactly match supported booleans')
    if grants.get('read_chat_history') and not str(p.get('scope_notes', {}).get('history') or '').strip():
        raise ValueError('Name the specific conversations authorized for this setup')
    if not grants['save_profile']: raise ValueError('Local profile storage was not authorized')
    if not evidence.strip(): raise ValueError('Record the user action authorizing import')
    if not p.get('identity',{}).get('name') or '@' not in p.get('identity',{}).get('application_email',''):
        raise ValueError('Name and application email required')
    limit = bundle['permissions'].get('max_submissions_per_day',3)
    if type(limit) is not int or not 1 <= limit <= 50: raise ValueError('Daily limit must be 1–50')
    dem = bundle.get('demographics',{})
    if dem and not grants['save_demographics']: raise ValueError('Demographic storage was not authorized')
    zone = p.get('search', {}).get('timezone') or 'UTC'
    try:
        ZoneInfo(zone)
    except (ValueError, ZoneInfoNotFoundError) as exc:
        raise ValueError('Choose a time zone such as America/New_York') from exc
    paused = read(Path(w)/'permissions.json').get('paused', False)
    permissions = {'version':1,'revision':now(),'paused':paused,'max_submissions_per_day':limit,'grants':grants,'evidence':evidence}
    # Import is a user review step, never inferred from a resume or webpage.
    p['confirmed_at'] = now()
    write(Path(w)/'profile.json',p)
    write(Path(w)/'permissions.json',permissions)
    write(Path(w)/'demographics.json',dem if grants['save_demographics'] else {})
    with connect(w) as db: event(db,'profile_import',{'permissions_revision':permissions['revision'],'evidence':evidence})
    return {'status':'profile_saved','permission_revision':permissions['revision']}

def upsert(w, source):
    incoming = read(source)
    for field in ('company','role','url'):
        if not incoming.get(field): raise ValueError('Missing job '+field)
    incoming['url'] = canonical(incoming['url'])
    jid = key(incoming)
    with connect(w) as db:
        # Also match the canonical URL if a requisition was discovered later.
        existing = [json.loads(r[0]) for r in db.execute('SELECT data FROM jobs')]
        old = next((j for j in existing if j['id']==jid or canonical(j['url'])==incoming['url']),None)
        j = old or {'id':jid,'status':'Discovered','first_seen':now(),'submitted_at':None}
        for k,v in incoming.items():
            if k not in ('id','status','first_seen','submitted_at','evidence','authorization'): j[k] = v
        putjob(db,j)
        event(db,'job_updated' if old else 'job_discovered',{'url':j['url']},j['id'])
    export(w)
    return {'id':j['id'],'duplicate':bool(old),'status':j['status']}

def update_permissions(w, source, evidence):
    changes=read(source)
    if not evidence.strip(): raise ValueError('User instruction evidence required')
    if set(changes)-{'grants','paused','max_submissions_per_day'}: raise ValueError('Unsupported permission change')
    updates=changes.get('grants',{})
    if set(updates)-set(PERMISSIONS) or any(type(v) is not bool for v in updates.values()): raise ValueError('Invalid grant update')
    if 'paused' in changes and type(changes['paused']) is not bool: raise ValueError('paused must be boolean')
    if 'max_submissions_per_day' in changes and (type(changes['max_submissions_per_day']) is not int or not 1<=changes['max_submissions_per_day']<=50): raise ValueError('Daily limit must be 1–50')
    if updates.get('read_chat_history'):
        profile = read(Path(w)/'profile.json')
        if not str(profile.get('scope_notes', {}).get('history') or '').strip():
            raise ValueError('Name the specific conversations authorized for this setup')
    p=read(Path(w)/'permissions.json');p['grants'].update(updates)
    for field in ('paused','max_submissions_per_day'):
        if field in changes:p[field]=changes[field]
    p.update(revision=now(),evidence=evidence);write(Path(w)/'permissions.json',p)
    with connect(w) as db:event(db,'permissions_changed',{'changes':changes,'evidence':evidence,'revision':p['revision']})
    return {'revision':p['revision'],'changed':changes,'note':'Also update the native scheduler if cadence permission changed. Existing employer disclosures cannot be undone.'}

def gate(w, jid, review_file):
    p = read(Path(w)/'profile.json'); permission = read(Path(w)/'permissions.json'); review = read(review_file)
    reasons=[]
    with connect(w) as db: j=loadjob(db,jid)
    if permission.get('paused'): reasons.append('Automation is paused')
    if not permission['grants'].get('save_profile'): reasons.append('Profile reuse permission revoked')
    if not permission['grants'].get('use_computer'):
        reasons.append('Computer use for employer forms has not been authorized')
    if not p.get('confirmed_at'): reasons.append('Profile has not been confirmed')
    if not p.get('resume',{}).get('confirmed'): reasons.append('Authoritative resume facts have not been confirmed')
    if not permission['grants'].get('auto_submit'):
        approval=review.get('user_submit_approval')
        if not isinstance(approval,dict) or approval.get('job_id')!=jid or not approval.get('evidence') or not approval.get('at'):
            reasons.append('User approval needed for this application')
    if j['status'] in TERMINAL+('Submitting','Submission uncertain','Closed'): reasons.append('Duplicate, closed or uncertain submission')
    for field in ('official_posting_verified','matches_search','eligibility_verified','facts_verified','resume_one_page_verified','form_reviewed','host_allows_submission'):
        if review.get(field) is not True: reasons.append('Review required: '+field)
    if review.get('job_id')!=jid: reasons.append('Review belongs to a different job')
    if review.get('permission_revision')!=permission['revision']: reasons.append('Permissions changed; repeat review')
    if review.get('unknown_answers'): reasons.append('Required answers remain unknown')
    for category in review.get('consents_needed',[]):
        if category not in PERMISSIONS or not permission['grants'].get(category): reasons.append('Consent not granted: '+str(category))
    resume = (Path(w)/str(j.get('resume',''))).resolve()
    if not resume.is_relative_to(Path(w).resolve()): reasons.append('Resume must be inside the private workspace')
    elif not resume.is_file() or resume.suffix.lower()!='.pdf': reasons.append('Role-specific PDF missing')
    elif review.get('resume_sha256')!=hashlib.sha256(resume.read_bytes()).hexdigest(): reasons.append('Resume changed; review it again')
    if not review.get('answer_evidence'): reasons.append('Confirmed answer sources missing')
    return j,permission,review,reasons

def reserve(w,jid,review_file):
    j,p,r,reasons=gate(w,jid,review_file)
    if reasons: return {'allowed':False,'reasons':reasons}
    with connect(w) as db:
        db.execute('BEGIN IMMEDIATE')
        current=loadjob(db,jid)
        if current['status'] in TERMINAL+('Submitting','Submission uncertain','Closed'):
            return {'allowed':False,'reasons':['Submission already reserved or completed']}
        zone = ZoneInfo(read(Path(w)/'profile.json').get('search', {}).get('timezone') or 'UTC')
        local_time = datetime.fromisoformat(now()).astimezone(zone)
        midnight = local_time.replace(hour=0, minute=0, second=0, microsecond=0)
        bounds = tuple(t.astimezone(timezone.utc).isoformat() for t in (midnight, midnight + timedelta(days=1)))
        count = db.execute("SELECT count(*) FROM events WHERE kind='submission_reserved' AND at>=? AND at<?", bounds).fetchone()[0]
        if count>=p['max_submissions_per_day']: return {'allowed':False,'reasons':['Daily submission limit reached for '+str(zone)]}
        # An unresolved reservation is deliberately never auto-retried.
        current['status']='Submitting'; current['authorization']={'at':now(),'revision':p['revision'],'review':r}
        putjob(db,current); event(db,'submission_reserved',{'revision':p['revision']},jid)
    export(w)
    return {'allowed':True,'id':jid,'instruction':'Recheck live form and current permissions immediately before the one submit action; then record evidence.'}

def transition(w,jid,status,evidence,event_key=None,next_action=None):
    if status not in STATES: raise ValueError('Unknown status')
    if not evidence.strip(): raise ValueError('Evidence is required; never infer submission or rejection')
    with connect(w) as db:
        if event_key and db.execute('SELECT 1 FROM events WHERE event_key=?',(event_key,)).fetchone(): return {'duplicate_event':True}
        j=loadjob(db,jid)
        if status=='Submitting': raise ValueError('Use reserve with a reviewed application')
        if j['status']=='Submitting' and status in ('Discovered','Shortlisted','Preparing','Ready'):
            raise ValueError('Resolve uncertain submission first; do not silently retry')
        if j.get('submitted_at') and status in ('Discovered','Shortlisted','Preparing','Ready'):
            raise ValueError('Do not reset a previously submitted application')
        old=j['status']; j['status']=status; j['evidence']=evidence
        if status=='Submitted' and not j.get('submitted_at'): j['submitted_at']=now()
        if next_action is not None: j['next_action']=next_action
        putjob(db,j); event(db,'status_changed',{'from':old,'to':status,'evidence':evidence},jid,event_key)
    export(w)
    return {'id':jid,'status':status}

def safe_cell(v):
    if isinstance(v,(list,dict)): v=json.dumps(v,ensure_ascii=False)
    if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@','\t','\r')): return "'"+v
    return '' if v is None else v

def export(w):
    w=Path(w)
    with connect(w) as db: jobs=[json.loads(r[0]) for r in db.execute('SELECT data FROM jobs ORDER BY id')]
    dest=w/'exports'; dest.mkdir(exist_ok=True)
    fd,name=tempfile.mkstemp(dir=dest,prefix='.tracker-')
    with os.fdopen(fd,'w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f);writer.writerow(FIELDS)
        for j in jobs: writer.writerow([safe_cell(j.get(k)) for k in FIELDS])
    os.replace(name,dest/'applications.csv')
    write(dest/'applications.json',[{k:j.get(k) for k in FIELDS} for j in jobs])
    # Local privacy-preserving workbook input: never include profiles or demographics.
    return {'count':len(jobs),'csv':str(dest/'applications.csv'),'json':str(dest/'applications.json')}

def main():
    os.umask(0o077)
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--workspace',required=True)
    sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('init')
    p=sub.add_parser('import-profile');p.add_argument('file');p.add_argument('--evidence',required=True)
    p=sub.add_parser('add-job');p.add_argument('file')
    p=sub.add_parser('permissions');p.add_argument('file');p.add_argument('--evidence',required=True)
    p=sub.add_parser('reserve');p.add_argument('id');p.add_argument('review')
    p=sub.add_parser('status');p.add_argument('id');p.add_argument('status',choices=STATES);p.add_argument('--evidence',required=True);p.add_argument('--event-key');p.add_argument('--next-action')
    sub.add_parser('export')
    sub.add_parser('pause')
    args=ap.parse_args();w=Path(args.workspace).expanduser().resolve()
    if args.command!='init' and not (w/'profile.json').exists(): raise ValueError('Initialize a private workspace first')
    if args.command=='init': result=init(w)
    elif args.command=='import-profile': result=import_profile(w,args.file,args.evidence)
    elif args.command=='add-job': result=upsert(w,args.file)
    elif args.command=='permissions': result=update_permissions(w,args.file,args.evidence)
    elif args.command=='reserve': result=reserve(w,args.id,args.review)
    elif args.command=='status': result=transition(w,args.id,args.status,args.evidence,args.event_key,args.next_action)
    elif args.command=='pause':
        p=read(w/'permissions.json');p['paused']=True;p['revision']=now();write(w/'permissions.json',p);result={'paused':True}
    else: result=export(w)
    print(json.dumps(result,indent=2))
    if result.get('allowed') is False: sys.exit(2)

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,OSError,sqlite3.Error) as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr);sys.exit(1)
