# ============================================================
# Step 1: Data Extraction
# ============================================================
# Fetches raw movie data from the TMDB API for a predefined
# list of movie IDs and saves the result as a CSV file.
# ============================================================

import time
import logging
import requests
import pandas as pd

from config import (
    API_KEY,
    BASE_URL,
    MOVIE_IDS,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    MAX_RETRIES,
    RAW_DATA_PATH
)

# Get logger for this module
logger = logging.getLogger(__name__)


# ============================================================
# FETCH SINGLE MOVIE WITH RETRY LOGIC
# ============================================================

def fetch_movie(movie_id: int) -> dict | None:
    """
    Fetches data for a single movie from the TMDB API.

    Implements retry logic with exponential backoff to handle
    transient network errors and API rate limiting gracefully.

    Args:
        movie_id (int): The unique TMDB ID of the movie.

    Returns:
        dict: Movie data as a Python dictionary if successful.
        None: If all retries fail or movie is not found.
    """
    url = f"{BASE_URL}/{movie_id}?api_key={API_KEY}"

    # Retry loop — attempts MAX_RETRIES times before giving up
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Send GET request with timeout to avoid hanging
            # timeout=REQUEST_TIMEOUT raises error if no response
            # received within the specified seconds
            response = requests.get(url, timeout=REQUEST_TIMEOUT)

            # 200 = success — return the movie data
            if response.status_code == 200:
                return response.json()

            # 404 = movie not found — no point retrying
            elif response.status_code == 404:
                logger.warning(
                    f"Movie ID {movie_id} not found (404). Skipping."
                )
                return None

            # 429 = rate limited — wait longer before retrying
            elif response.status_code == 429:
                wait_time = 2 ** attempt  # exponential backoff: 2, 4, 8 seconds
                logger.warning(
                    f"Rate limited on movie {movie_id}. "
                    f"Waiting {wait_time}s before retry {attempt}/{MAX_RETRIES}."
                )
                time.sleep(wait_time)

            # Other errors — log and retry
            else:
                logger.warning(
                    f"Unexpected status {response.status_code} "
                    f"for movie {movie_id}. "
                    f"Attempt {attempt}/{MAX_RETRIES}."
                )

        except requests.exceptions.Timeout:
            # Request took too long — log and retry
            logger.warning(
                f"Timeout fetching movie {movie_id}. "
                f"Attempt {attempt}/{MAX_RETRIES}."
            )

        except requests.exceptions.ConnectionError:
            # No internet connection — log and retry
            logger.warning(
                f"Connection error for movie {movie_id}. "
                f"Attempt {attempt}/{MAX_RETRIES}."
            )

        except requests.exceptions.RequestException as e:
            # Any other request error — log and retry
            logger.error(
                f"Request error for movie {movie_id}: {e}. "
                f"Attempt {attempt}/{MAX_RETRIES}."
            )

        # Wait before next retry using exponential backoff
        # Why exponential backoff: each retry waits longer
        # giving the API time to recover — 2, 4, 8 seconds
        if attempt < MAX_RETRIES:
            time.sleep(2 ** attempt)

    # All retries exhausted
    logger.error(
        f"Failed to fetch movie {movie_id} "
        f"after {MAX_RETRIES} attempts. Skipping."
    )
    return None


# ============================================================
# FETCH ALL MOVIES
# ============================================================

def fetch_all_movies(movie_ids: list) -> list:
    """
    Fetches data for all movies in the provided list of IDs.

    Iterates through each movie ID, calls fetch_movie() and
    collects successful results. Adds a delay between requests
    to respect the TMDB API rate limit.

    Args:
        movie_ids (list): List of TMDB movie IDs to fetch.

    Returns:
        list: List of movie data dictionaries.
    """
    movies = []

    for idx, movie_id in enumerate(movie_ids, start=1):
        logger.info(
            f"Fetching movie {idx}/{len(movie_ids)} — ID: {movie_id}"
        )

        data = fetch_movie(movie_id)

        if data:
            movies.append(data)

        # Pause between requests to avoid hitting rate limit
        # Why: sending too many requests too fast gets us blocked
        time.sleep(REQUEST_DELAY)

    logger.info(
        f"Successfully fetched {len(movies)}/{len(movie_ids)} movies."
    )
    return movies


# ============================================================
# SAVE TO CSV
# ============================================================

def save_raw_data(movies: list) -> pd.DataFrame:
    """
    Converts the list of movie dictionaries to a DataFrame
    and saves it as a CSV file for the next pipeline step.

    Args:
        movies (list): List of movie data dictionaries.

    Returns:
        pd.DataFrame: The raw movie DataFrame.
    """
    # Convert list of dicts to DataFrame
    df = pd.DataFrame.from_records(movies)

    # Save raw data — before any cleaning or transformation
    # Why save raw data: allows reprocessing without re-fetching
    df.to_csv(RAW_DATA_PATH, index=False)

    logger.info(f"Raw data saved to {RAW_DATA_PATH}")
    logger.info(f"Shape: {df.shape}")

    return df


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_fetch_data():
    """
    Entry point for the data extraction step.

    Orchestrates fetching all movies and saving raw data.
    Called by main.py as Step 1 of the pipeline.
    """
    logger.info("Starting data extraction from TMDB API...")

    # Fetch all movies
    movies = fetch_all_movies(MOVIE_IDS)

    if not movies:
        raise ValueError(
            "No movies fetched. "
            "Check API key and internet connection."
        )

    # Save to CSV
    df = save_raw_data(movies)

    logger.info(
        f"Data extraction complete. "
        f"{len(movies)} movies saved."
    )
    return df


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    run_fetch_data()