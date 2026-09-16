import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const w=await fs.mkdtemp(path.join(os.tmpdir(),'jobkit-workbook-'));
try{
 await fs.mkdir(path.join(w,'exports'));
 const data=[{id:'one',company:'Example A',role:'Analyst',status:'Submitted',salary_min:100000,notes:'Initial note'},{id:'two',company:'Example B',role:'Associate',status:'Ready'}];
 const input=path.join(w,'exports/applications.json'),file=path.join(w,'Application Tracker.xlsx');
 const script=new URL('../scripts/export-workbook.mjs',import.meta.url).pathname;
 await fs.writeFile(input,JSON.stringify(data));execFileSync(process.execPath,[script,w]);
 let wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));let t=wb.worksheets.getItem('Tracker');
 assert.equal(t.getRange('A2').values[0][0],'one');assert.equal(t.getRange('A3').values[0][0],'two');
 t.getRange('S2').values=[['User note keep me']];wb.worksheets.add('Personal notes').getRange('A1').values=[['Keep this tab']];
 await(await SpreadsheetFile.exportXlsx(wb)).save(file);
 data[0].status='Interview';data[0].notes='Overwrite attempt';data.push({id:'three',company:'Example C',role:'=HYPERLINK("bad")',status:'Discovered'});
 await fs.writeFile(input,JSON.stringify(data));execFileSync(process.execPath,[script,w]);
 wb=await SpreadsheetFile.importXlsx(await FileBlob.load(file));t=wb.worksheets.getItem('Tracker');
 assert.equal(t.getRange('M2').values[0][0],'Interview');assert.equal(t.getRange('S2').values[0][0],'User note keep me');
 assert.equal(t.getRange('A4').values[0][0],'three');assert.equal(wb.worksheets.getItem('Personal notes').getRange('A1').values[0][0],'Keep this tab');
 assert.ok(!t.getRange('C4').formulas[0][0]);
 if(process.env.TRACKER_SCREENSHOT){const img=await wb.render({sheetName:'Tracker',range:'A1:D4',scale:1.5});await fs.writeFile(process.env.TRACKER_SCREENSHOT,new Uint8Array(await img.arrayBuffer()));}
 console.log('PASS: workbook creation, append, status update, existing user notes/other tabs preserved, formula text not executed');
}finally{await fs.rm(w,{recursive:true,force:true});}
