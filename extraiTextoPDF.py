import fitz
import os

def ler_texto_pdf(caminho_pdf):
    """Extrai o texto de um PDF especificado pelo caminho."""
    texto = ""
    with fitz.open(caminho_pdf) as pdf:
        for pagina in pdf:
            texto += pagina.get_text()
    return texto

def ler_texto_pdfs_diretorio(diretorio):
    """Extrai o texto de todos os PDFs dentro de um diretório."""
    textos = {}
    for arquivo in os.listdir(diretorio):
        if arquivo.lower().endswith(".pdf"):
            caminho_pdf = os.path.join(diretorio, arquivo)
            textos[arquivo] = ler_texto_pdf(caminho_pdf)
    return textos