# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:40:15 2020

@author: Szafran
"""

"""
theres an exception in layout of a genius page - fix it"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

data = pd.read_csv('dataset_with_links.csv')

lyrics_dict = {}

for record in data.iloc:
    request = requests.get(record['links'], headers=headers).content
    soup = BeautifulSoup(request, 'html.parser')
    for song_link in soup.find_all('a'):
        if ('-lyrics' in str(song_link.get('href'))):
            while True:
                try:
                    request_song = requests.get(str(song_link.get('href')), headers=headers).content
                except requests.exceptions.SSLError:
                    time.sleep(10)
                    continue
                soup_song = BeautifulSoup(request_song, 'html.parser')
                if 'Burrr' in str(soup_song):
                    lyrics_dict[song_link.get('href')] = 'Error. Lyrics not found.'
                    break
                elif "More on Genius" in str(soup_song):
                    song_name = soup_song.find_all('h2')[-1].get_text()[:-7]
                    lyrics = BeautifulSoup(str(soup_song)[str(soup_song).index('<div class="lyrics">'): str(soup_song).index('More on Genius')], 'html.parser').get_text()
                    lyrics_dict[record['Album'] + "|" + song_name] = lyrics
                    break
            
import json

json = json.dumps(lyrics_dict)
f = open("lyrics_dict.json","w")
f.write(json)
f.close()

