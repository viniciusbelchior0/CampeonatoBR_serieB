import pandas as pd
import numpy as np
import time
from sqlalchemy import create_engine

def coletar_estatisticas_serieb(id_squad, name_squad, ano):

  url_schedule = f"https://fbref.com/en/squads/{id_squad}/{ano}/matchlogs/c38/schedule/"
  time.sleep(4)
  url_shooting = f"https://fbref.com/en/squads/{id_squad}/{ano}/matchlogs/c38/shooting/"
  time.sleep(4)
  url_keeper = f"https://fbref.com/en/squads/{id_squad}/{ano}/matchlogs/c38/keeper/"
  time.sleep(4)
  url_misc = f"https://fbref.com/en/squads/{id_squad}/{ano}/matchlogs/c38/misc/"
  time.sleep(4)

  #Scores & Fixtures
  schedule = pd.read_html(url_schedule,header=0, attrs={'id':'matchlogs_for'})[0]
  schedule = schedule.drop(columns=['Match Report','Notes'])
  schedule['Round'] = schedule['Round'].str.replace("Matchweek", "")
  schedule['GDiff'] = schedule['GF'] - schedule['GA']
  schedule['idTeam'] = f"{id_squad}"
  schedule['Team'] = f"{name_squad}"
  schedule['Tournament'] = f"Campeonato Brasileiro - Série B - {ano}"
  schedule['Captain'] = schedule['Captain'].fillna("NA")
  schedule['Formation'] = schedule['Formation'].fillna("NA")
  schedule['Poss'] = schedule['Poss'].fillna(0)
  schedule['Attendance'] = schedule['Attendance'].fillna(0)
  schedule['Poss'] = schedule['Poss']/100
  schedule = schedule.astype({'Round': int, 'Poss':float}) #alterar as demais
  schedule['points'] = schedule['Result'].map({'W': 3, 'D': 1, 'L': 0})

  #Shooting
  shooting = pd.read_html(url_shooting,header=1, attrs={'id':'matchlogs_for'})[0]
  shooting = shooting[['Sh','SoT','SoT%','G/Sh','G/SoT','PK','PKatt']]
  shooting = shooting.fillna(0)
  shooting['SoT%'] = shooting['SoT%']/100
  shooting['PK%'] = shooting['PK']/shooting['PKatt']


  #Goalkeeping
  keeper = pd.read_html(url_keeper,header=1, attrs={'id':'matchlogs_for'})[0]
  keeper = keeper[['SoTA','Saves','Save%','CS','PKatt','PKsv']]
  keeper = keeper.rename(columns={'PKatt':'PKatt_A'})
  keeper = keeper.fillna(0)
  keeper['Save%'] = keeper['Save%']/100
  keeper['PKsv%'] = keeper['PKsv']/keeper['PKatt_A']


  #Miscellaneous
  misc = pd.read_html(url_misc,header=1, attrs={'id':'matchlogs_for'})[0]
  misc = misc[['CrdY','CrdR','2CrdY','Fls','Fld','Off','Crs','Int','TklW','OG']]
  misc = misc.fillna(0)

  new_df = pd.concat([schedule,shooting,keeper,misc],axis=1)
  new_df = new_df.fillna(0)

  #Ajustar os tipos de dados
  new_df[['Time','Round','Day','Venue','Result','Opponent','Captain','Formation','Referee','idTeam','Team','Tournament']] = new_df[['Time','Round','Day','Venue','Result','Opponent','Captain','Formation','Referee','idTeam','Team','Tournament']].astype(object)
  new_df[['GF','GA','Attendance','GDiff']] = new_df[['GF','GA','Attendance','GDiff']].astype(int)
  new_df[['Poss','SoT%','G/Sh','G/SoT','PK%','Save%','PKsv%']] = new_df[['Poss','SoT%','G/Sh','G/SoT','PK%','Save%','PKsv%']].astype(float)
  new_df['Date'] = pd.to_datetime(new_df['Date'], format='mixed')
  new_df = new_df.loc[new_df['Poss'] > 0]

  #Renomear as colunas
  novos_nomes = {'Date':'date','Time':'time','Round':'round','Day':'day','Venue':'venue','Result':'result','GF':'gf',\
  'GA':'ga','Opponent':'opponent','Poss':'possession','Attendance':'attendance','Captain':'captain',\
  'Formation':'formation','Referee':'referee','GDiff':'gdiff','idTeam':'idteam','Team':'team','Tournament':'tournament',\
  'Sh':'shots','SoT':'shotsontarget','SoT%':'p_shotsontarget','G/Sh':'goals_shots',\
  'G/SoT':'goals_shotsontarget','PK':'penalty_goals','PKatt':'penalty_attempted','PK%':'p_penaltyconverted',\
  'SoTA':'shotsontarget_against','Saves':'saves','Save%':'p_saves','CS':'cleansheets',\
  'PKatt_A':'penalty_attempted_against','PKsv':'penalty_saved','PKsv%':'p_penalty_saved',\
  'CrdY':'yellow_cards','CrdR':'red_cards','2CrdY':'two_yellow_cards',\
  'Fls':'fouls_commited','Fld':'fouls_draw','Off':'offsides','Crs':'crosses','Int':'interceptions','TklW':'tackles_won','OG':'own_goals'}

  new_df = new_df.rename(columns=novos_nomes)
  new_df = new_df[new_df['date'] > "1970-01-01"]#remover a linha total da tabela
  new_df['idgameteam'] = new_df['idteam'] + "_" + new_df['round'].astype(str) + "_" + new_df['tournament'].str[-4:]

  #Reorganizar as colunas
  new_df = new_df[['idgameteam','date','time','round','day','tournament','venue','idteam','team','opponent','result','points','gf','ga','possession','attendance','captain','formation','referee','gdiff','shots','shotsontarget','p_shotsontarget','goals_shots','goals_shotsontarget','penalty_goals','penalty_attempted','p_penaltyconverted','shotsontarget_against','saves','p_saves','cleansheets','penalty_attempted_against','penalty_saved','p_penalty_saved','yellow_cards','red_cards','two_yellow_cards','fouls_commited','fouls_draw','offsides','crosses','interceptions','tackles_won','own_goals']]
  time.sleep(8)

  return new_df

squads = {"712c528f":"Santos","ece66b78":"Sport-Recife","baa296ad":"Chapecoense","d2dc922e":"Operario",\
          "78c617cc":"Goias","1f68d780":"America-MG","d680d257":"Coritiba","b8daef43":"Brusque-Futebol-Clube",\
          "f050c492":"Vila-Nova","289e8847":"Mirassol-Futebol-Clube","7a1064a2":"Gremio-Novorizontino",\
          "3cc399a5":"Botafogo-SP","2f335e17":"Ceara","3c7dd952":"Amazonas-FC","7fcb6e83":"CRB","81f8aeb6":"Paysandu",\
          "b162ebe7":"Ponte-Preta","f205258a":"Avai","341d7cb0":"Guarani","62d22efa":"Ituano"} #definir os times para coletar os dados

#colunas reordenadas
df = pd.DataFrame(columns = ['idgameteam','date','time','round','day','tournament','venue','idteam','team','opponent','result','points','gf','ga','possession','attendance','captain','formation','referee','gdiff','shots','shotsontarget','p_shotsontarget','goals_shots','goals_shotsontarget','penalty_goals','penalty_attempted','p_penaltyconverted','shotsontarget_against','saves','p_saves','cleansheets','penalty_attempted_against','penalty_saved','p_penalty_saved','yellow_cards','red_cards','two_yellow_cards','fouls_commited','fouls_draw','offsides','crosses','interceptions','tackles_won','own_goals'])

for id_squad, name_squad in squads.items():
   new_df = coletar_estatisticas_serieb(id_squad, name_squad,"2024")
   df = pd.concat([df,new_df],ignore_index=True)

#Inserindo os dados
def ingerir_dados_serieb(df):
    engine = create_engine('postgresql://postgres:admin@localhost:5432/teste_dados_r')
    
    #Obtendo as partidas ainda não adicionadas
    query = "SELECT * FROM (SELECT *, ROW_NUMBER() OVER () AS row FROM campeonatobr_serieb) sub ORDER BY row DESC LIMIT 760"
    all_matches = pd.read_sql_query(query,engine)
    all_matches = all_matches[['idgameteam']]

    #Anti-join
    outer = df.merge(all_matches, on='idgameteam', how='left', indicator=True)
    df_db = outer[outer['_merge'] == 'left_only'].drop(columns='_merge')

    if not df_db.empty:
      df_db.to_sql('campeonatobr_serieb',con=engine,if_exists='append',index=False)
      print("Dados inseridos com sucesso!")
    else:
      print("Sem partidas recentes. Nenhum dado foi inserido.")

ingerir_dados_serieb(df)