# Compatibilidade e status dos engines

| Engine | Estado desta entrega | Requisito / limite |
|---|---|---|
| LTX API v2 | Adaptador cloud implementado; não autenticado aqui | Chave válida, saldo e custos conforme conta; solicitações de até 20 s cada de acordo com modelo/API; geração real requer chamada autorizada. |
| LTX local | Não integrado | Pesos/licença e GPU compatível dependem da distribuição do modelo. |
| FFmpeg/FFprobe | Detectados se instalados | Transcodificação programática; esta base ainda não implementa pipeline de exportação completo. |
| Blender | Detecção de binário | Instalação e memória; render headless não está ligado a jobs de produção nesta versão. |
| Houdini | Detecção de hython | Instalação e licença; normalmente requer estação/serviço externo. |
| Fusion, Natron, After Effects | Detectores/adaptadores planejados; não ativos no Colab padrão | Apps desktop/licenças; integração via troca de arquivos ainda deve ser construída. |
| Remotion | Detecta Node/npm quando disponível | Não há composição/render Remotion funcional implementado nesta entrega; licença deve ser conferida para uso comercial. |
| ComfyUI | Health check remoto configurável | Informe `COMFYUI_URL`; o fluxo de geração ainda não foi integrado ao painel. |
| Piper/Kokoro/Whisper.cpp | Não conectados | Configuração e instalação externa necessárias. |

O painel reporta detecção real, e não inventa renderização ou progresso.
