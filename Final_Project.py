#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 21:28:13 2022

@author: Mustafa Cakir

Ders 11: Veri Analizi ve Görselleştirme Atölyesi

Dataset: https://www.themoviedb.org/movie/top-rated

Bitirme Projesi (Odev 6):
- Dilediğiniz bir web sitesinden request ve BeautifulSoup modüllerini kullanarak veri çekmek.
- Elde ettiğiniz verileri list veya dataframe yapısında saklamak. Gerekiyorsa ekstra hesaplamalar yapabilirsiniz.
- Sakladığınız verileri matplotlib, seaborn veya plotly kütüphanelerini kullanarak görselleştirmek.
- Ödevin .py dosyasının ilk kısmında yorum satırı olarak; projenizi özetleyen bir paragraf ekleyelim. 
Bu paragrafta projenizin amacını, hangi teknolojileri kullanacağınızı ve bu projeyle beraber hangi problemi 
çözdüğünüzü açıklayalım. İsteyenler ek bir sunum olarakta ekleyebilir.

Ozet:
Bu projede The Movie Database sitesinden en yuksek oy alan filmlerin bilgilerini toplamayi hedefledim. 
Amacim en yuksek oy alan filmleri tur, yonetmen, butce ve karlarini incelemek. Bu incelemeyi yaparken Python'un
request kutuphanisi kullanarak themoviedb.org sitesinden veri cekip, bu verileri BeautifulSoup kutuphanesi ile 
okunabilir hale getirip, sonra da Pandas kutuphanesi yardimi ile bir DataFrame'de saklayip, .csv dosyasina kaydedecegim.
Verisetini ise plotly express kutuphanesi kullanrak gorsellestirecegim.
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import plotly.express as px
# Asagidaki iki komut plotly grafiklerini Spyder IDE'sinde gosterebilmek icin
import plotly.io as io
io.renderers.default='browser'
import seaborn as sb
import matplotlib.pyplot as plt

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77'}

df_movies = pd.DataFrame(columns=['ID', 'Title', 'Director','Release_Year', 'Original_Lang', 
                                  'Main_Genre', 'Genres', 'Runtime', 'User_Score', 
                                  'Budget', 'Revenue','URL'])

url = 'https://www.themoviedb.org/discover/movie/items'

# Websitesine istekler gonderip, dataframe'i dolduran fonksiyon
def fill_df():
    index = 0
    
    # Websitesine veriler safyalar halinde saklandigi icin bir dongu ile ilk 10 sayfayi aliyoruz.
    for page in range(1,11):
        # Bu websitesi veri listesini donerken post methodu ile istek kabul etmektedir.
        params = {'page':page, 'sort_by':'vote_average.desc', 'vote_count.gte':'300',
                  'vote_average.gte':'0', 'vote_average.lte':'10', 'with_runtime.lte':'400'}
 
        req = requests.post(url, data=params, headers=header)

        if req.status_code == 200: # Sadece 200 kodu dondugu takdirde istkelere devam et
            prefix = 'https://www.themoviedb.org'
            bs = BeautifulSoup(req.content, 'lxml')
            movies = bs.find_all('div', attrs={'class':'wrapper'}, limit=20) # Her istekte en fazla 20 element getir.
            
            for m in movies:
                id = m.a.get('href')
                title = m.a.get('title')
                full_url = prefix + id + '-' + title.replace(' ', '-').replace('\'', '-').lower()
                movie_req = requests.get(full_url, headers=header)
                bs_movie = BeautifulSoup(movie_req.content, 'lxml', from_encoding="utf-8")
                release_year = bs_movie.find('span', attrs={'class':'tag release_date'}).text.replace('(', '').replace(')', '')
                
                info = bs_movie.find('section', attrs={'class':'facts left_column'})
                p = info.find_all('p')
                if 'Original Title' in p[0].text: 
                    p_index = 1 # Original title degeri varsa alma
                else:
                    p_index=0
                #status = p[p_index].text.replace('\n', '').split(' ')[1]
                original_lang = p[p_index+1].text.replace('\n', '').split(' ')[2]
                budget = p[p_index+2].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]
                revenue = p[p_index+3].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]
                
                genres = bs_movie.find('span', attrs={'class':'genres'}).text.replace('\n', '').replace(' ', '').replace('\xa0', '')
                main_genre = genres.split(',')[0]
                rest_genre = genres.split(',')[1:]
                director = bs_movie.find('li', attrs={'class':'profile'}).a.text
                
                runtime_txt = bs_movie.find('span', attrs={'class':'runtime'}).text.replace('\n', '').replace(' ', '')
                # runtime_txt integer'a donusmuyorsa oldugu gibi yaz
                try:
                    if len(runtime_txt.split('h')) == 1:
                        runtime = int(runtime_txt.replace('m', ''))
                    if len(runtime_txt.split('h')) == 2:
                        if runtime_txt.split('h')[1] != '':
                            runtime = int(runtime_txt.split('h')[0])*60 + int(runtime_txt.split('h')[1].replace('m', ''))
                    if len(runtime_txt.split('h')) == 2: 
                        if runtime_txt.split('h')[1] == '':
                            runtime = int(runtime_txt.split('h')[0])*60
                except:
                    runtime = runtime_txt
                try: # Oylar float'a donusmuyorsa oldugu gibi yaz
                    user_score = float(bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent'))
                except:
                    user_score = bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent')    
                
                # DataFrame'e yeni satir ekle
                df_movies.loc[index] = (id.split('/')[2], title, director, release_year, 
                                        original_lang, main_genre, rest_genre, runtime, 
                                        user_score, budget, revenue, full_url)
                print(index,':' + full_url)
                index = index+1
        else:
            print(req.status_code)
            break


fill_df()
df_movies.to_csv('top_rated_movies.csv', encoding='utf-8')

df_movies.info()

# Film turune gore en yuksek puan alan film sayilari
fig = px.histogram(df_movies, x='Main_Genre', barmode='group',
                   title='Ture gore film sayisi',
                   labels={'Main_Genre': 'Tur',
                           'value': 'Film Sayisi'})
fig.show()

# Orijinal dile gore en yuksek puan alan film sayilari
fig = px.histogram(df_movies, x='Original_Lang', barmode='group',
                   title='Dile gore film sayisi',
                   labels={'Original_Lang': 'Dil',
                           'value': 'Film Sayisi'})
fig.show()

df_movies['Revenue'].replace('-', np.nan, inplace=True)
df_movies['Budget'].replace('-', np.nan, inplace=True)
df_movies['Budget'].replace('-', np.nan, inplace=True)
df_movies['Revenue'] = df_movies['Revenue'].astype('Int64')
df_movies['Budget'] = df_movies['Budget'].astype('Int64')


df = df_movies.groupby(by='Release_Year').sum()[['Budget', 'Revenue']].reset_index()

fig = px.line(df, x='Release_Year', y='Budget',
                   title='Filmlerde kullanilan butcenin zamanla degisimi',
                   labels={'Release_Year': 'Yil',
                           'Budget': 'Butce'})
fig.show()

fig = px.line(df, x='Release_Year', y='Revenue',
                   title='Filmlerin karlarinin zamanla degisimi',
                   labels={'Release_Year': 'Yil',
                           'Budget': 'Kar'})
fig.show()
    