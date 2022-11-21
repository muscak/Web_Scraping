# Dataset

Only first 20 pages are scraped. Each page has 20 movies. There are 400 data points in the dataset.

The below fields (13 columns) are stored:

| **Column**    | **Description**                                                                                         |
|---------------|---------------------------------------------------------------------------------------------------------|
| ID            | Unique identifier of the movie in TMBD system.                                                          |
| Title         | English title of the movie. Original title is ignored.                                                  |
| Director      | The director of the movie. If the movie has more than one director, only the firts one listed is saved. |
| Release_Year  | The year that movie is released to the theatres.                                                        |
| Original_Lang | The language of the movie.                                                                              |
| Main_Genre    | The first genre that is listed in the info.                                                             |
| Genres        | The all listed genres apart from the first one.                                                         |
| Runtime       | Runtime in minutes.                                                                                     |
| User_Score    | The TMDB score of the movie.                                                                            |
| Ratings       | The number of ratings of the movie.                                                                     |
| Budget        | The budget of the movie in USD.                                                                         |
| Revenue       | The total revenue of the movie in USD.                                                                  |
| URL           | TMDB link of the movie.                                                                                 |
