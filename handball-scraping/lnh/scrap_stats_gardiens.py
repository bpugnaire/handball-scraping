import pandas as pd
from bs4 import BeautifulSoup
import http.client
import time
import zlib


SEASON_ID = [4,5,6,7,8,2,1,3]
YEAR = ['2004-05','2005-06','2006-07','2007-08','2008-09','2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
UNIVERS = ['d1-26623','d2-25326']
LIGUE = ['D1H','D2H']

conn = http.client.HTTPSConnection("www.lnh.fr")

for u in UNIVERS:
    if u == 'd1-26623':
        x = 0
        start_id = 16
    else:
        x = 1
        start_id = 28
    for i in range(start_id ,35):
        if i <24:
            season_id = SEASON_ID[i-16]
        else:
            season_id = i
        payload = f"seasons_id={season_id}&positions_name=Gardien&orderby=stats_total_stopped&type=gardiens&univers={u}&pagination-items=500&contents_controller=sportsPlayersStats&contents_action=index_ajax"

        headers = {
            'cookie': "PHPSESSID=stj9tts0qaq9ovtf009flrb8ta",
            'Accept-Encoding': "gzip, deflate, br",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
            }

        conn.request("POST", "/ajaxpost1", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = zlib.decompress( data , zlib.MAX_WBITS | 32).decode('utf-8')


        # Parse the html file
        soup = BeautifulSoup(data, 'html.parser')

        # Format the parsed html file
        strhtm = soup.prettify()
        result = pd.read_html(strhtm)

        result[0].to_csv(f'data/RAW/{LIGUE[x]}/stats_gardiens_{YEAR[i-16]}.csv')
        time.sleep(2)
    