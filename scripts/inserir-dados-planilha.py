#Script para inserção dos dados na planilha que fornece os dados para o modelo de ML do repositório ML_CampeonatoBrasileiro
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def conectar_banco():
    engine = create_engine('postgresql://postgres:admin@localhost:5432/teste_dados_r')
    return engine

def obter_dados(ano):
    #Obtendo as partidas
    query = f"""SELECT * FROM campeonatobr_serieb WHERE EXTRACT(YEAR from date) = '{ano}' """
    all_matches = pd.read_sql_query(query,engine)
    return all_matches

engine = conectar_banco()
dados = obter_dados(2024)
dados.to_excel("dados_planilha.xlsx")


