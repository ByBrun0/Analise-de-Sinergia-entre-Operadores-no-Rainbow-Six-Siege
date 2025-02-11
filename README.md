# Análise de Sinergia entre Operadores - Rainbow Six Siege

Este repositório contém um projeto de análise de sinergia entre operadores no jogo Rainbow Six Siege. O objetivo é explorar dados e identificar combinações eficazes de operadores para diferentes situações dentro do jogo.

## Requisitos

Antes de iniciar, certifique-se de ter o Python instalado em sua máquina.
O projeto utiliza bibliotecas específicas que devem ser instaladas antes da execução.

### Bibliotecas Necessárias
As seguintes bibliotecas são utilizadas no projeto e devem ser instaladas:

- os
- json
- pandas
- itertools
- networkx
- matplotlib
- seaborn

### Instalação

1. Clone este repositório:
```sh
git clone https://github.com/ByBrun0/Analise-de-Sinergia-entre-Operadores-no-Rainbow-Six-Siege.git
cd Analise-de-Sinergia-entre-Operadores-no-Rainbow-Six-Siege
```
2. Crie um ambiente virtual (opcional, mas recomendado):
```sh
python -m venv venv
source venv/bin/activate 
```
3. Instale as dependências necessárias:
```sh
pip install os json pandas networkx matplotlib seaborn
```

## Estrutura do Projeto
```sh
/
├── bases/          # Pasta onde os arquivos CSV devem ser armazenados
├── graficos_pagerank # Pasta onde as tabelas de PageRank serão armazenadas
├── grafos_Json  # Pasta onde os arquivos JSON serão armazenados
├── grafos_gephi  # Pasta onde os grafos criados no Gephi serão armazenados
├── grafos_imagens  # Pasta onde as imagens PNG dos grafos serão armazenadas
├── mapas_arestas  # Pasta onde os arquivos CSV devem ser armazenados
├── src/            # Código-fonte do projeto
│   ├── main.py # Código principal
│   ├── plotar_grafo.py # Script para plotar grafos
│   ├── plotar_tabela.py # Script para plotar tabelas
├── README.md       # Documentação do projeto
├── nos_gephi.csv  # Arquivo CSV dos NOS
├── Analise de Sinergia entre Operadores no Rainbow Six Siege usando Teoria dos Grafos.pdf # Artigo PDF
```
### Configuração dos Dados

1. Baixe os arquivos de dados do seguinte link: https://drive.google.com/drive/folders/1dEUP5TNT-aEXPiN9CATNGKMfBZk7g_cT?usp=drive_link .
2. Crie a pasta bases/ na raiz do projeto (caso ainda não exista).
3. Coloque os arquivos CSV baixados dentro da pasta bases/.

### Configuração de Caminhos

Antes de executar os scripts, altere os caminhos dos arquivos conforme seu diretório local:

- No *main.py*, altere a variável *arquivos_csv* para apontar para os arquivos corretos:
```sh
arquivos_csv = [
    "Caminho/para/seu/arquivo/bases/datadump_s5-000.csv",
    "Caminho/para/seu/arquivo/bases/datadump_s5-001.csv",
    "Caminho/para/seu/arquivo/bases/datadump_s5-002.csv"
]
```
- No *plotar_grafo.py*, defina os caminhos para os diretórios de saída:
```sh
PASTA_GRAFOS = "Caminho/para/seu/diretorio/grafos_Json"
PASTA_SAIDA_BASE = "Caminho/para/seu/diretorio/grafos_imagens"
```
- No *plotar_tabela.py*, configure os caminhos para as saídas das tabelas e análises:
```sh
PASTA_MAPAS = "Caminho/para/seu/diretorio/mapas_arestas"
PASTA_GRAFICOS = "Caminho/para/seu/diretorio/graficos_pagerank"
CAMINHO_NOS_GEPHI = "Caminho/para/seu/diretorio/nos_gephi.csv"
```

## Execução do Projeto

Com todas as dependências instaladas e os dados organizados, você pode executar os seguintes scripts na ordem:

1. Execute o script principal:
```sh
python src/main.py
```
2. Plote os grafos gerados:
```sh
python src/plotar_grafo.py
```
3. Plote as tabelas de análise:
```sh
python src/plotar_tabela.py
```
## Dúvidas

Caso tenha alguma dúvida ou precise de suporte, entre em contato:

- Nome: Bruno Prado Dos Santos
- Email: bruno.santos@aluno.cefetmg.br

