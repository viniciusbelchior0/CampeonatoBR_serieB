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
  all_matches['idteamgame'] = all_matches['team'] + "_" + all_matches['round'].astype(str) + '.0' + '_' + all_matches['tournament'].str[-4:]
  return all_matches


def obter_df_modelagem(df,janela):
    df = df[['round','team','tournament','opponent','result','venue','points','gf','ga','possession','gdiff','shots','p_shotsontarget','goals_shots','penalty_goals','p_penaltyconverted','shotsontarget_against','p_saves','cleansheets','penalty_attempted_against','p_penalty_saved','yellow_cards','red_cards','fouls_commited','fouls_draw','offsides','crosses','interceptions','tackles_won','own_goals']]
    df['cardscore'] = df['yellow_cards'] + df['red_cards']*5
    df['foulsdiff'] = df['fouls_draw'] - df['fouls_commited']
    df['tournament'] = df['tournament'].str[-4:]
    df['idteamgame'] = df['team'] + "_" + df['round'].astype(str) + "_" + df['tournament']
    df['idopponentgame'] = df['opponent'] + "_" + df['round'].astype(str) + "_" + df['tournament']
    df['idopponentgame'] = df['idopponentgame'].str.replace(' ','-')
    df['idopponentgame'] = df['idopponentgame'].str.replace('(','')
    df['idopponentgame'] = df['idopponentgame'].str.replace(')','')
    df['idopponentgame'] = df['idopponentgame'].str.replace('á','a')
    df['idopponentgame'] = df['idopponentgame'].str.replace('é','e')
    df['idopponentgame'] = df['idopponentgame'].str.replace('í','i')

    times = df[['team','tournament','round','venue','result','idteamgame','idopponentgame']].sort_values(by=['team','tournament'])
    times = times.reset_index().rename(columns={"index":"level_2"})

    #Obtendo valores agregados em séries temporais
    rolling_stats = (df.groupby(['team','tournament'])
                                            .apply(lambda x: x.rolling(window=janela).agg({'points':'sum','gf':'mean','ga':'mean','possession':'mean','gdiff':'sum','shots':'mean','p_shotsontarget':'mean','goals_shots':'mean','penalty_goals':'sum','p_penaltyconverted':'mean','shotsontarget_against':'mean','p_saves':'mean','cleansheets':'sum','penalty_attempted_against':'sum','p_penalty_saved':'mean','cardscore':'mean','foulsdiff':'mean','offsides':'mean','crosses':'mean','interceptions':'mean','tackles_won':'mean','own_goals':'sum'}).shift())).reset_index()

    rolling_stats = rolling_stats.drop(['team','tournament'], axis = 1)

    #Unindo os dados
    df_modelagem = times.merge(rolling_stats, on = 'level_2')

    df_modelagem2 = df_modelagem.drop(columns=['level_2','team','tournament','round','venue','result','idopponentgame'], axis=1)

    df_modelagem2 = df_modelagem2.rename(columns={'idteamgame':'idopponentgame','points':'opp_points','gf':'opp_gf','ga':'opp_ga','possession':'opp_possession','gdiff':'opp_gdiff','shots':'opp_shots',\
                                        'p_shotsontarget':'opp_p_shotsontarget','goals_shots':'opp_goals_shots','penalty_goals':'opp_penalty_goals',\
                                        'p_penaltyconverted':'opp_p_penaltyconverted','shotsontarget_against':'opp_shotsontarget_against',\
                                        'p_saves':'opp_p_saves','cleansheets':'opp_cleansheets','penalty_attempted_against':'opp_penalty_attempted_against',\
                                        'p_penalty_saved':'opp_p_penalty_saved','cardscore':'opp_cardscore','foulsdiff':'opp_foulsdiff',\
                                        'offsides':'opp_offsides','crosses':'opp_crosses','interceptions':'opp_interceptions',\
                                        'tackles_won':'opp_tackles_won','own_goals':'opp_own_goals'})

    df_modelagem = df_modelagem.merge(df_modelagem2, on='idopponentgame')
    df_modelagem = df_modelagem.dropna()
    df_modelagem = df_modelagem[df_modelagem['possession']>0]

    df_modelagem = df_modelagem[['idteamgame','idopponentgame','tournament','venue','result','points','gf','ga','possession','gdiff','shots',\
                                    'p_shotsontarget','goals_shots','penalty_goals','p_penaltyconverted','shotsontarget_against',\
                                                                'p_saves','cleansheets','penalty_attempted_against','p_penalty_saved','cardscore',\
                                                                'foulsdiff','offsides','crosses','interceptions','tackles_won','own_goals',\
                                                                'opp_points','opp_gf','opp_ga','opp_possession','opp_gdiff','opp_shots','opp_p_shotsontarget',\
                                                                'opp_goals_shots','opp_penalty_goals','opp_p_penaltyconverted','opp_shotsontarget_against',\
                                                                'opp_p_saves','opp_cleansheets','opp_penalty_attempted_against','opp_p_penalty_saved','opp_cardscore',\
                                                                'opp_foulsdiff','opp_offsides','opp_crosses','opp_interceptions','opp_tackles_won','opp_own_goals']]

    return df_modelagem


def consolidar_dados(df,ano):
    #Obtendo as partidas já modeladas
    query_2 = f"""SELECT * FROM campeonatobr_serieb_modelagem WHERE tournament = '{ano}' """
    mod_matches = pd.read_sql_query(query_2,engine)
    mod_matches = mod_matches[['idteamgame']]

    #Anti-join
    outer = df.merge(mod_matches, on='idteamgame', how='left', indicator=True)
    df_db = outer[outer['_merge'] == 'left_only'].drop(columns='_merge')
    return df_db


def inserir_dados(df):
    if not df.empty:
            df.to_sql('campeonatobr_serieb_modelagem',con=engine,if_exists='append',index=False)
            print("Dados inseridos com sucesso!")
    else:
            print("Sem partidas recentes. Nenhum dado foi inserido.")

engine = conectar_banco()
dados = obter_dados(2024)
dados_modelagem = obter_df_modelagem(dados,5)
dados = consolidar_dados(dados_modelagem,2024)
inserir_dados(dados)
