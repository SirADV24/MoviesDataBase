"""
    This script uses the data from https://www.kaggle.com/neha1703/movie-genre-from-its-poster?select=MovieGenre.csv
    You need the file MovieGenre.csv
    This script will download the posters (.jpg) of the movies in MovieGenre.csv and keep
        only the movies with valid posters

    We will only keep the first 100 movies that have a score higher than the margin

"""
import csv
import os
import requests
import shutil
from PIL import Image

DATA_BASE_FOLDER = "MoviesDataBase"
POSTER_FOLDER = "MoviesPosters"
MOVIES_INFO_CSV = "Movies.csv"
RAW_DATA_MOVIES = "MovieGenre.csv"

POSTER_FOLDER_PATH = os.path.join(DATA_BASE_FOLDER, POSTER_FOLDER)
MOVIES_INFO_CSV_PATH = os.path.join(DATA_BASE_FOLDER, MOVIES_INFO_CSV)
RAW_DATA_MOVIES_PATH = os.path.join(DATA_BASE_FOLDER, RAW_DATA_MOVIES)
MOVIE_RATING_MARGIN = 8.5
NUMBER_OF_MOVIES = 100

if os.path.isdir(POSTER_FOLDER_PATH):
    pass
else:
    os.mkdir(POSTER_FOLDER_PATH)

if os.path.isfile(MOVIES_INFO_CSV):
    pass
else:
    with open(MOVIES_INFO_CSV_PATH, 'wb') as file:
        pass


def get_data():
    with open(RAW_DATA_MOVIES_PATH, encoding="ISO-8859-1") as raw_file:
        lines = csv.reader(raw_file, delimiter=',')
        errors = 0
        poster_downloaded = 0
        with open(MOVIES_INFO_CSV_PATH, "w") as final:
            for line in lines:
                movie_name = line[2]
                movie_score = line[3]
                movie_genre = line[4]
                movie_url_poster = line[5]

                try:
                    score = float(movie_score)
                    if score < MOVIE_RATING_MARGIN:
                        continue
                except ValueError:
                    continue

                # download movie poster
                try:
                    response = requests.get(movie_url_poster, stream=True)
                    poster_name = movie_name + ".png"
                    movie_poster_path = os.path.join(POSTER_FOLDER_PATH, poster_name)
                    response.raw.decode_content = True

                    with open(movie_poster_path, "wb") as poster:
                        shutil.copyfileobj(response.raw, poster)
                    # find if the jpg is corrupted ( must be a cleaner way tbh )
                    try:
                        im = Image.open(movie_poster_path)
                        im.verify()
                        im.close()
                        poster_downloaded += 1
                    except Exception as ex:
                        os.remove(movie_poster_path)
                        raise Exception()

                    final.write(movie_name + "," + movie_score + "," + movie_genre + ","
                                + movie_poster_path + "\n")

                except Exception as _:
                    errors += 1
                if poster_downloaded >= NUMBER_OF_MOVIES:
                    break


if __name__ == "__main__":
    print("Loading data base\n")
    get_data()
    print("Data loaded")
