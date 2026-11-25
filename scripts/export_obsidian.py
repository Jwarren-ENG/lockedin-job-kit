#!/usr/bin/env python3
"""Generate a private Obsidian dashboard, board and interview calendar. No network."""
import argparse
import calendar
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import jobkit

START='<!-- jobkit:managed:start -->'
END='<!-- jobkit:managed:end -->'

def plain(value):
    return re.sub(r'[\[\]<>|\r\n`#*\\]', ' ', str(value or '')).strip()

def managed(path, body):
    path.parent.mkdir(parents=True,exist_ok=True)
    block=START+'\n'+body+'\n'+END
    if path.exists():
        old=path.read_text()
        if START not in old or END not in old:
            raise ValueError('Refusing to replace an unmanaged note: '+path.name)
        before,rest=old.split(START,1)
        _,after=rest.split(END,1)
        path.write_text(before+block+after)
    else:
        path.write_text(block+'\n\n## My notes\n\n')

def stamp(value):
    t=datetime.fromisoformat(value.replace('Z','+00:00'))
    if t.tzinfo is None: raise ValueError('Interview timestamps must include a UTC offset')
    return t

def ics_text(value):
    return str(value).replace('\\','\\\\').replace('\n','\\n').replace(';','\\;').replace(',','\\,').replace('\r','')

def export(workspace):
    w=Path(workspace).expanduser().resolve()
    if not (w/'profile.json').is_file(): raise ValueError('Initialize the private workspace first')
    if w==jobkit.ROOT or jobkit.ROOT in w.parents: raise ValueError('Vault must remain outside the plugin')
    grants = jobkit.read(w/'permissions.json')['grants']
    if not grants.get('obsidian_export'):
        raise ValueError('Obsidian export is off. Enable it in your job search permissions first.')
    v=w/'obsidian'; v.mkdir(exist_ok=True)
    with jobkit.connect(w) as db:
        jobs=[json.loads(r[0]) for r in db.execute('SELECT data FROM jobs ORDER BY id')]
    meetings={}
    for p in sorted((w/'interviews').glob('*.json')):
        m=json.loads(p.read_text())
        if m.get('status')!='Scheduled': continue
        if not re.fullmatch(r'[A-Za-z0-9_-]+',m['id']): raise ValueError('Use a stable alphanumeric interview ID')
        start,end=stamp(m['start']),stamp(m['end'])
        if end<=start: raise ValueError('Interview end must follow start')
        if m['id'] in meetings: raise ValueError('Duplicate interview ID; update its existing file')
        meetings[m['id']]=(m,start,end)
    upcoming=[x for x in meetings.values() if x[2]>=datetime.now(timezone.utc)]
    upcoming.sort(key=lambda x:x[1])
    board=['---','kanban-plugin: board','---','','# Applications','']
    for status in jobkit.STATES:
        board+=['## '+status,'']
        for j in jobs:
            if j['status']==status:
                board+=['- [ ] [[Applications/'+j['id']+'|'+plain(j['company'])+' — '+plain(j['role'])+']]']
        board+=['']
    # Regenerated board: user edits belong in each application note, never this view.
    (v/'Application Board.md').write_text('\n'.join(board))
    for j in jobs:
        managed(v/'Applications'/ (j['id']+'.md'), '\n'.join([
            '# '+plain(j['company'])+' — '+plain(j['role']),
            '**Status:** '+plain(j['status']), '**Location:** '+plain(j.get('location')),
            '**Next action:** '+plain(j.get('next_action')),
            '**Posting:** <'+jobkit.canonical(j['url']).replace('>','%3E').replace('<','%3C')+'>',
            '**Skills to practice:** '+plain(', '.join(j.get('skills_to_learn') or []))]))
    home=['# Job Search','',f'{len(jobs)} roles · {sum(bool(j.get("submitted_at")) for j in jobs)} submitted · {len(upcoming)} upcoming interviews','',
          '[[Application Board|Applications board]] · [[Calendar|Calendar]]','','## Upcoming interviews','']
    events=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Job Search Kit//Interviews//EN','CALSCALE:GREGORIAN']
    months={}
    for m,start,end in upcoming:
        title=plain(m.get('company'))+' — '+plain(m.get('role'))
        note='Interviews/'+m['id']
        home+=['- '+start.strftime('%b %d, %Y %H:%M %z')+' [['+note+'|'+title+']]']
        managed(v/(note+'.md'),'# '+title+'\n\n'+start.isoformat()+' to '+end.isoformat()+'\n\nFormat: '+plain(m.get('format')))
        months.setdefault((start.year,start.month),{}).setdefault(start.day,[]).append('[['+note+'|'+title+']]')
        events+=['BEGIN:VEVENT','UID:'+m['id']+'@job-search-kit.local','DTSTAMP:'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
                 'DTSTART:'+start.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
                 'DTEND:'+end.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ'),
                 'SUMMARY:'+ics_text(title),'END:VEVENT']
    if not upcoming: home+=['No upcoming interviews recorded.']
    managed(v/'Home.md','\n'.join(home))
    cal=['# Calendar','','Times follow the UTC offset recorded on each confirmed interview.','']
    if not months:
        today=datetime.now();months[(today.year,today.month)]={}
    for (year,month),days in sorted(months.items()):
        cal+=['## '+calendar.month_name[month]+' '+str(year),'','| Mon | Tue | Wed | Thu | Fri | Sat | Sun |','|---|---|---|---|---|---|---|']
        for week in calendar.monthcalendar(year,month):
            cal+=['| '+' | '.join('' if not day else str(day)+(' <br> '+' <br> '.join(days[day]) if day in days else '') for day in week)+' |']
        cal+=['']
    managed(v/'Calendar.md','\n'.join(cal))
    events+=['END:VCALENDAR']
    # Fold UTF-8 lines to RFC 5545's 75-octet recommendation.
    folded=[]
    for line in events:
        chunk=''
        for char in line:
            if len((chunk+char).encode())>75: folded.append(chunk);chunk=' '
            chunk+=char
        folded.append(chunk)
    (v/'Interviews.ics').write_bytes(('\r\n'.join(folded)+'\r\n').encode())
    return {'vault':str(v),'roles':len(jobs),'upcoming_interviews':len(upcoming)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True)
    print(json.dumps(export(p.parse_args().workspace),indent=2))
