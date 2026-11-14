"""LTX API v2 asynchronous client. Credentials are read only from environment."""
import os, requests
BASE="https://api.ltx.io"
MODELS={"ltx-2-3-fast","ltx-2-3-pro","ltx-2-5-fast","ltx-2-5-pro"}
CAMERA={"dolly_in","dolly_out","dolly_left","dolly_right","jib_up","jib_down","static","focus_shift"}
class LTXError(RuntimeError): pass
class LTXClient:
    def __init__(self, api_key=None, timeout=45):
        self.api_key=api_key or os.getenv("LTX_API_KEY"); self.timeout=timeout
    def _headers(self):
        if not self.api_key: raise LTXError("LTX_API_KEY ausente; configure-o no ambiente.")
        return {"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"}
    def submit_text_to_video(self, prompt, model="ltx-2-5-fast", duration=5, resolution="1280x720", fps=24, generate_audio=True, camera_motion=None):
        if model not in MODELS: raise LTXError(f"Modelo inválido; opções: {', '.join(sorted(MODELS))}")
        if not prompt.strip() or len(prompt)>5000: raise LTXError("O prompt deve conter de 1 a 5000 caracteres.")
        if duration is not None and not 1<=int(duration)<=20: raise LTXError("Duração deve ser entre 1 e 20 segundos por solicitação.")
        body={"prompt":prompt,"model":model,"duration":duration,"resolution":resolution,"fps":fps,"generate_audio":generate_audio}
        if camera_motion:
            if camera_motion not in CAMERA: raise LTXError("Movimento de câmera inválido.")
            body["camera_motion"]=camera_motion
        r=requests.post(f"{BASE}/v2/text-to-video",headers=self._headers(),json=body,timeout=self.timeout)
        if not r.ok: raise LTXError(f"LTX HTTP {r.status_code}: {r.text[:800]}")
        return r.json()
    def get_job(self, job_id):
        r=requests.get(f"{BASE}/v2/text-to-video/{job_id}",headers=self._headers(),timeout=self.timeout)
        if not r.ok: raise LTXError(f"LTX HTTP {r.status_code}: {r.text[:800]}")
        return r.json()
    def health(self): return {"configured":bool(self.api_key),"provider":"LTX API v2","base_url":BASE,"models":sorted(MODELS),"authenticated":False,"note":"Conectividade/autenticação só é validada ao enviar uma solicitação."}
