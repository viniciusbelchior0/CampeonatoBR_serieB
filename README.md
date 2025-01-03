# CampeonatoBR_serieB
## 1. Descrição do Projeto

O próposito do projeto é a construção de um pipeline completo de uma aplicação de dados. Começando pela coleta dos resultados das partidas através de webscraping, esses dados serão armazenados em um banco de dados, que os servirá a um relatório interativo e a uma aplicação com o objetivo de prever o resultado de uma partida com base nos resultados recentes das equipes.

![pipeline](https://github.com/viniciusbelchior0/CampeonatoBR_serieB/blob/main/references/diagrama_br-serieb.png)

**Entregáveis**:
- Scripts para coleta e ingestão de dados (*Pipeline* de dados).
- Elaboração de Banco de Dados para armazenamento das informações.
- Relatórios para visualização e análise de dados (*Dashboards*).
- Aplicação para predição do resultado de uma partida.

**Status do projeto**:
- Etapas concluídas: códigos para coleta e ingestão de dados, códigos para elaboração do banco de dados, prótotipos dos relatórios (dashboards).
- Futuros desenvolvimentos: 

**Stack (tecnologias e ferramentas utilizadas)**
- Programação e códigos para coleta de dados: `Python` (e bibliotecas listadas `requirements.txt`);
- Banco de Dados: `PostgreSQL`;
- Relatórios: `PowerBI` e `Figma` (elaboração da interface do relatório).
- Aplicação: `Streamlit` (hospedagem da aplicação desenvolvida em python) e `Google Sheets` (armazenamento dos dados para consumo pela aplciação.)


**Obs**: a aplicação pode ser encontrada em outro [repositório](https://github.com/viniciusbelchior0/ML_CampeonatoBrasileiro).

## 2. Descrição das etapas
### 2.1 - Obtenção dos dados

A primeira fase se trata da obtenção dos dados. Eles são coletados através do site FBRef - que faz parte de uma família de endereços(sports reference) que contêm diversas estatísticas referentes às partidas das principais ligas esportivas do mundo. Esses dados estão dispostos em diferentes tabelas contendo informações a respeito de calendários, estatísticas ofensivas, estatísticas defensivas e outras medidas; eles também são granularizados por partida: cada linha se refere a uma partida. Além disso, deve-se reunir essas tabelas para um mesmo time e depois disso, coletar essas tabelas para todos os 20 times. Caso isso fosse feito manualmente, despenderia muito trabalho e tempo, podendo levar algumas horas para atualizações referentes a uma única rodada.

Com a utilização das bibliotecas `pandas` e `numpy`, o processo de automatização da extração pode ser desenvolvido. Através de requisições à página da web, esses dados são obtidos já em formato tabular (dataframe), bastando apenas dar prosseguimento às etapas de limpeza dos dados, criação de novas medidas e posterior união das tabelas. Esses dados serão armazenados um banco de dados `PostgreSQL`. Ademais, esse fluxo pode ser orquestrado utilizando o apache airflow (e semelhantes), para que seja executado sempre em datas posteriores a realização das partidas, usualmente as terças-feiras e aos sábados.

### 2.2 - Modelagem Preditiva

Para realizar a predição dos resultados,devemos analisar o passado para estimar o futuro. Assim, aquela tabela de resultados deverá passar por transformações para que possamos obter informações referentes à performance recente de cada equipe; para sua obtenção, calcularemos as médias e soma móveis das últimas 5 rodadas. Esse processo também será realizado utilizando as bibliotecas `pandas` e `numpy`, bem como os dados também serão armazenados em um banco de dados `PostgreSQL`.

Esses dados servirão de insumo para a realização de modelagem preditiva utilizando técnicas de machine learning, como as *random forests*. O processo de modelagem envolve a divisão da base de dados - treino, teste e validação - para estimação e avaliação do modelo, bem como a utilização de métricas avaliativas para problemas de classificação, como *accuracy* e *f1-score*. Foram desenvolvidas duas abordagens para o problema: a predição do resultado geral - vitória, empate ou derrota - ou três predições distintas - um para vitório, outro para empate e outro para derrota. Posteriormente, a abordagem com melhores resultados terá seu(s) modelo(s) submetidos à etapa de otimização de hiperparâmetros. Todas essas etapas referentes à modelagem preditiva serão realizadas utilizando a biblioteca `scikit-learn`.


### 2.3 - Implantação

O projeto contará com dois entregáveis: uma relatório dinâmico dos resultados e uma aplicação web para predição dos resultados de futuras partidas.

Os relatório dinâmicos, comumente chamados de dashboards, são painéis que disponibilizam informações mutáveis, possíveis de serem analisadas através de filtros e parâmetros utilizados pelo usuário. Esse relatório é desenvolvido em `PowerBI`, e utilizará as informações da tabela dos resultados das partidas. 

A aplicação, por sua vez, utilizará o(s) modelo(s) estimado na fase de modelagem preditiva - sendo a abordagem de três modelos a escolhida - em uma interface web com parâmetros selecionados pelo usuário. Assim, três parâmetros - rodada, time da casa, time visitante - serão utilizados para a predição de uma nova partida. Essa aplicação é construída utilizando a biblioteca `streamlit`, que facilita a construção da estrutura front-end, e o modelo é disponibilizado através da serialização com a biblioteca joblib.

### 2.4 - Resultados e comentários

Os resultados podem ser considerados favoráveis. A automação da coleta de dados e sua disponibilização em uma interface gráfica resulta em enorme facilidade prática para os entusiastas do campeonato, permitindo a condução de análises de maneira facilitada. A respeito da aplicação, sua construção é um exercício interessante e agregador, no entanto, os dados coletados não apresentaram um resultado plenamente satisfatório para a predição das partidas, que pode tornar seu uso algo errôneo para a obtenção de informações.

O projeto possui amplas possibilidades de extensão. Dados de outras fontes podem ser consolidados e inseridos como complemento aos já utilizados. Novas transformações podem ser realizadas nas estatísticas de dados para a obtenção de informações de maior qualidade para a estimação de resultados futuros. A aplicação também pode ser otimizada com a utilização de conceitos de *MLOps*, como CI/CD, treino e teste automatizados e monitoramento do modelo.

## 3. Descrição dos Arquivos e das Pastas

- **dados**: pasta contendo os dados das partidas extraídos do banco de dados. 
- **dashboard**: pasta contendo os arquivos para a elaboração do relatório (dashboard). Possui o relatório elaborado no PowerBI no arquivo `cbr_dashboard.pbix`, e a interface das páginas utilizadas no relatório nos arquivos `cbr_*.png`.
- **modelagem_banco**: pasta contendo os códigos para elaboração das tabelas do banco de dados. O arquivo `criar_banco_campenatobr_serieb.sql` contém o script para criação da tabela contendo as estatísticas das partidas e o arquivo `criar_banco-serieb_modelagem.sql` contém o script para a criação da tabela contendo os dados transformados para a realização de modelagem de técnicas de ML. O arquivo `erd_bd_cbr.png` apresenta o diagrama entidade relacionamento das tabelas.
- **notebooks**: pasta contendo os rascunhos/protótipos dos códigos, no formato de jupyter notebooks.
- **references**: pasta contendo informações e referências ao projeto.
- **scripts**: pasta contendo os códigos para extração, transformação e ingestão dos dados.
- *ingestao-transformacao_dados_modelagem.py*: script contendo o código para coleta das estatísticas e inserção no banco de dados. Este arquivo é o mesmo disponível na pasta `scripts`. É o script para ser utilizado em produção.
- *ingestao_dados_serieb.py*: script contendo o código para adaptação dos dados ao formato adequado para realização de modelagem de técnicas de ML. Este arquivo é o mesmo disponível na pasta `scripts`. É o script para ser utilizado em produção.
- *requirements.txt*: listagem das bibliotecas e suas respectivas versão utilizadas no projeto.

## 4. Exemplos

![dashboard](https://github.com/viniciusbelchior0/CampeonatoBR_serieB/blob/main/references/dashboard_screenshot.PNG)
*(Exemplo de uma página da dashboard)*

![aplicação](https://github.com/viniciusbelchior0/CampeonatoBR_serieB/blob/main/references/aplicacao_screenshot.PNG)
*(Exemplo da página da [aplicação: prevendo uma partida do campeonato brasileiro série B](https://mlcampeonatobrasileiro-serieb.streamlit.app/))*

