// Run with the host's bundled Node and @oai/artifact-tool dependencies.
import fs from 'node:fs/promises';
import path from 'node:path';
import {FileBlob,SpreadsheetFile,Workbook} from '@oai/artifact-tool';
const workspace=process.argv[2];
if(!workspace) throw new Error('Usage: node export-workbook.mjs PRIVATE_WORKSPACE');
const file=path.join(workspace,'Application Tracker.xlsx');
const rows=JSON.parse(await fs.readFile(path.join(workspace,'exports/applications.json'),'utf8'));
const fields=['id','company','role','location','url','requisition','salary_min','salary_max','currency','pay_period','posted_at','first_seen','status','submitted_at','next_action','deadline','contact','resume','notes','skills_to_learn','evidence'];
let wb,t,existing=false;
try{await fs.access(file);existing=true;}catch{}
if(existing){wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));t=wb.worksheets.getItem('Tracker');if(JSON.stringify(t.getRange('A1:U1').values[0])!==JSON.stringify(fields))throw new Error('Tracker headers changed; reconcile manually instead of overwriting');}
else{wb=Workbook.create();t=wb.worksheets.add('Tracker');t.getRange('A1:U1').values=[fields];t.tables.add('A1:U2',true,'Applications');t.freezePanes.freezeRows(1);t.showGridLines=false;t.getRange('A1:U1').format.fill='#193c35';t.getRange('A1:U1').format.font={bold:true,color:'#ffffff'};t.getRange('A1:U2').format.columnWidth=22;t.getRange('A1:U2').format.wrapText=true;}
const clean=v=>{if(v==null)return null;if(typeof v==='object')return JSON.stringify(v);return typeof v==='string'&&/^[\s]*[=+\-@]/.test(v)?"'"+v:v;};
let ids=t.getUsedRange().values.map(r=>r[0]);
for(const job of rows){let i=ids.indexOf(job.id);const vals=fields.map(f=>clean(job[f]));
 if(i<0){const table=t.tables.getItem('Applications');if(ids.length===2&&!ids[1]){i=1;t.getRange('A2:U2').values=[vals];ids[1]=job.id;}else{table.rows.add(null,[vals]);i=ids.length;ids.push(job.id);}t.getRange(`A${i+1}:U${i+1}`).format.wrapText=true;t.getRange(`A${i+1}:U${i+1}`).format.rowHeight=64;}
 else{vals[18]=t.getRange(`S${i+1}`).values[0][0];t.getRange(`A${i+1}:U${i+1}`).values=[vals];}
}
wb.recalculate();
await(await SpreadsheetFile.exportXlsx(wb)).save(file);
console.log(JSON.stringify({file,jobs:rows.length,notes_preserved:true}));
