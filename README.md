# A - APLICAÇÃO PARA EXTRAIR OS DADOS DE UM PROCESSO PÚBLICO DO SIPAC

1. O usuário passa o link do processo

https://www.sipac.ufpi.br/public/jsp/processos/processo_detalhado.jsf?id=673322#

2. O sistema acessa o conteúdo da página pública do processo

3. O sistema baixa localmente dois arquivos csv com o conteúdo público do processo

4. O sistema extrai os dados do processo a partir dos csvs
- dados gerais do processo
- interessado
- documentos do processo
- movimentações do processo

Processamento:
1. Acessar o conteúdo público do processo
2. Baixar localmente os CSVs
3. Extrair os dados dos arquivos CSVs

Saída:
- dados gerais do processo
- interessado
- documentos do processo ()
- movimentações do processo

# B - APLICAÇÃO PARA RESUMIR OS DADOS DO PROCESSO

1. Resumir os textos
Acessar a LLM e passar os textos para resumir

2. Quais os tipos de resumo
- Resumo Geral (a concatenação de TODOS os texto do processo)
- documentos do processo
- Resumo das movimentações

3. Resultados dos resumos