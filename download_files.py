import requests
import os
import re

def download_files(url):
    download_folder = 'Arquivos_Processo'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"Directory '{download_folder}' created")

    # Verifica se a URL contém "idArquivo=" ou termina em .pdf
    if "idArquivo=" in url or url.endswith('.pdf'):
        download_file(url, download_folder, is_pdf=True)
    elif "documento_visualizacao.jsf?idDoc=" in url:
        # Salva como HTML se for uma página de visualização
        download_file(url, download_folder, is_pdf=False)
    else:
        # Download de uma sequência de PDFs
        i = 1
        while True:
            pdf_url = f"{url.rstrip('/')}/d{i}.pdf"
            print(f"Trying to download {pdf_url}")
            if not download_file(pdf_url, download_folder, is_pdf=True):
                print(f"No more files found after {i-1} downloads.")
                break
            i += 1

def download_file(url, dest_folder, is_pdf=True):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print(f"Failed to download: {url}")
        return False

    # Tenta extrair o nome do arquivo ou usa o idDoc como nome base para HTML
    if is_pdf:
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            match = re.search(r'filename="(.+)"', content_disposition)
            filename = match.group(1) if match else url.split("/")[-1]
        else:
            filename = url.split("/")[-1]
        
        filename = re.sub(r'[^\w\-.]', '_', filename)  # Limpa caracteres inválidos
        if not filename.endswith('.pdf'):
            filename += '.pdf'
    else:
        # Usa o idDoc como nome base e evita sobrescrever arquivos HTML
        filename = f"idDoc_{re.search(r'idDoc=(\d+)', url).group(1)}.html"

    filepath = os.path.join(dest_folder, filename)

    if is_pdf:
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(filepath, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                downloaded_size += len(data)
                if total_size > 0:
                    progress = (downloaded_size / total_size) * 100
                    print(f"\rDownloading {filename}: {progress:.2f}%", end="")
                else:
                    print(f"\rDownloading {filename}: {downloaded_size} bytes downloaded", end="")
    else:
        # Salva o conteúdo HTML
        with open(filepath, 'w', encoding=response.encoding) as file:
            file.write(response.text)
        print(f"\nSaved HTML page: {filename}")

    print(f"\nDownloaded: {filename}")
    return True

download_files("https://www.sipac.ufpi.br/public/jsp/processos/documento_visualizacao.jsf?idDoc=2068823")