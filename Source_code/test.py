from bs4 import BeautifulSoup
import pandas as pd
import urllib
from urllib.request import urlopen
from tqdm import tqdm
from tqdm import tqdm_notebook

date = pd.date_range('2019-06-14',periods=8, freq='7d') #d는 day, 1/15까지 넣을거
print(date[0])
print(type(date[0]))
print(type(date))
date

music_date = []
music_title = []
music_artist = []
music_album = []
music_ranking = []


for today in tqdm_notebook(date):
    url = "https://music.bugs.co.kr/chart/track/week/total?chartdate={date}" #date 값 넣어주기 위해 {}
    html = url.format(date= urllib.parse.quote(today.strftime('%Y%m%d')))
    response = urlopen(html)
    
    soup = BeautifulSoup(response, 'html.parser')
    end = 50 #영화 갯수 체크
    
    music_date.extend([today for n in range(end)])
    music_title.extend([soup.find_all('p','title')[n].a.string for n in range(end)])
    music_artist.extend([soup.find_all('p','artist')[n].a.string for n in range(end)])
    music_album.extend([soup.find_all('a','album')[n+1].string for n in range(end)])
    music_ranking.extend([soup.find_all('div','ranking')[n].strong.string for n in range(end)])

import numpy as np


music = pd.DataFrame({'date': music_date,'ranking': music_ranking, 'title': music_title, 'artist': music_artist,  'album': music_album})

music['ranking'] = pd.to_numeric(music['ranking'])

music_unique = pd.pivot_table(music, index=['title'], aggfunc = np.mean) #평균은 np.mean
music_unique = music_unique.sort_values(by='ranking', ascending = True)
music_unique