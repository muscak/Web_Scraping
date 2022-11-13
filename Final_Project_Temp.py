#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 21:28:13 2022

@author: Mustafa Cakir
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77'}

df_movies = pd.DataFrame(columns=['ID', 'Title', 'Director','Release_Year', 'Original_Lang', 
                                  'Main_Genre', 'Genres', 'Runtime', 'User_Score', 
                                  'Budget', 'Revenue','URL'])

url = 'https://www.themoviedb.org/discover/movie/items'

fill_df()
df_movies.to_csv('top_rated_movies.csv')

def fill_df():
    index = 0
    for page in range(1,2):
        params = {'page':page, 'sort_by':'vote_average.desc', 'vote_count.gte':'300',
                  'vote_average.gte':'0', 'vote_average.lte':'10', 'with_runtime.lte':'400'}
 
        req = requests.post(url, data=params, headers=header)

        if req.status_code == 200:
            prefix = 'https://www.themoviedb.org'
            bs = BeautifulSoup(req.content, 'lxml')
            movies = bs.find_all('div', attrs={'class':'wrapper'}, limit=20)
            
            for m in movies:
                id = m.a.get('href')
                title = m.a.get('title')
                full_url = prefix + id + '-' + title.replace(' ', '-').replace('\'', '-').lower()
                movie_req = requests.get(full_url, headers=header)
                bs_movie = BeautifulSoup(movie_req.content, 'lxml')
                release_year = bs_movie.find('span', attrs={'class':'tag release_date'}).text.replace('(', '').replace(')', '')
                
                info = bs_movie.find('section', attrs={'class':'facts left_column'})
                p = info.find_all('p')
                if 'Original Title' in p[0].text:
                    p_index = 1
                else:
                    p_index=0
                status = p[p_index].text.replace('\n', '').split(' ')[1]
                original_lang = p[p_index+1].text.replace('\n', '').split(' ')[2]
                budget = p[p_index+2].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]
                revenue = p[p_index+3].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]
                
                genres = bs_movie.find('span', attrs={'class':'genres'}).text.replace('\n', '').replace(' ', '').replace('\xa0', '')
                main_genre = genres.split(',')[0]
                rest_genre = genres.split(',')[1:]
                director = bs_movie.find('li', attrs={'class':'profile'}).a.text
                
                runtime_txt = bs_movie.find('span', attrs={'class':'runtime'}).text.replace('\n', '').replace(' ', '')
                try:
                    runtime = int(runtime_txt.split('h')[0])*60 + int(runtime_txt.split('h')[1].replace('m', ''))
                except:
                    runtime = runtime_txt
                try:
                    user_score = float(bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent'))
                except:
                    user_score = bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent')    
                    
                df_movies.loc[index] = (id.split('/')[2], title, director, release_year, 
                                        original_lang, main_genre, rest_genre, runtime, 
                                        user_score, budget, revenue, full_url)
                print(index,':' + full_url)
                index = index+1
        else:
            print(req.status_code)
        
        

    


movie_req = requests.get(df_movies.iloc[8,11], headers=header)
bs_movie = BeautifulSoup(movie_req.content, 'lxml')
release_year = bs_movie.find('span', attrs={'class':'tag release_date'}).text.replace('(', '').replace(')', '')

genres = bs_movie.find('span', attrs={'class':'genres'}).text.replace('\n', '').replace(' ', '').replace('\xa0', '')
main_genre = genres.split(',')[0]
rest_genre = genres.split(',')[1:]
runtime_txt = bs_movie.find('span', attrs={'class':'runtime'}).text.replace('\n', '').replace(' ', '')
try:
    runtime = int(runtime_txt.split('h')[0])*60 + int(runtime_txt.split('h')[1].replace('m', ''))
except:
    runtime = runtime_txt
try:
    user_score = float(bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent'))
except:
    user_score = bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent')
director = bs_movie.find('li', attrs={'class':'profile'}).a.text



info = bs_movie.find('section', attrs={'class':'facts left_column'})
p = info.find_all('p')

if 'Original Title' in p[0].text:
    p_index = 1
else:
    p_index=0
status = p[p_index].text.replace('\n', '').split(' ')[1]
original_lang = p[p_index+1].text.replace('\n', '').split(' ')[2]
budget = p[p_index+2].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]
revenue = p[p_index+3].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]



#votes = bs_movie.find('div', attrs={'class':'rating_details'})

##--------------------

movies

a = 1
for m in movies:
    url = m.a.get('href')
    title = m.a.get('title')
    full_url = prefix + url + '-' + title.replace(' ', '-').lower()
    print(a,':' + full_url)
    a = a+1


params = {'page':'1', 'sort_by':'vote_average.desc', 'vote_count.gte':'300',
          'vote_average.gte':'0', 'vote_average.lte':'10', 'with_runtime.lte':'400'}
url = 'https://www.themoviedb.org/discover/movie/items'

req2 = requests.post(url, data=params)
bs2 = BeautifulSoup(req2.content, 'lxml')

movies = bs2.find_all('div', attrs={'class':'wrapper'}, limit=20)

a = 1
for m in movies:
    url = m.a.get('href')
    title = m.a.get('title')
    full_url = prefix + url + '-' + title.replace(' ', '-').lower()
    print(a,':' + full_url)
    a = a+1

    