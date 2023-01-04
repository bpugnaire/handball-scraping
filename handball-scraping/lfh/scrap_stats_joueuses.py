import http.client
import zlib
import json
import pandas as pd
import time

UNIVERS = ['107982','108094']

conn = http.client.HTTPSConnection("api.ligue-feminine-handball.fr")

payload = ""

headers = { 'Accept-Encoding': "gzip, deflate, br" }

for i in range(len(UNIVERS)):

    conn.request("GET", f"/player-stat?competitionId={UNIVERS[i]}&page=1&sort=totalGoals&desc=totalGoals&limit=5000", payload, headers)

    res = conn.getresponse()
    data = res.read()

    data = zlib.decompress( data , zlib.MAX_WBITS | 32).decode('utf-8')

    obj = json.loads(data)
    df = pd.DataFrame(obj['docs'])
    if i == 0:
        filename = 'data/D1F/stats_joueuses_D1F_2022-23.csv'
    else :
        filename = 'data/D2F/stats_joueuses_D2F_2022-23.csv'
    df.to_csv(filename)
    time.sleep(2)