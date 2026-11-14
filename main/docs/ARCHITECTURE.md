# Arquitetura

- `backend/`: API FastAPI e inicialização do SQLite.
- `ai/director.py`: planejador determinístico substituível por provedor LLM.
- `ai/ltx/client.py`: integração cloud LTX API v2 com modelos documentados e jobs assíncronos.
- `engines/registry.py`: detecção efetiva de executáveis/serviços; detecção não equivale a integração de render.
- `frontend/`: painel responsivo HTML/CSS/JS servido pela API.
- `notebooks/`: launcher de runtime Google Colab.
- `storage/`: dados mutáveis fora do Git.

O backend é local e sem autenticação de usuário por padrão; mantenha em localhost. Para hospedagem pública, implemente autenticação, TLS, rate limits, isolamento de jobs e revisão de segurança antes de expor.
