import pandas as pd
import re
from unidecode import unidecode

def last_capital_letter(word):
    for i in range(len(word)-1, -1,-1):
        if (word[i].isupper()) :
            return i
    return 0

def first_digit(word):
    for i in range(len(word)-1):
        if (word[i].isdigit()) and not (word[i+1].isdigit()):
            return i+1
    return 0

def upperify_accents(word):
    word = list(word)
    for i in range(1,len(word)-1):
        if not word[i].isupper() and (word[i-1].isupper() and (word[i+1].isupper() or word[i+1]==' ')):
            word[i] = word[i].upper()
    return "".join(word)

def reformate_stats_gardien(row):
    joueur = row['joueurs']
    joueur = upperify_accents(joueur)
    try:
        debut_prenom = next(re.finditer('([A-ZÀ-Ú][a-zá-ú])', joueur)).start(0)
        prenom = unidecode(joueur[debut_prenom:])
        nom = unidecode(joueur[first_digit(joueur):debut_prenom-1]).upper()
    except:
        prenom = ''
        nom = ''
    matchs = row['mj']
    #total arrets
    x = row["total  arrêts"].split('/') 
    arrets_total = x[0].strip()
    occasion_total = x[1].strip()
    pourcentage_arrets = row['%  total'].split(' ')[0].strip().replace(',','.')
    total_arret_match = str(row['total  arrêts / mj']/100)
    #arrets sur tir
    x = row['arrêts  tirs'].split('/')
    arrets_tirs = x[0].strip()
    tirs_total = x[1].strip()
    pourcentage_arrets_tirs = row['%  tirs'].split(' ')[0].strip().replace(',','.')
    total_arret_tirs_match = str(row['arrêts  tirs / mj']/100)
    #arrets sur penalty
    x = row['arrêts  penalty'].split('/')
    arrets_penalty = x[0].strip()
    penalty_total = x[1].strip()
    pourcentage_arrets_penalty = row['%  penalty'].split(' ')[0].strip().replace(',','.')
    total_arret_penalty_match = str(row['arrêts  penalty / mj']/100)
    return [prenom,nom,matchs,arrets_total,occasion_total,pourcentage_arrets,total_arret_match,arrets_tirs,
    tirs_total,pourcentage_arrets_tirs,total_arret_tirs_match,arrets_penalty,penalty_total,
    pourcentage_arrets_penalty,total_arret_penalty_match]

def reformate_stats_joueurs(row):
    joueur = row['joueurs']
    joueur = upperify_accents(joueur)
    try:
        debut_prenom = next(re.finditer('([A-ZÀ-Ú][a-zá-ú])', joueur)).start(0)
        prenom = unidecode(joueur[debut_prenom:])
        nom = unidecode(joueur[first_digit(joueur):debut_prenom-1]).upper()
    except:
        prenom = ''
        nom = ''
    
    matchs = row['mj']
    #total arrets
    x = row["total  buts"].split('/') 
    but_total = x[0].strip()
    occasion_total = x[1].strip()
    pourcentage_buts = row['%  total'].split(' ')[0].strip().replace(',','.')
    total_but_match = str(row['total  buts / mj']/100)
    #arrets sur tir
    x = row['buts  tirs'].split('/')
    arrets_tirs = x[0].strip()
    tirs_total = x[1].strip()
    pourcentage_arrets_tirs = row['%  tirs'].split(' ')[0].strip().replace(',','.')
    total_arret_tirs_match = str(row['tirs  buts / mj']/100)
    #arrets sur penalty
    x = row['buts  penalty'].split('/')
    arrets_penalty = x[0].strip()
    penalty_total = x[1].strip()
    pourcentage_arrets_penalty = row['%  penalty'].split(' ')[0].strip().replace(',','.')
    total_arret_penalty_match = str(row['penalty  buts / mj']/100)
    return [prenom,nom,matchs,but_total,occasion_total,pourcentage_buts,total_but_match,arrets_tirs,
    tirs_total,pourcentage_arrets_tirs,total_arret_tirs_match,arrets_penalty,penalty_total,pourcentage_arrets_penalty,total_arret_penalty_match]

YEAR = ['2004-05','2005-06','2006-07','2007-08','2008-09','2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
LIGUE = ['D1H','D2H']

df_columns_gardiens = ['prenom','nom','match_joues','total_arrets','total_occasions','pourcentage_arrets','arrets/match','arrets_tirs',
    'total_tirs','pourcentage_arrets_tirs','arrets_tirs/match','arrets_penalty','total_penalty','pourcentage_arrets_penalty','arrets_penalty/match']

df_columns_joueurs = ['prenom','nom','match_joues','total_buts','total_occasions','pourcentage_buts','buts/match','buts_tirs',
    'total_tirs','pourcentage_buts_tirs','buts_tirs/match','buts_penalty','total_penalty','pourcentage_buts_penalty','buts_penalty/match']

for l in LIGUE:
    for y in YEAR:
        try:
            filepath = f'data/RAW/{l}/stats_gardiens_{y}.csv'
            df = pd.read_csv(filepath)
            df_result = df.apply(reformate_stats_gardien,axis=1,result_type='expand')
            df_result.columns = df_columns_gardiens
            filepath = f'data/FORMATED/{l}/stats_gardiens_{y}.csv'
            df_result.to_csv(filepath)
            filepath = f'data/RAW/{l}/stats_joueurs_{y}.csv'
            df = pd.read_csv(filepath)
            df_result = df.apply(reformate_stats_joueurs,axis=1,result_type='expand')
            df_result.columns = df_columns_joueurs
            filepath = f'data/FORMATED/{l}/stats_joueurs_{y}.csv'
            df_result.to_csv(filepath)
        except :
            pass

