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

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

l = []

try:
    with open('listfile.txt', 'r') as filehandle:
        for line in filehandle:
            el = json.loads(line)
            delatime = datetime.now() - datetime.strptime(el["time"], '%Y-%m-%d %H:%M:%S.%f')
            print("delattime:", delatime)
            if delatime.seconds <= 24 * 60:
                l.append(line)
except Exception as E:
    print("error listfile: ", E)
cg = CoinGeckoAPI()

tokens = ['bitcoin', 'litecoin', 'ethereum']


while 1:
    prices = cg.get_price(ids=tokens, vs_currencies='usd')
    current_time = datetime.now()
    prices.update({"time":current_time})
    l.append(prices)
    if (len(l) >= 1500):
        l.pop(0)
    with open('listfile.txt', 'a+') as filehandle:
        filehandle.write(json.dumps(prices, default=str) + "\n")
    time.sleep(2)
