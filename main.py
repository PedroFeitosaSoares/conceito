from extraiTextoPDF import TextExtractor
from dotenv import load_dotenv
import pandas as pd
from download_files import FileDownloader
from extrai_informacao_html import HTMLInformationExtractor
from agent_refatorado import AgentResumo
import os
class MainResumo:
    def __init__(self, api_key):
        self.agent = AgentResumo(api_key)
        self.file_downloader = FileDownloader()

    def make(self, link: str):
        HTMLInformationExtractor.extrair_data(link)
        self.file_downloader.limpar_arquivos()

        df = pd.read_csv("Documentos do Processo.csv")

        documentos_nao_baixados = 0

        for link in df['link']:
            if not isinstance(link, str) or pd.isna(link):
                print(f"Ignorado: '{link}' não é uma URL válida.")
                documentos_nao_baixados += 1
            else:
                self.file_downloader.download_files(link)

        textos_processos = TextExtractor.ler_texto_arquivos_diretorio("Arquivos_Processo")
        resumo = self.agent.gerar_resumo(textos_processos)

        return resumo
    
if __name__ == "__main__":
    load_dotenv('.env')
    api_key = os.getenv("API_KEY")
    pipeline = MainResumo(api_key)

    user_input = str(input("Digite o link: "))
    print(pipeline.make(user_input))
