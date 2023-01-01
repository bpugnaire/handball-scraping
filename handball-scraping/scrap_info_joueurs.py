import pandas as pd
from bs4 import BeautifulSoup
import http.client
import time
import zlib

YEAR = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
COHORTE = ['PRO', 'CF', 'RES']
UNIVERS = ['d1-26623','d2-25326']
def first_capital_letter(word):
    for i in range(0, len(word)) :
        if (word[i].isupper()) :
            return i
    return 0

def last_capital_letter(word):
    for i in range(len(word)-1, -1,-1):
        if (word[i].isupper()) :
            return i
    return 0

def extract_name(word):
    i = first_capital_letter(word)
    j = last_capital_letter(word)
    return word[i:j+1]

def extract_poste(poste):
    mot1 = poste.string.split(' ')[12]
    mot2 = poste.string.split(' ')[13]
    if mot2 == '':
        return mot1
    else:
        return mot1 + " " + mot2 

def get_player_info_df(data, cohorte): 
    soup = BeautifulSoup(data, 'html.parser')

    postes = soup.find_all('div', class_="description")
    names = soup.find_all('div', class_="name")
    numbers = soup.find_all('div', class_="number")
    equipes = soup.find_all('div', class_="col-infos")
    photos = soup.find_all('div', class_="col-picture")

    postes_list = []
    names_list = []
    numbers_list = []
    equipes_list = []
    photos_list = []

    for i in range(len(postes)):
        postes_list.append(extract_poste(postes[i]))
        names_list.append(extract_name(names[i].string) )
        numbers_list.append(numbers[i].string.split('#')[1].split(' ')[0])
        equipes_list.append(equipes[i].find('img', alt=True)['alt'].split('équipe')[1][1:])
        photos_list.append(photos[i].get('style').split('(')[1].split(')')[0])

    result_df = pd.DataFrame({
        'prenom_nom' : names_list,
        'poste' : postes_list,
        'numero' : numbers_list,
        'equipe' : equipes_list,
        'photo_url' : photos_list })
    result_df['cohorte'] = cohorte
    return result_df

conn = http.client.HTTPSConnection("www.lnh.fr")


for i in range(24,35):
    df = []
    for coh in COHORTE:
        payload = f"seasons_id={i}&players_groups_slug={coh}&search=&pagination-items=5000&teams_id=all&pagination-current=1&univers={UNIVERS[1]}&contents_controller=sportsPlayers&contents_action=index_ajax"

        headers = {
            'cookie': "PHPSESSID=stj9tts0qaq9ovtf009flrb8ta",
            'Accept-Encoding': "gzip, deflate, br",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
            }

        conn.request("POST", "/ajaxpost1", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = zlib.decompress( data , zlib.MAX_WBITS | 32).decode('utf-8')
        player_info_df = get_player_info_df(data, coh)
        if len(df) == 0:
            df = player_info_df
        else:
            df = pd.concat([df,player_info_df])
    df.to_csv(f'data/proligue/joueurs_proligue_{YEAR[i-24]}.csv')
    time.sleep(2)


