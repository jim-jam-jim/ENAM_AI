export async function api<T=any>(path:string,method='GET',body?:unknown):Promise<T>{
 let workspace=localStorage.getItem('finn-workspace');
 if(!workspace){workspace=crypto.randomUUID();localStorage.setItem('finn-workspace',workspace)}
 const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),90000);
 try{
  const response=await fetch('/api'+path,{method,signal:controller.signal,headers:{'Content-Type':'application/json','X-Finn-Workspace':workspace},body:body===undefined?undefined:JSON.stringify(body)});
  const data=await response.json();if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:'Request unavailable. Please retry.');return data;
 }catch(e){if((e as Error).name==='AbortError')throw new Error('Request timed out. Saved checkpoints remain; retry to resume.');throw e}finally{clearTimeout(timeout)}
}
export const displayDate=(value?:string)=>value?new Date(value).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric',timeZone:'Asia/Kolkata'}):'Not fetched';
