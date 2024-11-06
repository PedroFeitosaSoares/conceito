import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin
import pandas as pd
import os
import re

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

                        # Extrai todos os links na célula, incluindo sublistagens
                        links = []
                        for a in coluna.find_all('a', href=True):
                            href = a.get('href', '')

                            # Caso o href não seja útil, verifica o onclick
                            if href == '#':
                                onclick = a.get('onclick', '')
                                match = re.search(r"window\.open\('([^']+)'", onclick)
                                if match:
                                    href = match.group(1)

                            links.append(urljoin(url, href))

                        if links:
                            texto += " " + " | ".join(links) + ""  # Anexa todos os links ao texto da célula

                        dados_linha.append(texto)

                    if dados_linha:  # Adiciona apenas linhas não vazias
                        linhas.append(dados_linha)

                # Cria o DataFrame da tabela atual
                df = pd.DataFrame(linhas, columns=headers)
                dataframes[legenda] = df
                if legenda == "Movimentações do Processo":
                    dataframes[legenda] = tratamento_movimentacoes_processos(df)
                if legenda == "Documentos do Processo":
                    dataframes[legenda] = tratamento_documentos_processos(df)

        return dataframes

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None
def tratamento_movimentacoes_processos(df):
    # Remove linhas com índices 1, 4, 7, etc., mantendo apenas os índices pares para preenchimento
    df = df.drop(df.index[range(1, len(df), 3)]).reset_index(drop=True)
    
    # Criar as novas colunas
    df[['Despacho', "Link"]] = None
    
    # Preencher as colunas 'Despacho' e 'Link despacho' dos índices pares
    # com os valores das colunas 'unidade origem' e 'unidade destino' dos índices ímpares
    for i in range(0, len(df) - 1, 2):
        df.at[i, 'Despacho'] = df.at[i + 1, 'Unidade Origem']
        df.at[i, 'Link'] = df.at[i + 1, 'Unidade Destino']
        
    #remover as linhas impares
    df = df.drop(df.index[range(1, len(df), 2)]).reset_index(drop=True)
    
    return df

def tratamento_documentos_processos(df):
    # Faz uma cópia do DataFrame original para preservar os dados
    df_copy = df.copy()

    # Exclui as duas últimas colunas do DataFrame original e modifica df diretamente
    df = df.iloc[:, :-2].copy()  # Garante que df seja uma cópia independente

    # Cria uma nova coluna chamada 'link' no DataFrame original usando .loc
    df.loc[:, 'link'] = df_copy.iloc[:, -2].values  # Usa valores da penúltima coluna de df_copy

    return df
    
def extrair_data(URL):
    # Legendas das tabelas que queremos extrair
    legendas_tabelas = ["Documentos do Processo", "Movimentações do Processo"]
    # Extrair as tabelas e organizá-las em DataFrames
    tabelas_df = extrair_tabelas_para_dataframe(URL, legendas_tabelas)

    # Exibir e manipular as tabelas extraídas
    if tabelas_df:
        for legenda, df in tabelas_df.items():
            # Exemplo: Salvar a tabela em CSV
            df.to_csv(f"{legenda}.csv", index=False)
