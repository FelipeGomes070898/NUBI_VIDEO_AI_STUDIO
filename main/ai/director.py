from typing import Any

def make_plan(idea: str, language: str="pt-BR", duration: int=60, style: str="cinematic") -> dict[str, Any]:
    """Deterministic planning starter. Plug an LLM provider in through this module later."""
    idea=idea.strip()
    if not idea: raise ValueError("Informe uma ideia para o projeto.")
    labels=["Gancho", "Contexto", "Desenvolvimento", "Clímax", "Conclusão"]
    ratios=[.10,.18,.34,.23,.15]
    scenes=[]; elapsed=0
    for i,(label,ratio) in enumerate(zip(labels,ratios),1):
        secs=round(duration*ratio,1)
        scenes.append({"position":i,"title":label,"duration":secs,"start":round(elapsed,1),"prompt":f"{style}; {label.lower()} da história: {idea}. Direção de câmera e iluminação cinematográficas."})
        elapsed+=secs
    return {"idea":idea,"language":language,"duration":duration,"style":style,"hook":f"Uma abertura visual forte que introduz: {idea}","scenes":scenes,"note":"Plano-base determinístico; conecte um LLM para roteiro criativo completo."}
