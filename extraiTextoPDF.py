import fitz
import os
from bs4 import BeautifulSoup
class TextExtractor:
    def ler_texto_pdf(caminho_pdf):
        """Extrai o texto de um PDF especificado pelo caminho."""
        texto = ""
        with fitz.open(caminho_pdf) as pdf:
            for pagina in pdf:
                texto += pagina.get_text()
        return texto

    def ler_texto_html(caminho_html):
        """Extrai o texto de um arquivo HTML especificado pelo caminho."""
        with open(caminho_html, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            texto = soup.get_text()
        return texto

    def ler_texto_arquivos_diretorio(diretorio):
        """Extrai o texto de todos os arquivos PDF e HTML dentro de um diretório."""
        textos = {}
        for arquivo in os.listdir(diretorio):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            if arquivo.lower().endswith(".pdf"):
                textos[arquivo] = TextExtractor.ler_texto_pdf(caminho_arquivo)
            elif arquivo.lower().endswith(".html"):
                textos[arquivo] = TextExtractor.ler_texto_html(caminho_arquivo)
        return textos
