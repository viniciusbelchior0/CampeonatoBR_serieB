import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:admin@localhost:5432/teste_dados_r')
    
#Obtendo as partidas ainda não adicionadas
query = "SELECT * FROM  campeonatobr_serieb WHERE EXTRACT(year FROM date) = 2024"
all_matches = pd.read_sql_query(query,engine)

all_matches.to_excel("dados_planilha.xlsx")