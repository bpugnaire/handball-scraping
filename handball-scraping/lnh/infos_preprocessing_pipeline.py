import pandas as pd
import re
from unidecode import unidecode


def upperify_accents(word):
    word = list(word)
    for i in range(1,len(word)-1):
        if not word[i].isupper() and (word[i-1].isupper() and (word[i+1].isupper() or word[i+1]==' ')):
            word[i] = word[i].upper()
    return "".join(word)

def formate_prenom_nom(row):
    joueur = row['prenom_nom']
    joueur = upperify_accents(joueur)
    try:
        debut_nom = next(re.finditer('([A-ZÀ-Ú][A-ZÀ-Ú])', joueur)).start(0)
        nom = unidecode(joueur[debut_nom:]).upper()
        prenom = unidecode(joueur[:debut_nom-1])
    except:
        prenom = ''
        nom = ''
    return [prenom,nom]

YEAR = ['2004-05','2005-06','2006-07','2007-08','2008-09','2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
LIGUE = ['D1H','D2H']


for l in LIGUE:
    for y in YEAR:
        try:
            filepath = f'data/RAW/{l}/joueurs_{y}.csv'
            df = pd.read_csv(filepath)
            df[['prenom','nom']] = df.apply(formate_prenom_nom,axis=1, result_type = 'expand')
            df = df.drop(columns =['Unnamed: 0'])
            filepath = f'data/FORMATED/{l}/joueurs_{y}.csv'
            df.to_csv(filepath)
        except Exception as e:
            print(e)
            pass

