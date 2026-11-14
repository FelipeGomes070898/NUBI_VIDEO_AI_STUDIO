# Solução de problemas

- **Não abre o painel:** confira se o processo iniciou e acesse `http://127.0.0.1:8000`; logs aparecem no terminal/saída da célula Colab.
- **LTX 401:** a chave está ausente ou inválida. Use variável de ambiente/Colab Secrets; nunca coloque tokens em código versionado.
- **LTX 429 / sem crédito:** aguarde liberação da fila ou consulte saldo/limites da conta LTX.
- **Sem GPU:** o sistema continua em modo CPU para planejamento; geração local de modelos pesados não é garantida.
- **Dados do Colab sumiram:** `/content` é temporário; monte Drive antes de iniciar e use-o como `NUBI_DATA_DIR`.
- **Blender/Houdini/Desktop não detectados:** o notebook não os instala automaticamente. Use um host externo com instalação/licença compatível.
- **CORS / túnel:** não exponha o servidor sem autenticação. A URL de proxy do Colab é temporária e vinculada à sessão.
