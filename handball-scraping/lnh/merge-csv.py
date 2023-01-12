import pandas as pd

YEAR = ['2004-05','2005-06','2006-07','2007-08','2008-09','2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
LIGUE = ['D1H','D2H']

df_info = []
df_stat_joueurs = []
df_stat_gardiens = []

for l in LIGUE:
    for y in YEAR:
        try:
            filepath = f'data/FORMATED/{l}/joueurs_{y}.csv'
            df = pd.read_csv(filepath,index_col=[0])
            df['saison'] = y
            df['ligue'] = l
            if len(df_info) == 0:
                df_info = df
            else:
                df_info = pd.concat([df_info,df])
        except:
            pass

for l in LIGUE:
    for y in YEAR:
        try:
            filepath = f'data/FORMATED/{l}/stats_joueurs_{y}.csv'
            df = pd.read_csv(filepath,index_col=[0])
            df['saison'] = y
            df['ligue'] = l
            if len(df_stat_joueurs) == 0:
                df_stat_joueurs = df
            else:
                df_stat_joueurs = pd.concat([df_stat_joueurs,df])
        except:
            pass

for l in LIGUE:
    for y in YEAR:
        try:
            filepath = f'data/FORMATED/{l}/stats_gardiens_{y}.csv'
            df = pd.read_csv(filepath,index_col=[0])
            df['saison'] = y
            df['ligue'] = l
            if len(df_stat_gardiens) == 0:
                df_stat_gardiens = df
            else:
                df_stat_gardiens = pd.concat([df_stat_gardiens,df])
        except:
            pass

df_info.to_csv('data/MERGED/joueurs_lnh.csv')
df_stat_joueurs.to_csv('data/MERGED/stats_joueurs_lnh.csv')
df_stat_gardiens.to_csv('data/MERGED/stats_gardiens_lnh.csv')