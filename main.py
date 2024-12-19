from extraiTextoPDF import ler_texto_arquivos_diretorio
from dotenv import load_dotenv
import pandas as pd
from download_files import download_files, limpar_arquivos
from extrai_informacao_html import extrair_data
from agent_refatorado import AgentResumo
import os

class ResumoPipeline:
    def __init__(self, api_key):
        self.agent = AgentResumo(api_key)

    def make(self, link: str):
        extrair_data(link)
        limpar_arquivos()

        df = pd.read_csv("Documentos do Processo.csv")

        documentos_nao_baixados = 0

        for link in df['link']:
            if not isinstance(link, str) or pd.isna(link):
                print(f"Ignorado: '{link}' não é uma URL válida.")
                documentos_nao_baixados += 1
            else:
                download_files(link)

        textos_processos = ler_texto_arquivos_diretorio("Arquivos_Processo")
        resumo = self.agent.gerar_resumo(textos_processos)

        return resumo
    
if __name__ == "__main__":
    load_dotenv('.env')
    api_key = os.getenv("API_KEY")
    pipeline = Resumo(api_key)

    user_input = str(input("Digite o link: "))
    print(pipeline.make(user_input))
