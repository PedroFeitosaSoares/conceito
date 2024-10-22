import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import pandas as pd
import os

def extrair_tabelas_para_dataframe(url, legendas):
    try:
        # Faz a requisição GET para obter o conteúdo da página
        resposta = requests.get(url)
        resposta.raise_for_status()  # Garante que não houve erro na requisição

        # Parseando o HTML com BeautifulSoup
        soup = BeautifulSoup(resposta.content, 'html.parser')

        # Armazena DataFrames para cada tabela
        dataframes = {}

        # Iterar sobre as legendas-alvo e buscar as tabelas correspondentes
        for legenda in legendas:
            tabela = None

            # Procurando todas as tabelas e verificando a legenda <caption>
            for t in soup.find_all('table'):
                caption = t.find('caption')
                if caption and legenda in caption.get_text(strip=True):
                    tabela = t
                    break  # Para ao encontrar a tabela correta

            # Se a tabela foi encontrada, extrair os dados
            if tabela:
                linhas = []
                headers = [th.get_text(strip=True) for th in tabela.find_all('tr')[0].find_all('th')]

                # Itera pelas linhas da tabela, pulando a linha de cabeçalho
                for linha in tabela.find_all('tr')[1:]:
                    dados_linha = []
                    for coluna in linha.find_all(['th', 'td']):
                        texto = coluna.get_text(strip=True)

                        # Verifica se há link na célula e anexa ao texto
                        link = coluna.find('a', href=True)
                        if link:
                            texto += f" (Link: {urljoin(url, link['href'])})"

                        dados_linha.append(texto)

                    if dados_linha:  # Adiciona apenas linhas não vazias
                        linhas.append(dados_linha)

                # Cria o DataFrame da tabela atual
                df = pd.DataFrame(linhas, columns=headers)
                dataframes[legenda] = df

        return dataframes

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None


# Carregar a URL do .env
load_dotenv()
URL = os.getenv("URL")

# Legendas das tabelas que queremos extrair
legendas_tabelas = ["Documentos do Processo", "Movimentações do Processo"]

# Extrair as tabelas e organizá-las em DataFrames
tabelas_df = extrair_tabelas_para_dataframe(URL, legendas_tabelas)

# Exibir e manipular as tabelas extraídas
if tabelas_df:
    for legenda, df in tabelas_df.items():
        print(f"\nTabela: {legenda}")
        print(df)

        # Exemplo: Salvar a tabela em CSV
        df.to_csv(f"{legenda}.csv", index=False)
