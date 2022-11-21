# TMDB Scraping (WIP)

## Objective
In this project, I aimed to collect the information of the movies with the highest ratings from The Movie Database.
I will extract data from themoviedb.org site using Python's request library, make this data readable with the BeautifulSoup library, then store it in a DataFrame and save it in a .csv file with the help of the Pandas library.

## Website
The data is collected from [The Movie Database (TMDB)](https://www.themoviedb.org/) which is a community built movie and TV database. Since my focus was on the top rated movies, I scraped [Top Rated Movies](https://www.themoviedb.org/movie/top-rated) page.

## Dataset
Only first 20 pages are scraped. Each page has 20 moves. 
The below fields are stored:
- <ins>ID:</ins> Unique identifier of the movie in TMBD system.
- **Title:** English title of the movie. Original title is ignored.
- Director: The director of the movie. If the movie has more than one director, only the firts one listed is saved. 
- Release_Year: The year that movie is released to the theatres.
- Original_Lang: The language of the movie.
- Main_Genre: The first genre that is listed in the info.
- Genres: The all listed genres apart from the first one.
- Runtime: Runtime in minutes.
- User_Score: The TMDB score of the movie.
- Ratings: The number of ratings of the movie.
- Budget: The budget of the movie in USD.
- Revenue: The total revenue of the movie in USD.
- URL: TMDB link of the movie.

| **Column** | **Description**                                        |
|------------|--------------------------------------------------------|
| ID         | Unique identifier of the movie in TMBD system.         |
| Title      | English title of the movie. Original title is ignored. |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |
|            |                                                        |

