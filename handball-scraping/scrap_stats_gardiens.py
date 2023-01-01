import pandas as pd
from bs4 import BeautifulSoup
import http.client
import time
import zlib

YEAR = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
UNIVERS = ['d1-26623','d2-25326']

conn = http.client.HTTPSConnection("www.lnh.fr")

for i in range(28,35):
    payload = f"seasons_id={i}&positions_name=Gardien&orderby=stats_total_stopped&type=gardiens&univers={UNIVERS[1]}&pagination-items=500&contents_controller=sportsPlayersStats&contents_action=index_ajax"

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
    result[0].to_csv(f'data/proligue/stats_gardiens_proligue_{YEAR[i-24]}.csv')
    time.sleep(2)
    