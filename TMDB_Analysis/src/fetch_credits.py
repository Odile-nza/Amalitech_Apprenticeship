# ============================================================
#  Credits Enrichment
# ============================================================
# Fetches cast and crew data from the TMDB credits endpoint
# and enriches the cleaned movie dataset with this information.
# ============================================================

import time
import logging
import requests
import pandas as pd

from config import (
    API_KEY,
    BASE_URL,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    MAX_RETRIES,
    CLEAN_DATA_PATH,
    FINAL_DATA_PATH
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Number of top cast members to extract
# Why 10: The full cast list can have 50+ members including
# extras. Top 10 captures the most relevant cast members
# while keeping the data manageable for analysis.
TOP_CAST_COUNT = 10


# ============================================================
# FETCH CREDITS FOR A SINGLE MOVIE
# ============================================================

def fetch_credits(movie_id: int) -> dict | None:
    """
    Fetches cast and crew data for a single movie from the
    TMDB credits endpoint with retry logic.

    Why separate endpoint: Cast and crew data lives at
    /movie/{id}/credits — a different endpoint from movie
    details at /movie/{id}. This requires a separate API call
    for each movie.

    Args:
        movie_id (int): The unique TMDB ID of the movie.

    Returns:
        dict: Credits data containing cast and crew lists.
        None: If all retries fail or credits not found.
    """
    # Credits endpoint differs from movie details endpoint
    url = f"{BASE_URL}/{movie_id}/credits?api_key={API_KEY}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 404:
                logger.warning(
                    f"Credits not found for movie {movie_id} (404). "
                    f"Skipping."
                )
                return None

            elif response.status_code == 429:
                wait_time = 2 ** attempt
                logger.warning(
                    f"Rate limited for movie {movie_id}. "
                    f"Waiting {wait_time}s before retry "
                    f"{attempt}/{MAX_RETRIES}."
                )
                time.sleep(wait_time)

            else:
                logger.warning(
                    f"Unexpected status {response.status_code} "
                    f"for movie {movie_id}. "
                    f"Attempt {attempt}/{MAX_RETRIES}."
                )

        except requests.exceptions.Timeout:
            logger.warning(
                f"Timeout fetching credits for movie {movie_id}. "
                f"Attempt {attempt}/{MAX_RETRIES}."
            )

        except requests.exceptions.ConnectionError:
            logger.warning(
                f"Connection error for movie {movie_id}. "
                f"Attempt {attempt}/{MAX_RETRIES}."
            )

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Request error for movie {movie_id}: {e}. "
                f"Attempt {attempt}/{MAX_RETRIES}."
            )

        if attempt < MAX_RETRIES:
            time.sleep(2 ** attempt)

    logger.error(
        f"Failed to fetch credits for movie {movie_id} "
        f"after {MAX_RETRIES} attempts."
    )
    return None


# ============================================================
# EXTRACT CAST AND CREW FROM CREDITS
# ============================================================

def extract_credits(credits_data: dict) -> dict:
    """
    Extracts useful cast and crew information from raw
    credits API response.

    Why top 10 cast only: The full cast list includes
    extras and minor roles. Top 10 captures the most
    relevant cast members ordered by prominence.

    Why store price_at_purchase pattern for director:
    Using next() with a default of None safely returns
    the first director without crashing if none exists.

    Args:
        credits_data (dict): Raw credits response from TMDB.

    Returns:
        dict: Extracted cast names, sizes and director info.
    """
    # Extract cast list
    cast_list = credits_data.get('cast', [])

    # Get top N cast member names separated by pipe
    cast_names = '|'.join(
        [member['name'] for member in cast_list[:TOP_CAST_COUNT]]
    )

    # Total number of cast members in the full list
    cast_size = len(cast_list)

    # Extract crew list
    crew_list = credits_data.get('crew', [])

    # Find director — first crew member with job = "Director"
    # Why next() with None default: safely returns None
    # if no director exists instead of raising StopIteration
    director = next(
        (member['name'] for member in crew_list
         if member['job'] == 'Director'),
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


# ============================================================
# ENRICH DATAFRAME WITH CREDITS
# ============================================================

def enrich_with_credits(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fetches and adds cast and crew data to the DataFrame.

    Why convert placeholder columns to object type first:
    Placeholder columns were initialized with np.nan which
    pandas stores as float64. String values cannot be inserted
    into float64 columns — converting to object type first
    allows both strings and NaN values.

    Args:
        df (pd.DataFrame): Cleaned movie DataFrame with
                           placeholder cast/crew columns.

    Returns:
        pd.DataFrame: DataFrame enriched with credits data.
    """
    # Convert placeholder columns from float64 to object
    # Why: Allows inserting string values into NaN columns
    for col in ['cast', 'cast_size', 'director', 'crew_size']:
        df[col] = df[col].astype(object)

    total = len(df)

    for idx, row in df.iterrows():
        movie_id = row['id']
        title    = row['title']

        logger.info(
            f"Fetching credits {idx + 1}/{total} — {title}"
        )

        credits_data = fetch_credits(int(movie_id))

        if credits_data:
            credits = extract_credits(credits_data)

            # Update individual cells with extracted values
            df.at[idx, 'cast']      = credits['cast']
            df.at[idx, 'cast_size'] = credits['cast_size']
            df.at[idx, 'director']  = credits['director']
            df.at[idx, 'crew_size'] = credits['crew_size']

        # Pause between requests to respect API rate limit
        time.sleep(REQUEST_DELAY)

    logger.info("Credits enrichment complete.")
    return df


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_fetch_credits():
    """
    Entry point for the credits enrichment step.

    Loads cleaned data, fetches credits for all movies
    and saves the enriched dataset. Called by main.py
    as Step 3 of the pipeline.

    Returns:
        pd.DataFrame: DataFrame enriched with credits data.
    """
    logger.info("Starting credits enrichment...")

    # Load cleaned data from previous step
    df = pd.read_csv(CLEAN_DATA_PATH)
    logger.info(f"Cleaned data loaded. Shape: {df.shape}")

    # Enrich with credits
    df = enrich_with_credits(df)

    # Verify no missing credits
    missing = df[['cast', 'director', 'cast_size', 'crew_size']].isnull().sum()
    logger.info(f"Missing values after enrichment:\n{missing}")

    # Save enriched dataset
    df.to_csv(FINAL_DATA_PATH, index=False)
    logger.info(f"Enriched data saved to {FINAL_DATA_PATH}")

    return df


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    run_fetch_credits()