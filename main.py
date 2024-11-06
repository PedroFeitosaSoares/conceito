from extraiTextoPDF import ler_texto_arquivos_diretorio
from dotenv import load_dotenv
import pandas as pd
from download_files import download_files
from extrai_tabela_data import extrair_data
import os

extrair_data("https://www.sipac.ufpi.br/public/jsp/processos/processo_detalhado.jsf?id=673322#")

df = pd.read_csv("Documentos do Processo.csv")

documentos_nao_baixados = 0

for link in df['link']:
    if not isinstance(link, str) or pd.isna(link):
        print(f"Ignorado: '{link}' não é uma URL válida.")
        documentos_nao_baixados = documentos_nao_baixados + 1
    else:
        download_files(link)

textos_processos = ler_texto_arquivos_diretorio("Arquivos_Processo")

print(textos_processos)
print(documentos_nao_baixados)