#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 23:59:02 2021

@author: arthur
"""

import pycoingecko
from pycoingecko import CoinGeckoAPI
import time
import json
from datetime import date,  datetime


l = []

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
        if dtime.seconds > 3500 and dtime.seconds < 4700: #1h
            print(el)
            for tok in tokens:
                if prices[tok]["usd"]/el[tok]["usd"] <= 0.7:
                    print("chute de +30% en 1h sur ", tok)
                if prices[tok]["usd"]/el[tok]["usd"] >= 1.3:
                    print("monte de 30% en 1h sur", tok)
                    
                
            
    time.sleep(2)
