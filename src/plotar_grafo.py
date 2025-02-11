import os
import json
import networkx as nx
import matplotlib.pyplot as plt

# Definição de caminhos
PASTA_GRAFOS = "C:/Users/Bruno/Documents/Faculdade/Trabalho Final/grafos_Json"
PASTA_SAIDA_BASE = "C:/Users/Bruno/Documents/Faculdade/Trabalho Final/grafos_imagens"
os.makedirs(PASTA_SAIDA_BASE, exist_ok=True)

# Função para processar e salvar um grafo

def processar_grafo(arquivo_json):
    with open(arquivo_json, 'r') as f:
        grafo_data = json.load(f)

    G = nx.Graph()

    # Adicionando nós
    for node in grafo_data['nodes']:
        G.add_node(node['id'], label=node['label'])

    # Adicionando arestas com pesos
    for edge in grafo_data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

    # Calcular PageRank
    pagerank = nx.pagerank(G)
    max_pagerank = max(pagerank.values())
    node_sizes = [pagerank[n] / max_pagerank * 10000 for n in G.nodes()]
    
    # Layout do grafo
    pos = nx.spring_layout(G, k=0.7, seed=42)
    
    plt.figure(figsize=(15, 10))
    labels = nx.get_node_attributes(G, 'label')
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="lightblue", 
                           edgecolors="black", linewidths=2, alpha=0.85)
    
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    edge_widths = [w / max(edge_weights) * 100 for w in edge_weights]
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.7, edge_color="black")
    
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color="black", 
                            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"))
    
    # Salvar grafo
    nome_arquivo = os.path.basename(arquivo_json).replace("_location_graph.json", "")
    nome_mapa = os.path.basename(os.path.dirname(arquivo_json))
    pasta_mapa = os.path.join(PASTA_SAIDA_BASE, nome_mapa)
    os.makedirs(pasta_mapa, exist_ok=True)
    caminho_saida = os.path.join(pasta_mapa, nome_arquivo + ".png")
    plt.title(f"Grafo: {nome_arquivo}", fontsize=14, fontweight="bold")
    plt.savefig(caminho_saida, format="png", dpi=300, bbox_inches="tight")
    plt.close()

# Processar todos os grafos na pasta
def processar_todos_grafos():
    for root, _, files in os.walk(PASTA_GRAFOS):
        for file in files:
            if file.endswith("_location_graph.json"):
                caminho_arquivo = os.path.join(root, file)
                processar_grafo(caminho_arquivo)

# Executa o processamento
processar_todos_grafos()
