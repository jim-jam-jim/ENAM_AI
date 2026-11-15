'use client';
import {useEffect,useState,useRef} from 'react';
import {api,displayDate} from './client';
export default function ResearchView({initial='INFY'}:{initial?:string}){
 const [symbol,setSymbol]=useState(initial),[active,setActive]=useState(initial),[data,setData]=useState<any>(null),[question,setQuestion]=useState('Is growth supported by cash generation?'),[answer,setAnswer]=useState<any>(null),[error,setError]=useState(''),[status,setStatus]=useState(''),[busy,setBusy]=useState(false),[passage,setPassage]=useState<any>(null);
 const [reload,setReload]=useState(0); const alive=useRef(true);useEffect(()=>()=>{alive.current=false},[]);
 async function load(t=active){const value=await api('/companies/'+encodeURIComponent(t));setData(value);return value}
 useEffect(()=>{alive.current=true;let current=true;setError('');setData(null);setBusy(true);setStatus('Loading company sources…');api('/companies/'+encodeURIComponent(active)).then(value=>{if(current)setData(value)}).catch(e=>{if(current)setError(e.message)}).finally(()=>{if(current){setBusy(false);setStatus('')}});return()=>{current=false}},[active,reload]);
 async function action(fn:()=>Promise<void>){setBusy(true);setError('');try{await fn()}catch(e){setError((e as Error).message)}finally{setBusy(false);setStatus('')}}
 async function prepare(){
  setStatus('Discovering primary documents…');await api('/companies/'+active+'/discover','POST');let value=await load();
  for(const doc of value.documents){
   let state=doc;
   while(alive.current&&!['complete','identity_review'].includes(state.phase)&&!(state.phase==='failed'&&state.attempts>=3)){
    setStatus(`${state.kind.replace('_',' ')} · ${state.completed_pages||0}${state.page_count?' / '+state.page_count:''} pages saved`);
    state=await api('/documents/'+doc.id+'/advance','POST');await load();
    if(state.phase==='busy')throw new Error('Another document job is running or recovering. Saved progress is safe; retry shortly.');if(state.phase==='failed')throw new Error('Document processing failed: '+(state.http_status?'HTTP '+state.http_status:state.error)+'. Retry to resume.');
   }
  }
 }
 return <section><h1>Company research</h1><p className="muted">Annual reports and earnings calls. Inspect the evidence behind each answer.</p>
 <form className="research-form" onSubmit={e=>{e.preventDefault();setError('');setAnswer(null);setPassage(null);setActive(symbol.trim().toUpperCase());setReload(v=>v+1)}}><label>NSE symbol<input value={symbol} onChange={e=>setSymbol(e.target.value)} maxLength={20} required/></label><button className="primary" disabled={busy}>{busy?'Working…':'Open company'}</button></form>
 <p className="muted">Prepared companies: INFY, DABUR, HCLTECH. Other NSE symbols use the same discovery pipeline where sources are available.</p>
 {error&&<p className="error" role="alert">{error}</p>}{status&&<p role="status">{status}</p>}
 {data&&<><h2>{active}</h2><details className="routine"><summary>Source coverage · {data.readiness?.ready_count||0} ready</summary>
 {data.documents.map((d:any)=><div className="document-row" key={d.id}><strong>{d.kind.replace('_',' ')}</strong><span>{d.phase.replace('_',' ')} · {d.completed_pages||0}{d.page_count?' / '+d.page_count:''} pages</span><span>Fetched {displayDate(d.fetched_at)}{d.http_status?' · HTTP '+d.http_status:''}</span><a href={d.url} target="_blank" rel="noreferrer">Original document</a>{d.phase==='identity_review'&&<span>Company/type needs review; excluded from research.</span>}</div>)}
 {!data.documents.length&&<p>No documents discovered yet.</p>}<button disabled={busy} className="primary" onClick={()=>action(prepare)}>Find / resume documents</button><p className="muted">Processing pauses when you leave. Saved pages resume on your next request. Large reports can take several minutes.</p></details>
 <p className="availability">{data.readiness?.message}</p><label className="question-label">Your question<textarea value={question} onChange={e=>setQuestion(e.target.value)} minLength={8} maxLength={600} rows={3}/></label>
 <div className="actions"><button className="primary" disabled={busy||question.trim().length<8||!data.research_available||!data.readiness?.ready} onClick={()=>action(async()=>{setStatus('Reading selected evidence…');setAnswer(await api('/companies/'+active+'/research','POST',{question}));setPassage(null)})}>{busy?'Working…':'Research question'}</button><button disabled={busy||question.trim().length<8} onClick={()=>action(async()=>{await api('/companies/'+active+'/question','PUT',{question});await load()})}>Save question</button></div>
 {!data.research_available&&<p className="availability">Research unavailable: runtime model access needs configuration.</p>}
 {data.saved_question&&<section className="saved"><h2>Watching</h2><p>{data.saved_question.question}</p><span className="muted">Saved {displayDate(data.saved_question.saved_at)} · This browser’s workspace</span><p className="muted">{data.monitoring_note}</p>{data.subsequent_events.length?data.subsequent_events.map((e:any)=><div key={e.id}><a href={e.source_url} target="_blank" rel="noreferrer">{e.title} · {displayDate(e.published_at)}</a><p className="muted">New disclosure · relevance not yet assessed</p><button disabled={busy} onClick={()=>action(async()=>{let result=await api('/companies/'+active+'/monitor/'+e.id,'POST');if(result.phase==='needs_document'){let d=result.document;while(alive.current&&!['complete','failed','identity_review','busy'].includes(d.phase)){setStatus('Processing subsequent evidence…');d=await api('/documents/'+d.id+'/advance','POST')}result=await api('/companies/'+active+'/monitor/'+e.id,'POST')}if(result.answer)setAnswer(result.answer)})}>Assess against saved question</button></div>):<p>No later disclosures in available coverage yet.</p>}</section>}
 {answer&&<section className="answer"><h2>Evidence review</h2><p className="muted">{answer.model} · {answer.cached?'Cached answer':'Generated'} {displayDate(answer.created_at)}</p><p className="verdict">{answer.verdict}</p>{answer.claims.map((c:any,i:number)=><article key={i}><span className="eyebrow">{c.kind==='reported'?'Reported fact':'Interpretation'}</span><p>{c.text}</p><blockquote>{c.quote}</blockquote><button onClick={()=>action(async()=>setPassage(await api('/passages/'+c.source_id)))}>Inspect supporting passage</button></article>)}<p className="availability">{answer.limitations}</p><p className="muted">{answer.citation_check}</p></section>}
 {passage&&<article className="evidence"><h2>Supporting passage · page {passage.page}</h2><a href={passage.url+'#page='+passage.page} target="_blank" rel="noreferrer">Open original document</a><pre tabIndex={0}>{passage.text}</pre><button onClick={()=>setPassage(null)}>Close passage</button></article>}
 </>}
 </section>
}
