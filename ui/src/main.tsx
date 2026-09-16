import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import {ArrowDownToLine, BriefcaseBusiness, LockKeyhole, ArrowUpRight} from 'lucide-react';
import {Button} from './components/ui/button';
import {Card,CardHeader,CardTitle,CardDescription,CardContent} from './components/ui/card';
import {Input} from './components/ui/input';
import {Label} from './components/ui/label';
import {Textarea} from './components/ui/textarea';
import {Checkbox} from './components/ui/checkbox';
import {Badge} from './components/ui/badge';
import {spec,choices} from './fields';

const sections=['About you','Target roles','Eligibility & timing','Resume & experience','Permissions','Optional demographics'];
function Section({n,description,children}:{n:number,description?:string,children:React.ReactNode}){return <Card id={'section-'+n} className="shadow-sm"><CardHeader className="pb-6"><div className="flex items-center gap-3"><span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border text-xs text-muted-foreground">{String(n).padStart(2,'0')}</span><CardTitle className="text-xl tracking-tight">{sections[n-1]}</CardTitle></div>{description&&<CardDescription className="pt-2 leading-relaxed">{description}</CardDescription>}</CardHeader><CardContent>{children}</CardContent></Card>}
function App(){
 const [grants,setGrants]=useState<Record<string,boolean>>({});
 const [confirmed,setConfirmed]=useState(false);
 const [result,setResult]=useState('');
 const [resetKey,setResetKey]=useState(0);
 const count=choices.filter(([key])=>grants[key]).length;
 function fields(section:string){return <div className="grid gap-5 sm:grid-cols-2">{spec[section].map(([key,title,required,type])=><div className="space-y-2" key={key}><Label htmlFor={section+'_'+key}>{title}{required&&<span aria-hidden="true"> *</span>}</Label><Input id={section+'_'+key} name={section+'_'+key} required={!!required} type={type||'text'} min={key==='minimum_base'?0:undefined} defaultValue={key==='currency'?'USD':key==='pay_period'?'year':key==='daily_time'?'08:00':undefined}/></div>)}</div>}
 function submit(e:React.FormEvent<HTMLFormElement>){
  e.preventDefault(); const form=e.currentTarget;
  const value=(id:string)=>(form.elements.namedItem(id) as HTMLInputElement)?.value.trim()||'';
  const values=(section:string)=>Object.fromEntries(spec[section].map(([key])=>[key,value(section+'_'+key)]));
  if(!grants.save_profile){setResult('Select local profile storage to export a reusable setup, or ask your assistant for a one-time session without saved details.');return;}
  const demographics=Object.fromEntries(Object.entries(values('demographics')).filter(([,v])=>v));
  if(Object.keys(demographics).length&&!grants.save_demographics){setResult('Clear demographic answers or explicitly allow saving them.');return;}
  if(!confirmed){setResult('Review your answers and permissions before downloading.');return;}
  const array=(s:string)=>s.split(',').map(x=>x.trim()).filter(Boolean);
  const search:any=values('search');for(const k of ['roles','locations','work_modes','employment_types','seniority','excluded_companies'])search[k]=array(search[k]);
  search.minimum_base=search.minimum_base===''?null:Number(search.minimum_base);search.sources=['https://apmlist.com/','https://github.com/jobright-ai/2026-Product-Management-New-Grad'];
  const eligibility:any=values('eligibility');eligibility.languages=array(eligibility.languages);
  const data={profile:{version:1,confirmed_at:null,identity:values('identity'),eligibility,search,education:[],experience:[],projects:[],skills:[],confirmed_answers:{},experience_notes:value('experience_notes'),resume:{authoritative_source:'resumes/base.tex',page_limit:1,confirmed:false}},permissions:{grants:Object.fromEntries(choices.map(([k])=>[k,!!grants[k]])),max_submissions_per_day:Number(value('daily_limit'))},demographics,reviewed_by_user:true};
  const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='job-search-setup.private.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  setResult('Setup downloaded. Give this private file to your assistant, then provide your resume. No applications have been submitted.');
 }

 return <><header className="border-b bg-card"><div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-5 py-5 sm:px-8"><div className="flex items-center gap-2 text-sm font-semibold"><BriefcaseBusiness className="h-5 w-5 text-primary"/> Job Search Kit</div><Badge variant="secondary" className="gap-1.5"><LockKeyhole className="h-3 w-3"/> Local setup</Badge></div></header>
 <main className="mx-auto max-w-6xl px-5 py-10 sm:px-8 sm:py-14"><div className="mb-10 max-w-2xl"><p className="mb-4 text-xs font-semibold uppercase tracking-[.18em] text-primary">A little setup. A clearer search.</p><h1 className="text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">Your search.<br/>Your choices.</h1><p className="mt-5 leading-relaxed text-muted-foreground">Give your assistant the details it needs and the permissions you choose. You stay in control of every step.</p><p className="mt-4 text-xs leading-relaxed text-muted-foreground">Works offline. No network requests, browser storage or automatic uploads.</p></div>
 <div className="grid items-start gap-8 lg:grid-cols-[210px_1fr]"><aside className="min-w-0 lg:sticky lg:top-8"><nav aria-label="Setup sections" className="flex gap-2 overflow-x-auto pb-2 lg:flex-col">{sections.map((name,i)=><a key={name} href={'#section-'+(i+1)} className="flex shrink-0 items-center gap-3 rounded-md px-3 py-2.5 text-sm text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary"><span className="text-xs opacity-60">0{i+1}</span>{name}</a>)}</nav><div className="mt-6 hidden border-t pt-5 text-xs leading-relaxed text-muted-foreground lg:block">Made for your assistant.<br/>Your private details stay out of the plugin you share.<ArrowUpRight className="mt-3 h-4 w-4"/></div></aside>
 <form id="setup" key={resetKey} onSubmit={submit} onReset={()=>{setGrants({});setConfirmed(false);setResult('');setResetKey(k=>k+1);}} className="min-w-0 space-y-6">
 <Section n={1} description="Only your name and application email are required here. Leave passwords and identity-document numbers out of this form.">{fields('identity')}</Section>
 <Section n={2} description="Define what a good match looks like. Separate multiple answers with commas.">{fields('search')}</Section>
 <Section n={3} description="Use confirmed answers. Your current address and permanent residency may differ; an ID alone does not determine residency.">{fields('eligibility')}</Section>
 <Section n={4} description="After setup, give your original LaTeX resume to your assistant. A PDF or Word resume can also become a LaTeX draft for your review."><Label htmlFor="experience_notes">Additional experience, education, projects or skills</Label><Textarea className="mt-2 min-h-28" id="experience_notes" name="experience_notes" placeholder="Optional. Add details to discuss, including contributions, dates and metrics."/></Section>
 <Section n={5} description="All optional permissions start off. Changes apply to future actions; they cannot undo information already sent."><div className="mb-3 flex items-center justify-between"><Label>Your choices</Label><Badge variant="secondary">{count} of {choices.length} enabled</Badge></div><div id="permissions" className="divide-y">{choices.map(([key,title,desc])=><div key={key} className="flex gap-3 py-4"><Checkbox id={'permission_'+key} className="mt-0.5 shrink-0" checked={!!grants[key]} onCheckedChange={checked=>setGrants(g=>({...g,[key]:checked===true}))} aria-describedby={'help_'+key}/><div className="space-y-1"><Label htmlFor={'permission_'+key} className="cursor-pointer leading-snug">{title}</Label><p id={'help_'+key} className="text-sm leading-relaxed text-muted-foreground">{desc}</p></div></div>)}</div><div className="mt-5 space-y-2 rounded-lg bg-muted p-4"><Label htmlFor="daily_limit">Maximum application attempts per day (UTC)</Label><Input className="max-w-28 bg-card" id="daily_limit" name="daily_limit" type="number" min="1" max="50" defaultValue="3" required/><p className="text-xs leading-relaxed text-muted-foreground">Unfamiliar terms, factual certifications, payments and other commitments require separate review. Host app permissions still apply.</p></div></Section>
 <Section n={6} description="Entirely optional. Saving and sending are separate permissions. Your exact answers stay out of your resume and tracker; “Prefer not to disclose” is different from leaving a field blank.">{fields('demographics')}</Section>
 <Card className="border-primary/30 bg-card"><CardHeader><CardTitle className="text-xl">Ready when you are.</CardTitle><CardDescription>Download your setup, then give the private file and your resume to your assistant.</CardDescription></CardHeader><CardContent className="space-y-5"><div className="flex gap-3"><Checkbox id="confirmed" checked={confirmed} onCheckedChange={v=>setConfirmed(v===true)} required className="mt-0.5"/><div><Label htmlFor="confirmed" className="cursor-pointer">I reviewed these answers and permissions.</Label><p className="mt-1 text-xs leading-relaxed text-muted-foreground">This file contains personal information. Share only the plugin package with others.</p></div></div><div className="flex flex-wrap gap-3"><Button type="submit"><ArrowDownToLine/>Download my setup</Button><Button variant="outline" type="reset">Clear form</Button></div><p id="result" role="status" aria-live="polite" className="text-sm font-medium leading-relaxed">{result}</p></CardContent></Card>
 <footer className="pb-8 text-xs leading-relaxed text-muted-foreground">Installation does not start applications or a background schedule. Your assistant will verify browser, email, spreadsheet and scheduling access separately.</footer>
 </form></div></main></>;
}
createRoot(document.getElementById('root')!).render(<App/>);
