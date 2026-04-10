import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================
# API CONFIGURATION
# ============================================================

# TMDB API key loaded securely from .env file
API_KEY  = os.getenv("TMDB_API_KEY")

# Base URL for TMDB movie endpoint
BASE_URL = "https://api.themoviedb.org/3/movie"

# Request timeout in seconds
# Prevents pipeline from hanging indefinitely on slow responses
REQUEST_TIMEOUT = 10

# Maximum number of retries on failed requests
MAX_RETRIES = 3

# Delay between requests in seconds
# Prevents hitting TMDB API rate limit
REQUEST_DELAY = 0.3

# ============================================================
# MOVIE IDs
# ============================================================

# List of movie IDs to fetch from TMDB API
MOVIE_IDS = [
    0, 299534, 19995, 140607, 299536, 597,
    135397, 420818, 24428, 168259, 99861,
    284054, 12445, 181808, 330457, 351286,
    109445, 321612, 260513
]

# ============================================================
# FILE PATHS
# ============================================================

# Raw data saved directly from API
RAW_DATA_PATH = "data/raw/raw_movies.csv"

# Cleaned data after transformation
CLEAN_DATA_PATH = "data/processed/clean_movies.csv"

# Final data with cast and crew
FINAL_DATA_PATH = "data/processed/final_movies.csv"

# Analysis data with KPI columns
ANALYSIS_DATA_PATH = "data/processed/analysis_movies.csv"

# Output folder for visualizations
OUTPUT_PATH = "outputs/"

# ============================================================
# ANALYSIS CONFIGURATION
# ============================================================

# Minimum budget in Million USD for ROI calculation
# Avoids misleading ROI from very low budget movies
MIN_BUDGET_FOR_ROI = 10

# Minimum vote count for rating analysis
MIN_VOTES_FOR_RATING = 10

# Number of top results to show in rankings
TOP_N_RESULTS = 5

# ============================================================
# VALIDATE API KEY
# ============================================================

if not API_KEY:
    raise ValueError(
        "TMDB_API_KEY not found! "
        "Please add it to your .env file: "
        "TMDB_API_KEY=your_api_key_here"
    )