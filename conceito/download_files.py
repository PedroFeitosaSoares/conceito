import os
import requests

# Define the base URL
base_url = "https://raw.githubusercontent.com/armandossrecife/mysummary/refs/heads/main/pdfs/"

# Defina o nome da pasta onde os PDFs serão salvos
download_folder = 'PDFs'

# Verifique se a pasta existe, se não, crie-a
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Directory '{download_folder}' created")

# Function to download a file without using tqdm
def download_file(url, dest_folder):
    filename = os.path.join(dest_folder, url.split("/")[-1])
    
    # Send HTTP request and get the total file size for the progress display
    response = requests.get(url, stream=True)
    
    # Check if the file exists (status code 200)
    if response.status_code != 200:
        return False

    total_size = int(response.headers.get('content-length', 0))
    downloaded_size = 0

    # Download the file with manual progress tracking
    with open(filename, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            downloaded_size += len(data)
            # Display progress in percentage
            progress = (downloaded_size / total_size) * 100
            print(f"\rDownloading {filename}: {progress:.2f}%", end="")

    print(f"\nDownloaded: {filename}")
    return True

# Loop to try downloading files until one fails
i = 1
while True:
    url = f"{base_url}d{i}.pdf"
    print(f"Trying to download {url}")
    try:
        if not download_file(url, download_folder):
            print(f"No more files found after {i-1} downloads.")
            break
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        break
    i += 1

print("Download process finished!")
