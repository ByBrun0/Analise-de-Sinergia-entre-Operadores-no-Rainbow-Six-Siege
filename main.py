import os
import json
import pandas as pd
from itertools import combinations

def carregar_dados(arquivos_csv):
    """Carrega e concatena múltiplos arquivos CSV em um único DataFrame."""
    dados = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
    return pd.concat(dados, ignore_index=True)

def filtrar_dados(dados):
    """Filtra os dados com base em colunas relevantes, modos de jogo e ranks."""
    colunas_relevantes = [
        'gamemode', 'mapname', 'matchid', 'roundnumber', 'objectivelocation',
        'operator', 'team', 'haswon', 'skillrank'
    ]
    dados = dados[colunas_relevantes]
    dados = dados[dados['gamemode'] == 'BOMB']
    ranks_validos = {'Unranked', 'Copper', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond'}
    return dados[dados['skillrank'].isin(ranks_validos)]

def criar_combinacao_operadores(grupo):
    """Cria uma string única representando a combinação ordenada de operadores."""
    return ",".join(sorted(grupo))

def extrair_combinacoes_vencedoras(dados):
    """Agrupa dados vencedores e cria combinações de operadores."""
    grupos = dados[dados['haswon'] == 1].groupby(
        ['matchid', 'roundnumber', 'mapname', 'objectivelocation', 'team']
    )
    df_combinacoes = grupos['operator'].apply(list).reset_index()
    df_combinacoes['comb_operadores'] = df_combinacoes['operator'].apply(criar_combinacao_operadores)
    return df_combinacoes

def criar_tabela_nos(combinacoes):
    """Cria a tabela de nós com operadores únicos."""
    nos = combinacoes['operator'].explode().unique()
    nos_df = pd.DataFrame({'Label': nos})
    nos_df['Id'] = nos_df.index
    return nos_df

def criar_pastas(*pastas):
    """Cria diretórios se ainda não existirem."""
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)

def processar_grafos(combinacoes, nos_df, pasta_mapas, pasta_grafos):
    """Gera tabelas de arestas e grafos JSON para cada mapa e bomb site."""
    for (mapa, local_objetivo), grupo in combinacoes.groupby(['mapname', 'objectivelocation']):
        mapa_pasta = os.path.join(pasta_mapas, mapa)
        grafo_pasta = os.path.join(pasta_grafos, mapa)
        criar_pastas(mapa_pasta, grafo_pasta)

        arestas = []
        for _, row in grupo.iterrows():
            operadores = row['operator']
            for comb in combinations(sorted(operadores), 2):
                arestas.append({'operator1': comb[0], 'operator2': comb[1], 'objectivelocation': local_objetivo, 'frequencia': 1})

        if arestas:
            arestas_df = pd.DataFrame(arestas)
            arestas_frequentes = arestas_df.groupby(['operator1', 'operator2', 'objectivelocation'])['frequencia'].sum().reset_index()
            arestas_frequentes['Source'] = arestas_frequentes['operator1'].map(nos_df.set_index('Label')['Id'])
            arestas_frequentes['Target'] = arestas_frequentes['operator2'].map(nos_df.set_index('Label')['Id'])
            arestas_frequentes['Weight'] = arestas_frequentes['frequencia']

            caminho_arestas = os.path.join(mapa_pasta, f"{local_objetivo}_arestas.csv")
            arestas_frequentes[['Source', 'Target', 'Weight']].to_csv(caminho_arestas, index=False)

            grafo = {
                'nodes': [{'id': row['Id'], 'label': row['Label']} for _, row in nos_df.iterrows()],
                'edges': [{'source': row['Source'], 'target': row['Target'], 'weight': row['Weight']} for _, row in arestas_frequentes.iterrows()]
            }

            caminho_grafo = os.path.join(grafo_pasta, f"{local_objetivo}_location_graph.json")
            with open(caminho_grafo, 'w') as f:
                json.dump(grafo, f, indent=4)

def main():
    arquivos_csv = [
        "C:/Users/Bruno/Documents/Faculdade/Trabalho Final/bases/datadump_s5-000.csv",
        "C:/Users/Bruno/Documents/Faculdade/Trabalho Final/bases/datadump_s5-001.csv",
        "C:/Users/Bruno/Documents/Faculdade/Trabalho Final/bases/datadump_s5-002.csv"
    ]
    pasta_mapas, pasta_grafos = "mapas_arestas", "grafos_Json"
    criar_pastas(pasta_mapas, pasta_grafos)

    dados = carregar_dados(arquivos_csv)
    dados_filtrados = filtrar_dados(dados)
    combinacoes_vencedoras = extrair_combinacoes_vencedoras(dados_filtrados)
    nos_df = criar_tabela_nos(combinacoes_vencedoras)
    processar_grafos(combinacoes_vencedoras, nos_df, pasta_mapas, pasta_grafos)
    
    nos_df[['Id', 'Label']].to_csv('nos_gephi.csv', index=False)

if __name__ == "__main__":
    main()
