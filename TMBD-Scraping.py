#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 20:07:13 2022

@author: Muscak

Dataset: https://www.themoviedb.org/movie/top-rated

Summary: 
In this project, I aimed to collect the information of the movies with the highest ratings from The Movie Database.
I will extract data from themoviedb.org site using Python's request library, 
make this data readable with the BeautifulSoup library, 
then store it in a DataFrame and save it in a .csv file with the help of the Pandas library.

"""

# Imoprt necessary libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Global parameters
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.77'}

df_movies = pd.DataFrame(columns=['ID', 'Title', 'Director','Release_Year', 'Original_Lang', 
                                  'Main_Genre', 'Genres', 'Runtime', 'User_Score', 'Ratings',
                                  'Budget', 'Revenue','URL'])

url = 'https://www.themoviedb.org/discover/movie/items'

max_pages = 21

# Function that sends requests to the website and fills the DataFrame accordingly
def fill_df():
    index = 0
    
    # The website lists the items in paged format.
    # This loop will get the first max_page pages.
    for page in range(1, max_pages):
        # The website accepts requests in post method.
        params = {'page':page, 'sort_by':'vote_average.desc', 'vote_count.gte':'300',
                  'vote_average.gte':'0', 'vote_average.lte':'10', 'with_runtime.lte':'400'}
 
        req = requests.post(url, data=params, headers=header)

        if req.status_code == 200: # Continue sending requests if the HTTP status code is 200
            prefix = 'https://www.themoviedb.org'
            bs = BeautifulSoup(req.content, 'lxml')
            movies = bs.find_all('div', attrs={'class':'wrapper'}, limit=20) # Get only 20 items with each request
            
            # This for loop is to collect the details of items in each page.
            for m in movies:
                id = m.a.get('href')
                title = m.a.get('title')
                full_url = prefix + id + '-' + title.replace(' ', '-').replace('\'', '-').lower()
                movie_req = requests.get(full_url, headers=header)
                bs_movie = BeautifulSoup(movie_req.content, 'lxml', from_encoding="utf-8")
                # Find the release year of the movie and remove paranthesis
                release_year = bs_movie.find('span', attrs={'class':'tag release_date'}).text.replace('(', '').replace(')', '')
                
                info = bs_movie.find('section', attrs={'class':'facts left_column'})
                p = info.find_all('p')
                if 'Original Title' in p[0].text: 
                    p_index = 1 # Don't get the original title value
                else:
                    p_index=0
                
                # Original audio language
                original_lang = p[p_index+1].text.replace('\n', '').split(' ')[2]
                # Production budget of the movie in USD
                budget = p[p_index+2].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]
                # Total revenue of the movie in USD
                revenue = p[p_index+3].text.replace('\n', '').split(' ')[1].replace('$','').replace(',','').split('.')[0]
                
                genres = bs_movie.find('span', attrs={'class':'genres'}).text.replace('\n', '').replace(' ', '').replace('\xa0', '')
                main_genre = genres.split(',')[0]
                rest_genre = genres.split(',')[1:]
                director = bs_movie.find('li', attrs={'class':'profile'}).a.text
                
                runtime_txt = bs_movie.find('span', attrs={'class':'runtime'}).text.replace('\n', '').replace(' ', '')
                # Add the runtime_txt value to the DataFrame if it can't be casted to integer
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
                try: # Add the user_score value to the DataFrame if it can't be casted to float
                    user_score = float(bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent'))
                except:
                    user_score = bs_movie.find('div', attrs={'class':'user_score_chart'}).get('data-percent')    
                # Send another request to get the number of ratings
                rating_url = prefix + id + '/remote/rating/details'
                rating_req = requests.get(rating_url, headers=header)
                bs_rating = BeautifulSoup(rating_req.content, 'lxml', from_encoding="utf-8")
                ratings = bs_rating.find('h3').text.split(' ')[0].replace(',', '')
               
                # Add all values to the DataFrame as a new row
                df_movies.loc[index] = (id.split('/')[2], title, director, release_year, 
                                        original_lang, main_genre, rest_genre, runtime, 
                                        user_score, ratings, budget, revenue, full_url)
                print(index,':' + full_url)
                index = index+1
        else:
            print(req.status_code)
            break


fill_df()

# Save the DataFrame as a .csv file.
df_movies.to_csv('tmdb_top_rated_movies.csv', encoding='utf-8')