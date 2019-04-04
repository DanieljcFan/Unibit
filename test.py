#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 00:15:32 2019
A simple work to show Unibit's API

@author: daniel
"""

import numpy as np
import pandas as pd

key = '-wZWj5vMAXJqKxlrjecJL_qUzevQIJpU'
cop_list = ['AMZN','BKNG','GOOGL','GOOG','ISRG','MELI','REGN','ORLY','NFLX','ULTA']

#real time price##################
def get_price(sticker='AAPL', size = '', datatype='csv',key=key):
    if size: size = 'size='+ str(size)
    url = 'https://api.unibit.ai/realtimestock/'+ sticker +'?'+ size +'&datatype='+ datatype +'&AccessKey='+ key
    df = pd.read_csv(url)
    df.insert(0,'Stock', sticker)
    return df

df = pd.DataFrame()
for cop in cop_list:
    temp = get_price(cop, size=1000)
    df = df.append(temp)

#history price######################
def get_histp(sticker='AAPL', ran='1m', interval = '1', datatype='csv',key = key):
    url = 'https://api.unibit.ai/historicalstockprice/'+ sticker +'?range='+ ran +'&interval='+ interval+'&datatype='+ datatype +'&AccessKey='+ key
    df = pd.read_csv(url)
    return df

df_close = pd.DataFrame()
for cop in cop_list:
    temp = get_histp(cop)
    if not df_close.shape[0]: 
        close = temp.iloc[:,[0,5]]
        close.columns.values[1] = cop
        df_close = close
    else: df_close[cop] = temp.iloc[:,5]
df_close = df_close.set_index('date')


logret = np.log(df_close / df_close.shift(1)) #log return of stocks
logret = logret[(logret.T != 0.0).any()]    # keep any row with any non-0.0 column value
logret = logret[logret.T.notnull().all()]       # keep any row with all non-NaN column values

print('mean of log returns:\n', logret.mean(),'\n')
print('standard diviation of log returns:\n',logret.std(), '\n')
print('skew of log returns:\n',logret.skew(),'\n')

logret.plot(figsize=(9,6)).legend(loc='upper left')

#ownership
def get_owner(sticker, owner = 'majority_holder', datatype = 'csv', key=key):
    url = 'https://api.unibit.ai/ownership/'+ sticker+'?ownership_type='+ owner + '&datatype='+datatype+'&AccessKey=' +key
    df = pd.read_csv(url)
    return df

df_holder = pd.DataFrame(columns = cop_list)
for cop in cop_list:
    temp = get_owner(cop,'top_institutional_holder')
    df_holder[cop] = temp.Holder.values

#find common holders:
def find_com(hlist1, hlist2):
    res = []
    for holder in hlist1:
        if holder in hlist2:
            res.append(holder)
    return res

com_holder = [[find_com(df_holder[cop1].values, df_holder[cop2].values) for cop2 in cop_list ] for cop1 in cop_list]

