import React, {useEffect, useRef, useState} from 'react';
import {Button} from './components/ui/button';
import {Input} from './components/ui/input';
import {Label} from './components/ui/label';
import {Textarea} from './components/ui/textarea';

const labels = {
  name: 'Name on résumé', application_email: 'Email', phone: 'Phone',
  linkedin: 'LinkedIn', github: 'GitHub', portfolio: 'Portfolio or website',
  education: 'Education', experience: 'Work and leadership', projects: 'Projects',
  skills: 'Skills', certifications: 'Certifications', languages: 'Languages',
  other: 'Other résumé details to review'
};
type Field = keyof typeof labels;
export type ResumeFacts = Record<Field, string>;
const groups: Record<string, Field> = {
  education:'education', academicbackground:'education', experience:'experience',
  workexperience:'experience', professionalexperience:'experience', employment:'experience',
  leadership:'experience', volunteerexperience:'experience', volunteering:'experience',
  projects:'projects', personalprojects:'projects', academicprojects:'projects',
  skills:'skills', technicalskills:'skills', certifications:'certifications', licenses:'certifications',
  languages:'languages'
};
const shortFields: Field[] = ['name','application_email','phone','linkedin','github','portfolio'];

// Keep source wording. The user corrects every proposed field before it becomes profile data.
function readResume(source: string): ResumeFacts {
  const facts = Object.fromEntries(Object.keys(labels).map(key=>[key,''])) as ResumeFacts;
  const lines = source.split(/\r?\n/).map(line=>line.trim()).filter(Boolean);
  const first = lines[0] || '';
  if (/^[\p{L}][\p{L} .'’\-]{1,65}$/u.test(first) && first.split(/\s+/).length <= 5 &&
      !groups[first.toLowerCase().replace(/\s+/g,'')]) facts.name = first;
  facts.application_email = source.match(/[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}/)?.[0] || '';
  facts.phone = source.match(/(?:\+\d{1,3}[ .-]?)?(?:\(\d{3}\)|\b\d{3})[ .-]\d{3}[ .-]\d{4}\b/)?.[0] || '';
  facts.linkedin = source.match(/(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[\w%./-]+/i)?.[0] || '';
  facts.github = source.match(/(?:https?:\/\/)?(?:www\.)?github\.com\/[\w.-]+/i)?.[0] || '';
  facts.portfolio = source.match(/(?:portfolio|website)\s*:\s*(https?:\/\/\S+)/i)?.[1] || '';
  let group: Field = 'other';
  for (const line of lines) {
    if (shortFields.some(key=>facts[key]===line)) continue;
    const [heading, ...rest] = line.split(':');
    const found = groups[heading.toLowerCase().replace(/\s+/g,'')];
    if (found) {
      group = found;
      if (rest.join(':').trim()) facts[group] += rest.join(':').trim()+'\n';
    } else {
      facts[group] += line+'\n';
    }
  }
  for (const key of Object.keys(labels) as Field[]) facts[key] = facts[key].trim();
  return facts;
}

export function ResumeIntake({onConfirm}:{onConfirm:(facts:ResumeFacts)=>void}) {
  const [source,setSource] = useState('');
  const [draft,setDraft] = useState<ResumeFacts|null>(null);
  const [error,setError] = useState('');
  const [reviewKeys,setReviewKeys] = useState<Field[]>([]);
  const title = useRef<HTMLHeadingElement>(null);
  const reviewing = draft !== null;
  useEffect(()=>{ if (reviewing) title.current?.focus(); },[reviewing]);
  function review() {
    if (!source.trim()) { setError('Paste some résumé text, choose a text file, or write a short work history.'); return; }
    const proposed=readResume(source);
    setReviewKeys((Object.keys(labels) as Field[]).filter(key=>proposed[key]));
    setError(''); setDraft(proposed); window.scrollTo(0,0);
  }
  return <section className="mx-auto max-w-3xl space-y-5 px-5 py-10" aria-labelledby="intake-title">
    <h1 ref={title} tabIndex={-1} id="intake-title" className="text-3xl font-semibold">{draft?'Check what we found':'Start with your résumé'}</h1>
    {draft ? <>
      <p>Compare these details with your original. Edit or remove anything you would prefer to leave out. You can fill missing details later.</p>
      <details><summary className="cursor-pointer">Compare with the text I provided</summary><pre className="mt-2 whitespace-pre-wrap break-words text-sm">{source}</pre></details>
      {reviewKeys.map(key=>
        <div key={key} className="space-y-1">
          <Label htmlFor={'review_'+key}>{labels[key]}</Label>
          {shortFields.includes(key) ?
            <Input id={'review_'+key} value={draft[key]} onChange={e=>setDraft({...draft,[key]:e.target.value})}/> :
            <Textarea id={'review_'+key} value={draft[key]} onChange={e=>setDraft({...draft,[key]:e.target.value})}/>}
        </div>)}
      <div className="flex flex-wrap gap-3">
        <Button variant="outline" onClick={()=>setDraft(null)}>Back to résumé</Button>
        <Button onClick={()=>onConfirm(draft)}>Confirm these facts and continue</Button>
      </div>
    </> : <>
      <p>Paste your résumé, or choose a text file. If you have a PDF or Word document, copy its text here or attach the document to your assistant. A short work history works too.</p>
      <Label htmlFor="resume_source">Résumé text or work history</Label>
      <Textarea id="resume_source" className="min-h-40" value={source} onChange={e=>setSource(e.target.value)}/>
      <Label htmlFor="resume_file">Or choose a .txt file</Label>
      <Input id="resume_file" type="file" accept=".txt,text/plain" onChange={async e=>{
        const file=e.target.files?.[0]; if (!file) return;
        try { const contents=await file.text(); setSource(contents); setError(''); }
        catch { setError('This file could not be read. Paste the text instead.'); }
      }}/>
      <Button onClick={review}>Review résumé facts</Button>
      <p role="alert">{error}</p>
      <p className="text-sm text-muted-foreground">This page works offline. Your answers stay in this tab until you download them.</p>
    </>}
  </section>;
}
