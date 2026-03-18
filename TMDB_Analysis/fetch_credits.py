# FETCH CAST & CREW DATA FROM TMDB CREDITS ENDPOINT
###############################################################
# This file fetches cast and crew data for each movie
# and updates the cleaned_movies.csv with the missing columns:
# cast, cast_size, director, crew_size

from dotenv import load_dotenv
import os

import requests
import pandas as pd
import time

# API CONFIGURATION
###############################################################

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

#verifying API
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")

# Credits endpoint
BASE_URL = "https://api.themoviedb.org/3/movie"

# LOAD CLEANED DATA
###############################################################

# Load the cleaned movies file
df = pd.read_csv("data/clean_movie_data.csv")

df['cast']      = df['cast'].astype(object)
df['cast_size'] = df['cast_size'].astype(object)
df['director']  = df['director'].astype(object)
df['crew_size'] = df['crew_size'].astype(object)

print(f"Loaded cleaned movies: {df.shape}")
print(f"Movies to fetch credits for: {len(df)}")


# FETCH CREDITS FUNCTION
###############################################################

def fetch_credits(movie_id):
    """
    Fetches cast and crew data for a single movie.

    Parameters:
        movie_id (int): The unique TMDB ID of the movie

    Returns:
        dict: Credits data containing cast and crew lists
        None: If the request failed
    """
    try:

        url = f"{BASE_URL}/{movie_id}/credits?api_key={API_KEY}"

        # Send GET request to TMDB
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Credits not found for movie ID {movie_id} — status {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching credits for movie {movie_id}: {e}")
        return None


# EXTRACT CAST & CREW INFORMATION
###############################################################

def extract_credits(credits_data):
    """
    Extracts useful cast and crew information from raw credits data.

    Parameters:
        credits_data (dict): Raw credits response from TMDB API

    Returns:
        dict: Extracted cast names, cast size, director name, crew size
    """

    cast_list = credits_data.get('cast', [])

    # Get names of top 10 cast members separated by "|"
    cast_names = '|'.join(
        [member['name'] for member in cast_list[:10]]
    )

    # Total number of cast members in the full list
    cast_size = len(cast_list)

    # Extract crew list
    crew_list = credits_data.get('crew', [])

    # Find the director — look for crew member with job = "Director"
    # next() returns the first match, None if no director found
    director = next(
        (member['name'] for member in crew_list if member['job'] == 'Director'),
        None
    )

    # Total number of crew members
    crew_size = len(crew_list)

    return {
        'cast':      cast_names,
        'cast_size': cast_size,
        'director':  director,
        'crew_size': crew_size
    }


# FETCH CREDITS FOR ALL MOVIES
###############################################################

print("\nFetching credits for all movies...")
print("=" * 60)

# Loop through each movie in our DataFrame
for idx, row in df.iterrows():

    movie_id = row['id']
    title    = row['title']

    print(f"Fetching credits for: {title} (ID: {movie_id})")

    # Fetch credits from TMDB
    credits_data = fetch_credits(movie_id)

    if credits_data:
        # Extract useful information from credits
        credits = extract_credits(credits_data)

        # Update the DataFrame with the extracted values
        df.at[idx, 'cast']      = credits['cast']
        df.at[idx, 'cast_size'] = credits['cast_size']
        df.at[idx, 'director']  = credits['director']
        df.at[idx, 'crew_size'] = credits['crew_size']

    # Pause between requests to avoid rate limiting
    time.sleep(0.3)


# PREVIEW & SAVE
###############################################################

print("\n Credits fetched for all movies!")
print(f"\nMissing values after fetching credits:")
print(df[['title', 'cast', 'cast_size', 'director', 'crew_size']].isnull().sum())

print(f"\nSample cast & crew data:")
print(df[['title', 'cast', 'director', 'cast_size', 'crew_size']].to_string())

# Save updated DataFrame — overwrite the cleaned file
df.to_csv("data/final_clean_movie_data.csv", index=False)

print("\n Updated clean_movie_data.csv with cast and crew data!")