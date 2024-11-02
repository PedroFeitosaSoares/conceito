import fitz
import os
from bs4 import BeautifulSoup

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
            textos[arquivo] = ler_texto_pdf(caminho_arquivo)
        elif arquivo.lower().endswith(".html"):
            textos[arquivo] = ler_texto_html(caminho_arquivo)
    return textos

diretorio = "Arquivos_Processo"  # Substitua pelo caminho do diretório onde estão seus arquivos

# Extrair o texto de todos os arquivos PDF e HTML do diretório
textos_extraidos = ler_texto_arquivos_diretorio(diretorio)

# Exibir o texto extraído
for nome_arquivo, texto in textos_extraidos.items():
    print(f"Texto extraído de {nome_arquivo}:")
    print(texto[:500])  # Exibe os primeiros 500 caracteres para cada arquivo
    print("-" * 50)