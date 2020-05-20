# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:12:53 2020

@author: Szafran
"""


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

data = pd.read_csv('albums.csv', sep=';', names=['Album', 'Artist', 'Year'])
data['Album'] = [i.replace("&", "and") for i in data['Album']]
data['Artist'] = [i.replace("&", "and") for i in data['Artist']]
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

links_to_albums = []

# SCRAP GOOGLE SEARCH
for record in data.iloc:
    google_search = f"https://google.com/search?q={record['Artist']} {record['Album']} album genius"
    request = requests.get(google_search, headers=headers).content
    soup = BeautifulSoup(request, 'html.parser')
    for link in soup.find_all('a'):
        if 'genius.com/albums' in str(link.get('href')):
            links_to_albums.append(str(link.get('href')))
            break

data['links'] = links_to_albums


data.to_csv('dataset_with_links.csv')