#STEP 1: FETCH MOVIE DATA FROM TMDB API
#This file establishes a connection with the TMDB API, retrieves movie data
# for a list of movie IDs, and stores the unprocessed data in a CSV file.
#############################################################################

from dotenv import load_dotenv
import os

#IMPORTS
import requests
import pandas as pd
import time

load_dotenv()

#Api configuration
API_KEY = os.getenv("TMDB_API_KEY")

#verifying API
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")

BASE_URL = "https://api.themoviedb.org/3/movie"

#Movie IDS
movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397,
             420818, 24428, 168259, 99861, 284054, 12445,
             181808, 330457, 351286, 109445, 321612, 260513]

#Fetch function
def fetch_movie(movie_id):
    try:
        url = f"{BASE_URL}/{movie_id}?api_key={API_KEY}"
        response = requests.get(url) #contains the movie data sent back by TMDB

        #Checking if the request was successful
        if response.status_code == 200:
            return response.json()#Converting the response from rwa JSON format to a python dictionary
        else:
            #if status code is not 200 printing a warning message
            print(f"Movie ID {movie_id} not found - status {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching movie {movie_id}: {e}")
        return None

#Fetching all movies
movies = []  #empty list to collect a movie data

#Loop through every movie ID in our list one by one
for movie_id in movie_ids:
    print(f"Fetching movie {movie_id}")
    data = fetch_movie(movie_id)
    if data:
        movies.append(data)
        time.sleep(0.5) #pause for 0.5 seconds between each request

#Creating Dataframe
df = pd.DataFrame.from_records(movies) #converting list of movie dictionaries into pandas DataFrame
print(f"\n Successfully fetched {len(movies)} movies")
print(f"Shape of DataFrame: {df.shape}")
print(f"\nColumns:\n{df.columns.tolist()}")
print(f"\nFirst 3 rows:")
print(df.head(3))

#Saving raw data
df.to_csv("data/raw_movie_data.csv", index=False)
print(f"\n Successfully saved {len(movies)} movies")