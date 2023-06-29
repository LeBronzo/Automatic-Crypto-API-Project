#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Connects to CoinMarketCap and pulls the data in JSON format

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
 'start':'1',
 'limit':'5000',
 'convert':'USD'
}
headers = {
 'Accepts': 'application/json',
 'X-CMC_PRO_API_KEY': 'df492302-31ee-4c0c-8ad2-195bb98c2af3',
}

session = Session()
session.headers.update(headers)

try:
 response = session.get(url, params=parameters)
 data = json.loads(response.text)
 print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
 print(e)


# In[3]:


type(data)


# In[5]:


# Normalizes the data in JSON format into a dataframe 

import pandas as pd
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)


# In[8]:


df = pd.json_normalize(data['data'])
df['timestamp'] = pd.to_datetime('now')
df


# In[9]:


# Function that compiles the above code into an API function that also writes the dataframe into a csv file inside a directory

def api_runner ():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'5000',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'df492302-31ee-4c0c-8ad2-195bb98c2af3',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now')
    df
    
    if not os.path.isfile(r'C:\Users\LEAN\Documents\CryptoAPIProj\API.csv'):
        df.to_csv(r'C:\Users\LEAN\Documents\CryptoAPIProj\API.csv', header='column_names')
    else:
        df.to_csv(r'C:\Users\LEAN\Documents\CryptoAPIProj\API.csv', mode='a', header=False)


# In[12]:


# Automates the API data pull so that it runs every 1 minute

import os
from time import time
from time import sleep

for i in range (333):
    api_runner()
    print('API Runner completed successfully')
    sleep(60) #sleep for 1 minute
exit()


# In[2]:


df


# In[20]:


df22 = pd.read_csv(r'C:\Users\LEAN\Documents\CryptoAPIProj\API.csv')
df22


# In[15]:


# Doing some data cleaning/transforming

pd.set_option('display.float_format', lambda x: '%.5f' % x)


# In[16]:


df


# In[18]:


df3 = df.groupby('name', sort=False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()


# In[19]:


df3


# In[20]:


df3.stack()


# In[21]:


type(df3)


# In[22]:


type(df3.stack())


# In[24]:


df4 = df3.stack()
df5 = df4.to_frame(name='values')
df5


# In[29]:


index = pd.Index(range(29844))
df6 = df5.reset_index()
df6


# In[32]:


df7 = df6.rename(columns={'level_1': 'percent_change'})
df7


# In[57]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d'], ['1h', '24h', '7d', '30d', '60d', '90d'])
df8 = df7.head(100)
df8


# In[80]:


# Data Visualizations that show the Percent Change in Value per Crypto over time and the Count of number of Cryptocurrencies added to CoinMarketCap through the years

import seaborn as sns
import matplotlib.pyplot as plt

sns.catplot(x='percent_change', y='values', hue='name', data=df8, kind='point', height=7, aspect=2).set(title='Percent Change in Value per Crypto')


# In[78]:


df['date_added2'] = df['date_added'].str[:10]
df['year_added'] = df['date_added'].str[:4]

sns.catplot(x='year_added', kind='count', data=df, height = 7, aspect = 2, order = ['2010', '2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023',]).set(title='Count of # of Cryptocurrencies Added to CoinMarketCap per Year')


# In[ ]:




