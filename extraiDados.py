import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import pandas as pd
import os

def limpar_tabela(df):
    # Remove colunas totalmente vazias
    df = df.dropna(axis=1, how='all')
    
    # Remove linhas totalmente vazias
    df = df.dropna(axis=0, how='all')
    
    # Remove colunas duplicadas com base nos nomes das colunas
    df = df.loc[:, ~df.columns.duplicated()]

    # Remove linhas duplicadas
    df = df.drop_duplicates()

    # Preenche valores vazios em células com um marcador ou deixa como está (ex: "N/A")
    df = df.fillna("N/A")

    return df

def converter_dataframe_para_dict(dataframes):
    # Dicionário final com todas as tabelas
    tabelas_dict = {}

    for nome_tabela, df in dataframes.items():
        # Cria o dicionário para a tabela atual
        tabela_dict = {}

        for i, linha in df.iterrows():
            # Cria o dicionário da linha com chave como nome da coluna e valor como conteúdo da célula
            tabela_dict[f"id={i}"] = linha.to_dict()

        # Adiciona ao dicionário final usando o nome da tabela como chave
        tabelas_dict[nome_tabela] = tabela_dict

    return tabelas_dict

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

                # Limpar a tabela usando a função limpar_tabela
                df = limpar_tabela(df)

                # Armazena o DataFrame limpo no dicionário de dataframes
                dataframes[legenda] = df

        # Converter os dataframes para dicionários
        tabelas_dict = converter_dataframe_para_dict(dataframes)
        return tabelas_dict

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None


# Carregar a URL do .env
load_dotenv()
URL = os.getenv("URL")

# Legendas das tabelas que queremos extrair
legendas_tabelas = ["Documentos do Processo"]

# Extrair as tabelas e organizá-las em dicionários
tabelas_dict = extrair_tabelas_para_dataframe(URL, legendas_tabelas)

# Exibir o dicionário resultante
if tabelas_dict:
    for nome_tabela, conteudo in tabelas_dict.items():
        print(f"\nTabela: {nome_tabela}")
        for id_linha, dados_linha in conteudo.items():
            print(f"{id_linha}: {dados_linha}")
