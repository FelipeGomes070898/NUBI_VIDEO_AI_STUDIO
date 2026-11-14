import os, shutil, subprocess, platform
from pathlib import Path

def probe(name):
    spec={"ffmpeg":("ffmpeg",["-version"]),"ffprobe":("ffprobe",["-version"]),"blender":(os.getenv("BLENDER_BIN","blender"),["--version"]),"houdini":(os.getenv("HOU_TOOL","hython"),["--version"]),"natron":(os.getenv("NATRON_BIN","Natron"),["--version"]),"after-effects":(os.getenv("AFTER_EFFECTS_BIN","aerender"),["-help"]),"remotion":("npx",["--no-install","remotion","--version"]),"comfyui":(os.getenv("COMFYUI_URL",""),[]),"fusion":(os.getenv("FUSION_BIN","/opt/resolve/resolve"),[])}
    binary,args=spec.get(name,(name,[]))
    if name=="comfyui":
        if not binary: return {"name":name,"available":False,"mode":"optional","detail":"COMFYUI_URL não configurada"}
        try:
            import requests; r=requests.get(binary.rstrip("/")+"/system_stats",timeout=2)
            return {"name":name,"available":r.ok,"mode":"remote","detail":f"HTTP {r.status_code}"}
        except Exception as e:return {"name":name,"available":False,"mode":"remote","detail":str(e)[:120]}
    resolved=shutil.which(binary) if not Path(binary).is_absolute() else (binary if Path(binary).exists() else None)
    if not resolved:return {"name":name,"available":False,"mode":"external" if name in {"fusion","after-effects"} else "optional","detail":"Executável não encontrado"}
    try:
        p=subprocess.run([resolved,*args],capture_output=True,text=True,timeout=3)
        version=(p.stdout or p.stderr).strip().splitlines()[0][:120] if (p.stdout or p.stderr) else "Executável detectado"
        return {"name":name,"available":True,"mode":"local","detail":version}
    except Exception as e:return {"name":name,"available":False,"mode":"local","detail":str(e)[:120]}

def all_status():
    names=["ffmpeg","ffprobe","blender","houdini","fusion","natron","remotion","after-effects","comfyui"]
    return {"platform":platform.platform(),"engines":[probe(n) for n in names]}
