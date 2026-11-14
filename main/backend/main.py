from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone
import json, os
from .database import connect, init_db
from .config import ROOT, OUTPUT_DIR
from engines.registry import all_status
from ai.director import make_plan
from ai.ltx.client import LTXClient, LTXError
app=FastAPI(title="NUBI VIDEO AI STUDIO API",version="0.1.0",description="MVP modular: projetos, plano de cenas, status de engines e submissões LTX API v2.")
app.add_middleware(CORSMiddleware,allow_origins=["http://127.0.0.1:8000","http://localhost:8000"],allow_methods=["GET","POST","PATCH","DELETE"],allow_headers=["*"])
init_db()
class ProjectIn(BaseModel):
 title:str=Field(min_length=1,max_length=160); topic:str=""; language:str="pt-BR"; duration:int=Field(default=60,ge=5,le=600); aspect_ratio:str="16:9"; resolution:str="1280x720"; fps:int=Field(default=24,ge=1,le=60); style:str="cinematic"
class LTXIn(BaseModel):
 prompt:str=Field(min_length=1,max_length=5000); model:str="ltx-2-5-fast"; duration:int=Field(default=5,ge=1,le=20); resolution:str="1280x720"; fps:int=24; generate_audio:bool=True; camera_motion:str|None=None; project_id:str|None=None
@app.get('/api/health')
def health():return {"status":"ok","version":"0.1.0","database":"connected","time":datetime.now(timezone.utc).isoformat()}
@app.get('/api/summary')
def summary():
 with connect() as c:
  projects=c.execute('select count(*) from projects').fetchone()[0]
  gens=c.execute("select count(*) from generation_jobs where status in ('pending','processing','queued')").fetchone()[0]
  renders=c.execute("select count(*) from render_jobs where status in ('pending','processing','queued')").fetchone()[0]
 return {"projects":projects,"active_jobs":gens,"render_queue":renders,"output_dir":str(OUTPUT_DIR)}
@app.get('/api/engines')
def engines():return all_status()
@app.get('/api/projects')
def projects():
 with connect() as c:return [dict(r) for r in c.execute('select * from projects order by created_at desc')]
@app.post('/api/projects')
def create_project(p:ProjectIn):
 pid=str(uuid4())
 with connect() as c:c.execute('insert into projects(id,title,topic,language,duration,aspect_ratio,resolution,fps,style) values(?,?,?,?,?,?,?,?,?)',(pid,p.title,p.topic,p.language,p.duration,p.aspect_ratio,p.resolution,p.fps,p.style))
 return {"id":pid,**p.model_dump(),"status":"draft"}
@app.get('/api/projects/{pid}')
def get_project(pid:str):
 with connect() as c:
  p=c.execute('select * from projects where id=?',(pid,)).fetchone()
  if not p:raise HTTPException(404,"Projeto não encontrado")
  return {**dict(p),"scenes":[dict(s) for s in c.execute('select * from scenes where project_id=? order by position',(pid,))]}
@app.post('/api/director/plan')
def director(body:dict):
 try:
  plan=make_plan(body.get('idea',''),body.get('language','pt-BR'),int(body.get('duration',60)),body.get('style','cinematic'))
  project_id=body.get('project_id')
  if project_id:
   with connect() as c:
    if not c.execute('select 1 from projects where id=?',(project_id,)).fetchone(): raise HTTPException(404,'Projeto não encontrado')
    c.execute('delete from scenes where project_id=?',(project_id,))
    for scene in plan['scenes']:
     c.execute('insert into scenes(id,project_id,position,title,prompt,duration,engine,status) values(?,?,?,?,?,?,?,?)',(str(uuid4()),project_id,scene['position'],scene['title'],scene['prompt'],scene['duration'],'ltx','planned'))
  return plan
 except (ValueError,TypeError) as e:raise HTTPException(400,str(e))
@app.post('/api/ltx/jobs')
def submit_ltx(body:LTXIn):
 jobid=str(uuid4())
 try:
  result=LTXClient().submit_text_to_video(body.prompt,body.model,body.duration,body.resolution,body.fps,body.generate_audio,body.camera_motion)
  ext=result.get('id')
  with connect() as c:c.execute('insert into generation_jobs(id,project_id,provider,model,prompt,status,external_id) values(?,?,?,?,?,?,?)',(jobid,body.project_id,'ltx',body.model,body.prompt,'pending',ext))
  return {"id":jobid,"external_id":ext,"status":"pending","provider":"LTX API v2","model":body.model,"submitted":True}
 except LTXError as e:raise HTTPException(502,str(e))
@app.get('/api/ltx/jobs/{jobid}')
def get_ltx_job(jobid:str):
 with connect() as c:row=c.execute('select * from generation_jobs where id=?',(jobid,)).fetchone()
 if not row:raise HTTPException(404,"Job não encontrado")
 row=dict(row)
 if row['external_id']:
  try:
   state=LTXClient().get_job(row['external_id']); status=state.get('status','unknown')
   with connect() as c:c.execute('update generation_jobs set status=?,updated_at=CURRENT_TIMESTAMP where id=?',(status,jobid))
   return {**row,"status":status,"provider_status":state,"result":state.get('result')}
  except LTXError as e:return {**row,"poll_error":str(e)}
 return row
@app.get('/api/jobs')
def jobs():
 with connect() as c:return [dict(r) for r in c.execute('select id,provider,model,status,created_at from generation_jobs order by created_at desc limit 30')]
@app.get('/api/settings')
def settings():
 with connect() as c:return {r['key']:json.loads(r['value']) for r in c.execute('select key,value from settings')}
@app.get('/api/ai/ltx/status')
def ltx_status():return LTXClient().health()
FRONT=ROOT/'frontend'
app.mount('/static',StaticFiles(directory=FRONT),name='static')
@app.get('/')
def index():
 from fastapi.responses import FileResponse
 return FileResponse(FRONT/'index.html')
