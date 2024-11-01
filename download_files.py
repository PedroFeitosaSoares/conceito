import os
import requests
import re

def download_pdfs(url):
    download_folder = 'PDFs'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"Directory '{download_folder}' created")

    # Verifica se a URL contém "idArquivo=", indicando um link direto para um único arquivo
    if "idArquivo=" in url or url.endswith('.pdf'):
        # Download de um único PDF
        download_file(url, download_folder)
    else:
        # Download de uma sequência de PDFs do repositório
        i = 1
        while True:
            pdf_url = f"{url.rstrip('/')}/d{i}.pdf"
            print(f"Trying to download {pdf_url}")
            if not download_file(pdf_url, download_folder):
                print(f"No more files found after {i-1} downloads.")
                break  # Sai do loop quando o arquivo não existe
            i += 1

def download_file(url, dest_folder):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print(f"Failed to download: {url}")
        return False

    # Tenta extrair o nome do arquivo do cabeçalho Content-Disposition
    content_disposition = response.headers.get('content-disposition')
    if content_disposition:
        match = re.search(r'filename="(.+)"', content_disposition)
        if match:
            filename = match.group(1)
        else:
            filename = url.split("/")[-1]
    else:
        filename = url.split("/")[-1]

    filename = re.sub(r'[^\w\-.]', '_', filename)  # Remove caracteres inválidos
    if not filename.endswith('.pdf'):
        filename += '.pdf'  # Garante a extensão .pdf
    filepath = os.path.join(dest_folder, filename)

    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    with open(filepath, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            downloaded_size += len(data)
            if total_size > 0:  # Verifica se o tamanho total é conhecido
                progress = (downloaded_size / total_size) * 100
                print(f"\rDownloading {filename}: {progress:.2f}%", end="")
            else:
                print(f"\rDownloading {filename}: {downloaded_size} bytes downloaded", end="")

    print(f"\nDownloaded: {filename}")
    return True