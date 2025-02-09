import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Definição de caminhos
PASTA_MAPAS = "mapas_arestas"
PASTA_GRAFICOS = "graficos_pagerank"
CAMINHO_NOS_GEPHI = "nos_gephi.csv"
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

# Carregar a tabela de nós
if not os.path.exists(CAMINHO_NOS_GEPHI):
    raise FileNotFoundError("Arquivo nos_gephi.csv não encontrado!")

nos_df = pd.read_csv(CAMINHO_NOS_GEPHI)
id_para_label = dict(zip(nos_df['Id'], nos_df['Label']))

# Função para processar cada bombsite
def processar_bombsite(caminho_arquivo, objectivelocation, pasta_graficos_bombsite):
    # Carregar as arestas
    arestas_df = pd.read_csv(caminho_arquivo)
    
    # Criar o grafo
    G = nx.Graph()
    for _, row in arestas_df.iterrows():
        operador1 = id_para_label.get(row['Source'], f"Desconhecido_{row['Source']}")  
        operador2 = id_para_label.get(row['Target'], f"Desconhecido_{row['Target']}")  
        G.add_edge(operador1, operador2, weight=row['Weight'])
    
    # Calcular o PageRank
    pagerank = nx.pagerank(G, alpha=0.85, weight='weight')
    
    # Transformar os dados em um DataFrame
    df_pagerank = pd.DataFrame(list(pagerank.items()), columns=['Operador', 'PageRank'])
    df_pagerank = df_pagerank.sort_values(by='PageRank', ascending=False)
    
    # Criar gráfico de barras
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Operador', y='PageRank', data=df_pagerank, palette="Blues_r")
    plt.title(f"PageRank dos Operadores - {objectivelocation}")
    plt.xlabel("Operadores")  
    plt.ylabel("Score de PageRank")  
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    # Salvar gráfico
    caminho_grafico = os.path.join(pasta_graficos_bombsite, f"pagerank_{objectivelocation}.png")
    plt.savefig(caminho_grafico, bbox_inches='tight')
    plt.close()

# Processar mapas
for mapa in os.listdir(PASTA_MAPAS):
    caminho_mapa = os.path.join(PASTA_MAPAS, mapa)
    if not os.path.isdir(caminho_mapa):
        continue
    
    pasta_graficos_mapa = os.path.join(PASTA_GRAFICOS, mapa)
    os.makedirs(pasta_graficos_mapa, exist_ok=True)
    
    # Processar arquivos de arestas
    for arquivo in os.listdir(caminho_mapa):
        if arquivo.endswith("_arestas.csv"):
            objectivelocation = arquivo.replace("_arestas.csv", "")
            pasta_graficos_bombsite = os.path.join(pasta_graficos_mapa, objectivelocation)
            os.makedirs(pasta_graficos_bombsite, exist_ok=True)
            caminho_arquivo = os.path.join(caminho_mapa, arquivo)
            processar_bombsite(caminho_arquivo, objectivelocation, pasta_graficos_bombsite)
