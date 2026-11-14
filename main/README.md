# NUBI VIDEO AI STUDIO

Starter modular executável para painel local, projetos, banco SQLite, planejamento inicial de cenas e submissão/polling de jobs LTX API v2. **Não é ainda a suíte de edição/render completa do prompt.**

## Requisitos e início local

- Python 3.10+ (recomendado 3.11).
- Opcional: FFmpeg/FFprobe, Blender, Houdini, ComfyUI remoto e aplicativos desktop com suas licenças.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Abra `http://127.0.0.1:8000`. O backend local não oferece autenticação; não o exponha publicamente. Dados ficam em `storage/`. Configure caminhos via variáveis de ambiente; para LTX, defina `LTX_API_KEY` no ambiente e não no código.

## Google Colab

Abra `notebooks/NUBI_Colab_Launcher.ipynb` e siga `docs/COLAB_GUIDE.md`. Drive é opcional, mas recomendado para persistência. A geração via LTX cloud exige uma chave válida e pode consumir créditos.

## O que funciona nesta entrega

- API FastAPI com health check, projetos, plano de cinco cenas, banco SQLite e registro de status/jobs.
- Dashboard responsivo em português com verificação efetiva de executáveis/serviços.
- Adaptador LTX cloud assíncrono para modelos LTX-2.3/2.5 documentados; chave ausente e erros do provedor são tratados.
- Notebook Colab com hardware, Drive, clone/atualização, configuração, banco, startup, proxy, testes e shutdown.

## Limites explícitos

O AI Director gera plano-base determinístico, não roteiro LLM. Não estão concluídos: timeline multi-trilha, síntese de imagens/áudio, renderização final, workers, geração local de LTX, fluxo ComfyUI, exportadores funcionais Blender/Houdini, Fusion/Natron/After Effects round-trip e composição Remotion. Detectar software não significa executar um pipeline. Consulte `docs/ENGINES.md`.

## Testes e licença

```bash
pytest -q
```

Nenhum modelo ou mídia de demonstração é baixado. Confira licenças e custos dos serviços e softwares antes do uso comercial.
