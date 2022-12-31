import pandas as pd
from bs4 import BeautifulSoup
import http.client
import time

conn = http.client.HTTPSConnection("www.lnh.fr")

year = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23']
for i in range(24,35):
    payload = f"seasons_id={i}&positions_name=all&orderby=stats_total_goals&type=joueurs&pagination-items=5000&pagination-current=1&contents_controller=sportsPlayersStats&contents_action=index_ajax"

    headers = {
        'cookie': "PHPSESSID=stj9tts0qaq9ovtf009flrb8ta",
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"
        }

    conn.request("POST", "/ajaxpost1", payload, headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")

    # Parse the html file
    soup = BeautifulSoup(data, 'html.parser')

    # Format the parsed html file
    strhtm = soup.prettify()
    result = pd.read_html(strhtm)
    result[0].to_csv(f'stats_joueurs_lnh_{year[i-24]}.csv')
    time.sleep(2)
    