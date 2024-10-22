import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


def extrair_dados_processo(url):
    try:
        # Faz a requisição GET para obter o conteúdo da página
        resposta = requests.get(url)
        resposta.raise_for_status()  # Garante que não houve erro na requisição

        # Parseando o HTML com BeautifulSoup
        soup = BeautifulSoup(resposta.content, 'html.parser')

        # Exemplo: Extraindo título e informações de tabelas
        titulo = soup.title.string if soup.title else "Título não encontrado"

        # Buscando uma tabela de dados (ajustar o seletor conforme o site)
        tabela = soup.find('table')
        dados_processo = []

        if tabela:
            # Iterando pelas linhas e colunas da tabela
            for linha in tabela.find_all('tr'):
                colunas = [coluna.get_text(strip=True) for coluna in linha.find_all('td')]
                if colunas:  # Apenas adiciona linhas não vazias
                    dados_processo.append(colunas)
        else:
            print("Tabela não encontrada.")

        # Retorna o título e os dados extraídos
        return {
            "titulo": titulo,
            "dados_processo": dados_processo
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None

load_dotenv()
URL = os.getenv("URL")

url_processo = URL
dados = extrair_dados_processo(url_processo)

if dados:
    print("Título da Página:", dados['titulo'])
    print("Dados do Processo:")
    for linha in dados['dados_processo']:
        print(linha)