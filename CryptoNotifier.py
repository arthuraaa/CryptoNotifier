#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 23:59:02 2021

@author: arthur
"""

from pycoingecko import CoinGeckoAPI
import time
import json
from datetime import date,  datetime


l = []
ll = []
try:
    with open('history.txt', 'r') as filehandle:
        for line in filehandle:
            el = json.loads(line)
            delatime = datetime.now() - datetime.strptime(el["time"], '%Y-%m-%d %H:%M:%S.%f')
            #print("delattime:", delatime)
            if delatime.seconds <= 24 * 60 * 60:
                l.append(json.loads(line))
except Exception as E:
    print("error listfile: ", E)
cg = CoinGeckoAPI()

tokens = ['bitcoin', 'litecoin', 'ethereum']

print('History OK')
while 1:
    
    prices = cg.get_price(ids=tokens, vs_currencies='usd')
    current_time = datetime.now()
    prices.update({"time":str(current_time)})
    l.append(prices)
    if (len(l) >= 1500):
        l.pop(0)
    with open('history.txt', 'a+') as filehandle:
        filehandle.write(json.dumps(prices, default=str) + "\n")
        
    for el in l:
        dtime = current_time - datetime.strptime(el["time"], '%Y-%m-%d %H:%M:%S.%f')
        #print(dtime.seconds)
        if dtime.seconds > 3550 and dtime.seconds < 4650: #1h 3200 et 4000 
            #print(el)
            for tok in tokens:
                #if ll[current_time] - dtime <= 3600 
                if len([item for item in ll if item[1]== tok and (current_time - item[0]).seconds < 1800]) == 0:
                    pourcentage=prices[tok]["usd"]/el[tok]["usd"]
                    if pourcentage <= 0.7:
                        print("chute de -"+ str(round((1-pourcentage)*100,4)) +"% en 1h sur ", tok)
                        ll.append((current_time,tok))
                        #print(dtime.seconds)
                    if pourcentage >= 1.3:
                        print("monte de +"+ str(round((pourcentage -1)*100,4)) +"% en 1h sur", tok)
                        ll.append((current_time,tok))
        if dtime.seconds > 10400 and dtime.seconds < 11200: #3h avec 6 minutes 40 d'intervale 
            #print(el)
            for tok in tokens:
                #if ll[current_time] - dtime <= 3600 
                if len([item for item in ll if item[1]== tok and (current_time - item[0]).seconds < 1800]) == 0:
                    pourcentage=prices[tok]["usd"]/el[tok]["usd"]
                    if pourcentage <= 0.65:
                        print("chute de -"+ str(round((1-pourcentage)*100,4)) +"% en 3h sur ", tok)
                        ll.append((current_time,tok))
                        #print(dtime.seconds)
                    if pourcentage >= 1.35:
                        print("monte de +"+ str(round((pourcentage -1)*100,4)) +"% en 3h sur", tok)
                        ll.append((current_time,tok))
                
            
    time.sleep(300)
    