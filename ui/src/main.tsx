import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Button} from './components/ui/button';
import {Input} from './components/ui/input';
import {Label} from './components/ui/label';
import {Textarea} from './components/ui/textarea';
import {Checkbox} from './components/ui/checkbox';
import {spec,choices} from './fields';
import {ResumeIntake, type ResumeFacts} from './ResumeIntake';

const steps = ['Past chats','Contact details','Job preferences','Availability','Experience','Permissions','Optional disclosures','Review and save'];
const sections: Record<string, number> = {identity:1, search:2, eligibility:3, demographics:6};
const list = (s:string)=>s.split(',').map(item=>item.trim()).filter(Boolean);
const paragraphs = (s:string)=>s.trim() ? [s.trim()] : [];
const headingStyle = 'text-2xl font-semibold';
const historyKey = 'read_chat_history';

function App() {
  const [facts,setFacts] = useState<ResumeFacts|null>(null);
  const [step,setStep] = useState(0);
  const [history,setHistory] = useState('skip');
  const [grants,setGrants] = useState<Record<string,boolean>>({});
  const [confirmed,setConfirmed] = useState(false);
  const [message,setMessage] = useState('');
  const form = useRef<HTMLFormElement>(null);
  const title = useRef<HTMLHeadingElement>(null);
  useEffect(()=>{ if(facts) title.current?.focus(); },[step,facts]);

  function validStep(index:number) {
    const inputs=form.current?.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>(`[data-step="${index}"] input, [data-step="${index}"] textarea`);
    for (const field of Array.from(inputs || [])) {
      if (!field.validity.valid) {
        const details=field.closest('details');
        if (details) details.open=true;
        field.reportValidity(); return false;
      }
    }
    return true;
  }
  function go(next:number) {
    if (next>step && !validStep(step)) return;
    setConfirmed(false);
    setMessage(''); setStep(next); window.scrollTo(0,0);
  }
  function save() {
    if (!facts || !form.current) return;
    const value=(key:string)=>(form.current!.elements.namedItem(key) as HTMLInputElement | null)?.value.trim() || '';
    const values=(section:string)=>Object.fromEntries(spec[section].map(([key])=>[key,value(section+'_'+key)]));
    if (!grants.save_profile) { setStep(5); setMessage('Select local profile storage to download a reusable setup. You can also keep working in your chat.'); return; }
    const demographics=Object.fromEntries(Object.entries(values('demographics')).filter(([,v])=>v));
    if (Object.keys(demographics).length && !grants.save_demographics) { setStep(6);setMessage('Clear demographic answers or allow saving them in Permissions.');return; }
    if (!confirmed) { setMessage('Review your choices and confirm before downloading.');return; }
    const search:any=values('search');
    for(const key of ['roles','locations','work_modes','employment_types','seniority','excluded_companies']) search[key]=list(search[key]);
    for(const key of ['minimum_base','preferred_base']) search[key]=search[key]===''?null:Number(search[key]);
    search.sources=[];
    const eligibility:any=values('eligibility');
    eligibility.languages=list(eligibility.languages);
    const profile={version:1,confirmed_at:null,identity:values('identity'),eligibility,search,
      education:paragraphs(facts.education),experience:paragraphs(facts.experience),projects:paragraphs(facts.projects),
      skills:paragraphs(facts.skills),certifications:paragraphs(facts.certifications),confirmed_answers:{},
      resume_review:{confirmed:true,other:facts.other},experience_notes:value('experience_notes'),
      scope_notes:{computer:value('computer_scope'),address:value('address_scope'),history:history==='selected'?value('history_scope'):''},
      history_choice:history,resume:{authoritative_source:'resumes/base.tex',page_limit:1,confirmed:false}};
    const allGrants=Object.fromEntries(choices.map(([key])=>[key,key===historyKey?history==='selected':!!grants[key]]));
    const data={profile,permissions:{grants:allGrants,max_submissions_per_day:Number(value('daily_limit'))},demographics,reviewed_by_user:true};
    const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
    const link=document.createElement('a');link.href=url;link.download='job-search-setup.private.json';link.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
    setMessage('Setup downloaded. Give this private file to your assistant so it can use the facts and permissions you reviewed.');
  }
  const base:Record<string,string>={...facts,currency:'USD',pay_period:'year',daily_time:'08:00'};
  function renderField(section:string, field:(string|boolean)[]) {
    const key=String(field[0]), label=String(field[1]), required=!!field[2], type=String(field[3]||'text');
    const id=section+'_'+key;
    return <div key={key} className="space-y-1"><Label htmlFor={id}>{label}{required?' *':''}</Label>
      <Input id={id} name={id} required={!!required} type={type||'text'} min={type==='number'?0:undefined} defaultValue={base[key]||''}/></div>;
  }
  function summaryValue(id:string) {
    return (form.current?.elements.namedItem(id) as HTMLInputElement|null)?.value.trim() || 'Left open';
  }
  return <><header className="border-b bg-card px-5 py-4 text-sm font-semibold">#LOCKEDIN Job Kit</header>
    {!facts ? <ResumeIntake onConfirm={data=>{setFacts(data);setStep(0);}}/> :
    <main className="mx-auto max-w-3xl space-y-5 px-5 py-8">
      <p className="text-sm text-muted-foreground">Setup · Step {step+1} of {steps.length}</p>
      <h1 className={headingStyle} tabIndex={-1} ref={title}>{steps[step]}</h1>
      <form ref={form} noValidate onSubmit={event=>{event.preventDefault();if(step<steps.length-1)go(step+1);else save();}} className="space-y-6">
        <section data-step="0" hidden={step!==0}>
          <p>Would you like your assistant to use an earlier conversation to learn about a project, achievement or job preference?</p>
          <fieldset className="mt-4 space-y-3"><legend className="sr-only">Choose how to use past chats</legend>
          {([['skip','Continue with my résumé only'],['excerpt','I’ll paste a relevant excerpt in my private chat'],['selected','Allow my assistant to read specific chats for this setup']] as const).map(([id,label])=>
            <label className="flex items-start gap-2" key={id}><input type="radio" name="history_mode" value={id} checked={history===id} onChange={()=>setHistory(id)}/>{label}</label>)}
          </fieldset>
          {history==='selected' && <div className="mt-5 space-y-2"><Label htmlFor="history_scope">Which app and conversations may it read?</Label><Textarea id="history_scope" name="history_scope" required placeholder="For example, only the project retrospective conversation I select in Claude."/><p className="text-sm">Your assistant will check what it can access and show proposed facts for your approval. This page does not open chats.</p></div>}
          {history==='excerpt' && <p className="mt-4 text-sm">Keep only the relevant lines. Your assistant can ask what to add after you paste the excerpt. This choice grants no history access.</p>}
        </section>
        {Object.entries(sections).map(([section,index])=>
          <section data-step={index} hidden={step!==index} key={section}>
            <p className="mb-4">{({identity:'Your confirmed details are filled in. Add missing information you want to reuse. A city on a résumé may differ from a permanent address.',search:'Which roles should the assistant look for? Separate firm limits from preferences. Leave an undecided answer blank.',eligibility:'Fill what applies to your search. You can leave a question open and return later.',demographics:'You can skip every field here. Saving answers privately and sharing them with employers are separate choices.'})[section]}</p>
            <div className="grid gap-4 sm:grid-cols-2">{spec[section].filter(([key])=>!facts[key]).map(field=>renderField(section,field))}</div>
            {spec[section].some(([key])=>facts[key]) && <details className="mt-5"><summary className="cursor-pointer font-medium">Review details already filled from my résumé</summary>
              <div className="mt-4 grid gap-4 sm:grid-cols-2">{spec[section].filter(([key])=>facts[key]).map(field=>renderField(section,field))}</div></details>}
          </section>)}
        <section data-step="4" hidden={step!==4}><Label htmlFor="experience_notes">What would a résumé reader miss?</Label><p className="my-2">Think of something from work, school, a club or your life outside work. Who needed help? What did you personally change? What evidence could you share?</p><Textarea id="experience_notes" name="experience_notes"/></section>
        <section data-step="5" hidden={step!==5}><p>Select the tasks you want help with. Your assistant will check the relevant app settings separately.</p>
          <div id="permissions" className="divide-y">{choices.filter(([key])=>key!==historyKey).map(([key,label,help])=>
            <div className="flex gap-3 py-3" key={key}><Checkbox id={'permission_'+key} checked={!!grants[key]} onCheckedChange={v=>setGrants(prev=>({...prev,[key]:v===true}))} aria-describedby={'help_'+key}/><div><Label htmlFor={'permission_'+key}>{label}</Label><p id={'help_'+key} className="text-sm text-muted-foreground">{help}</p></div></div>)}</div>
          {grants.use_computer && <div className="my-4 space-y-2"><Label htmlFor="computer_scope">Which employer sites and tasks?</Label><Textarea id="computer_scope" name="computer_scope" required placeholder="For example, prepare forms for employers matching my search until the review screen."/></div>}
          {grants.share_address && <div className="my-4 space-y-2"><Label htmlFor="address_scope">Which address, for which employers and when?</Label><Textarea id="address_scope" name="address_scope" required/></div>}
          <Label htmlFor="daily_limit">Maximum application attempts per day in your selected time zone</Label><Input name="daily_limit" id="daily_limit" type="number" min="1" max="50" defaultValue="3" required/>
        </section>
        <section data-step="7" hidden={step!==7} className="space-y-4">
          <p>Check your search summary before saving it to your private folder.</p>
          {step===7 && <dl className="divide-y">{[
            ['Application email','identity_application_email',1],['Target roles','search_roles',2],['Locations','search_locations',2],
            ['Minimum base pay','search_minimum_base',2],['Preferred base pay','search_preferred_base',2],
            ['Relocation','eligibility_relocation',3],['Earliest start','eligibility_earliest_start',3]
          ].map(([label,id,target])=><div key={id} className="flex items-center justify-between gap-3 py-2"><div><dt className="text-sm text-muted-foreground">{label}</dt><dd>{summaryValue(String(id))}
             {String(id).endsWith('_base') && summaryValue(String(id))!=='Left open' && ' '+summaryValue('search_currency')+' / '+summaryValue('search_pay_period')}</dd></div>
             <Button type="button" variant="ghost" aria-label={'Edit '+label} onClick={()=>go(Number(target))}>Edit</Button></div>)}</dl>}
          <ul className="list-disc pl-6"><li>Past chats: {history==='skip'?'skipped':history==='excerpt'?'only excerpts you choose to paste':'only the named conversations for this setup'}</li>{choices.filter(([key])=>key!==historyKey && grants[key]).map(([key,label])=><li key={key}>{label}</li>)}</ul>
          <div className="flex gap-2"><Checkbox id="confirmed" checked={confirmed} onCheckedChange={v=>setConfirmed(v===true)}/><Label htmlFor="confirmed">I reviewed these answers and permissions.</Label></div>
        </section>
        <div className="flex flex-wrap gap-2">
          {step>0 && <Button variant="outline" type="button" onClick={()=>go(step-1)}>Back</Button>}
          <Button type="submit">{step===7?'Download my setup':'Continue'}</Button>
          {step===7 && <Button type="button" variant="outline" onClick={()=>{setFacts(null);setGrants({});setHistory('skip');setConfirmed(false);setStep(0);setMessage('');}}>Clear form</Button>}
        </div>
        <p id="result" role="status" className="text-sm">{message}</p>
      </form>
    </main>}
  </>;
}
createRoot(document.getElementById('root')!).render(<App/>);
