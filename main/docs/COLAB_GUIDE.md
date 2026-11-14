# Guia rápido do Google Colab

1. Abra `notebooks/NUBI_Colab_Launcher.ipynb` no Google Colab.
2. Se necessário, em **Ambiente de execução → Alterar tipo de ambiente**, escolha GPU; disponibilidade é variável.
3. Execute as células do topo para baixo. Montar Drive é opcional; recomendado para persistência.
4. Para LTX, adicione `LTX_API_KEY` em **Secrets** do Colab e habilite acesso ao notebook, ou use a configuração segura solicitada na célula. Não imprima nem grave a chave no repositório. A chamada LTX pode custar créditos.
5. A célula final exibe URL de acesso pelo proxy integrado do Colab; use-a apenas durante a sessão. Não é um túnel público permanente.
6. Para encerrar, execute a célula de shutdown; arquivos persistentes devem apontar para Drive.

Houdini, Fusion, Natron e After Effects não são presumidos instalados no Colab.
