from extraiTextoPDF import ler_texto_arquivos_diretorio
from dotenv import load_dotenv
import pandas as pd
from download_files import download_files, limpar_arquivos
from extrai_informacao_html import extrair_data
from agent_refatorado import AgentResumo
import os

load_dotenv('.env')

agent = AgentResumo(os.getenv("API_KEY"))

def make(link: str):
    extrair_data(link)
    limpar_arquivos()

    df = pd.read_csv("Documentos do Processo.csv")

    documentos_nao_baixados = 0

    for link in df['link']:
        if not isinstance(link, str) or pd.isna(link):
            print(f"Ignorado: '{link}' não é uma URL válida.")
            documentos_nao_baixados = documentos_nao_baixados + 1
        else:
            download_files(link)

    textos_processos = ler_texto_arquivos_diretorio("Arquivos_Processo")
    resumo = agent.gerar_resumo(textos_processos)

    return resumo
