# ============================================================
# Step 2: Data Cleaning & Transformation
# ============================================================
# Loads raw movie data, cleans and transforms it into a
# structured format ready for analysis.
# ============================================================

import ast
import logging
import numpy as np
import pandas as pd

from config import (
    RAW_DATA_PATH,
    CLEAN_DATA_PATH,
    MIN_BUDGET_FOR_ROI
)

# Get logger for this module
logger = logging.getLogger(__name__)

# Columns to drop — no analytical value
COLUMNS_TO_DROP = [
    'adult', 'imdb_id', 'original_title',
    'video', 'homepage', 'backdrop_path',
    'origin_country'
]

# JSON-like columns containing nested data
JSON_COLUMNS = [
    'belongs_to_collection',
    'genres',
    'production_countries',
    'production_companies',
    'spoken_languages'
]

# Placeholder values to replace with NaN
PLACEHOLDERS = ['No Data', 'N/A', 'NA', 'none', 'None', '-', '']

# Final column order
FINAL_COLUMNS = [
    'id', 'title', 'tagline', 'release_date', 'genres',
    'belongs_to_collection', 'original_language', 'budget_musd',
    'revenue_musd', 'production_companies', 'production_countries',
    'vote_count', 'vote_average', 'popularity', 'runtime',
    'overview', 'spoken_languages', 'poster_path',
    'cast', 'cast_size', 'director', 'crew_size'
]


# ============================================================
# STEP 1 — DROP IRRELEVANT COLUMNS
# ============================================================

def drop_irrelevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drops columns that have no analytical value.

    Why: Reduces noise in the dataset and improves
    readability by removing fields like image URLs,
    external IDs and redundant title fields.

    Args:
        df (pd.DataFrame): Raw movie DataFrame.

    Returns:
        pd.DataFrame: DataFrame with irrelevant columns removed.
    """
    existing = [c for c in COLUMNS_TO_DROP if c in df.columns]
    df = df.drop(columns=existing, axis=1)
    logger.info(
        f"Dropped {len(existing)} irrelevant columns. "
        f"Shape: {df.shape}"
    )
    return df


# ============================================================
# STEP 2 — PARSE JSON-LIKE COLUMNS
# ============================================================

def safe_parse(value) -> list | dict | None:
    """
    Safely converts a string representation of a Python object
    back into a real Python list or dictionary.

    Why ast.literal_eval over eval(): ast.literal_eval only
    handles safe data types (lists, dicts, strings, numbers)
    and cannot execute arbitrary code — making it safe for
    processing untrusted data from CSV files.

    Args:
        value: String value to parse.

    Returns:
        list | dict: Parsed Python object if successful.
        None: If value is missing or cannot be parsed.
    """
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def parse_json_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts JSON-like string columns back into real
    Python objects (lists and dictionaries).

    Why: Saving a DataFrame to CSV converts nested fields
    like genres into plain strings. This step restores them
    to usable Python objects before extraction.

    Args:
        df (pd.DataFrame): DataFrame with string JSON columns.

    Returns:
        pd.DataFrame: DataFrame with parsed Python objects.
    """
    for col in JSON_COLUMNS:
        if col in df.columns:
            df[col] = df[col].apply(safe_parse)

    logger.info("JSON-like columns parsed successfully.")
    return df


# ============================================================
# STEP 3 — EXTRACT VALUES FROM JSON COLUMNS
# ============================================================

def extract_json_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts useful values from nested JSON columns using
    the pipe character as separator for multiple values.

    Why pipe separator: Commas are avoided because some
    company and country names contain commas themselves,
    which would cause parsing issues.

    Args:
        df (pd.DataFrame): DataFrame with parsed JSON columns.

    Returns:
        pd.DataFrame: DataFrame with flat string values.
    """
    # Extract collection name from dictionary
    # Why: We only need the name, not the ID or image paths
    df['belongs_to_collection'] = df['belongs_to_collection'].apply(
        lambda x: x['name'] if isinstance(x, dict) else None
    )

    # Extract genre names joined by pipe
    df['genres'] = df['genres'].apply(
        lambda x: '|'.join([g['name'] for g in x])
        if isinstance(x, list) else None
    )

    # Extract spoken language names joined by pipe
    # Why english_name: The 'name' field can be empty
    # for some languages (e.g. Xhosa returns empty string)
    df['spoken_languages'] = df['spoken_languages'].apply(
        lambda x: '|'.join([l['english_name'] for l in x])
        if isinstance(x, list) else None
    )

    # Extract production country names joined by pipe
    df['production_countries'] = df['production_countries'].apply(
        lambda x: '|'.join([c['name'] for c in x])
        if isinstance(x, list) else None
    )

    # Extract production company names joined by pipe
    df['production_companies'] = df['production_companies'].apply(
        lambda x: '|'.join([c['name'] for c in x])
        if isinstance(x, list) else None
    )

    logger.info("JSON values extracted successfully.")
    return df


# ============================================================
# STEP 4 — CONVERT DATA TYPES
# ============================================================

def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts columns to their correct data types.

    Why errors='coerce': Replaces invalid values with NaN
    instead of raising an error — making the pipeline robust
    against unexpected or missing values in the raw data.

    Args:
        df (pd.DataFrame): DataFrame with raw data types.

    Returns:
        pd.DataFrame: DataFrame with correct data types.
    """
    numeric_cols = [
        'budget', 'id', 'popularity', 'revenue',
        'runtime', 'vote_count', 'vote_average'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert release_date string to datetime
    # Why: Enables date arithmetic and time-based analysis
    if 'release_date' in df.columns:
        df['release_date'] = pd.to_datetime(
            df['release_date'], errors='coerce'
        )

    logger.info("Data types converted successfully.")
    logger.info(f"\n{df.dtypes}")
    return df


# ============================================================
# STEP 5 — HANDLE MISSING & UNREALISTIC VALUES
# ============================================================

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replaces unrealistic and placeholder values with NaN.

    Why replace zero budget/revenue: A value of $0 indicates
    missing data rather than an actual zero — keeping zeros
    would distort financial KPIs like ROI and profit.

    Args:
        df (pd.DataFrame): DataFrame with raw values.

    Returns:
        pd.DataFrame: DataFrame with cleaned values.
    """
    # Replace zero budget and revenue with NaN
    for col in ['budget', 'revenue']:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)

    # Replace zero runtime with NaN
    if 'runtime' in df.columns:
        df['runtime'] = df['runtime'].replace(0, np.nan)

    # Convert budget and revenue to Million USD
    # Why: Improves readability — $356,000,000 becomes $356.0M
    if 'budget' in df.columns:
        df['budget_musd'] = df['budget'] / 1_000_000
        df = df.drop(columns=['budget'])

    if 'revenue' in df.columns:
        df['revenue_musd'] = df['revenue'] / 1_000_000
        df = df.drop(columns=['revenue'])

    # Set vote_average to NaN where vote_count is 0
    # Why: A rating with zero votes is meaningless
    if 'vote_count' in df.columns and 'vote_average' in df.columns:
        df.loc[df['vote_count'] == 0, 'vote_average'] = np.nan

    # Replace known placeholder text with NaN
    for col in ['overview', 'tagline']:
        if col in df.columns:
            df[col] = df[col].replace(PLACEHOLDERS, np.nan)

    logger.info("Missing and unrealistic values handled.")
    return df


# ============================================================
# STEP 6 — REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate rows and rows with missing identifiers.

    Why check both id and title: Using both columns together
    ensures we only remove true duplicates — movies with the
    same ID AND title — not movies that share only one field.

    Args:
        df (pd.DataFrame): DataFrame to deduplicate.

    Returns:
        pd.DataFrame: Deduplicated DataFrame.
    """
    before = len(df)

    # Remove rows where id or title is missing
    df = df.dropna(subset=['id', 'title'])

    # Remove duplicate movies
    df = df.drop_duplicates(subset=['id', 'title'], keep='first')

    after = len(df)
    logger.info(
        f"Duplicates removed. "
        f"Rows before: {before}, after: {after}, "
        f"removed: {before - after}"
    )
    return df


# ============================================================
# STEP 7 — FILTER ROWS
# ============================================================

def filter_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters rows based on data completeness and status.

    Why minimum 10 non-NaN values: Rows with too many missing
    values are not useful for analysis. 10 non-NaN columns
    ensures enough data exists to draw meaningful insights.

    Why Released only: Unreleased movies have incomplete
    financial data and skew analysis results.

    Args:
        df (pd.DataFrame): DataFrame to filter.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    before = len(df)

    # Keep only rows with at least 10 non-NaN values
    df = df[df.notna().sum(axis=1) >= 10]

    # Keep only Released movies
    if 'status' in df.columns:
        df = df[df['status'] == 'Released']
        df = df.drop(columns=['status'])

    after = len(df)
    logger.info(
        f"Rows filtered. "
        f"Before: {before}, after: {after}"
    )
    return df


# ============================================================
# STEP 8 — ADD PLACEHOLDER COLUMNS
# ============================================================

def add_placeholder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds empty placeholder columns for cast and crew data.

    Why: Cast and crew data requires a separate API call to
    the TMDB credits endpoint (Step 3 of the pipeline).
    Placeholders are added here to maintain the correct
    final column structure.

    Args:
        df (pd.DataFrame): DataFrame without cast/crew columns.

    Returns:
        pd.DataFrame: DataFrame with placeholder columns added.
    """
    for col in ['cast', 'cast_size', 'director', 'crew_size']:
        df[col] = np.nan

    logger.info("Placeholder columns added for cast and crew.")
    return df


# ============================================================
# STEP 9 — REORDER AND RESET
# ============================================================

def reorder_and_reset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorders columns to the final required structure and
    resets the DataFrame index.

    Why reorder: A consistent column order improves
    readability and ensures downstream pipeline steps
    can reliably reference column positions.

    Why reset_index: After filtering rows the index has
    gaps (e.g. 0, 2, 5). Resetting gives a clean
    sequential index starting from 0.

    Args:
        df (pd.DataFrame): DataFrame to reorder.

    Returns:
        pd.DataFrame: Reordered DataFrame with reset index.
    """
    existing = [c for c in FINAL_COLUMNS if c in df.columns]
    df = df[existing]
    df = df.reset_index(drop=True)

    logger.info(f"Columns reordered. Final shape: {df.shape}")
    return df


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_clean_data():
    """
    Entry point for the data cleaning step.

    Loads raw data and applies all cleaning transformations
    in sequence. Called by main.py as Step 2 of the pipeline.

    Returns:
        pd.DataFrame: Fully cleaned and structured DataFrame.
    """
    logger.info("Starting data cleaning and transformation...")

    # Load raw data
    df = pd.read_csv(RAW_DATA_PATH)
    logger.info(f"Raw data loaded. Shape: {df.shape}")

    # Apply cleaning steps in sequence
    df = drop_irrelevant_columns(df)
    df = parse_json_columns(df)
    df = extract_json_values(df)
    df = convert_data_types(df)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = filter_rows(df)
    df = add_placeholder_columns(df)
    df = reorder_and_reset(df)

    # Save cleaned data
    df.to_csv(CLEAN_DATA_PATH, index=False)
    logger.info(f"Cleaned data saved to {CLEAN_DATA_PATH}")
    logger.info(f"Final shape: {df.shape}")
    logger.info(f"Missing values:\n{df.isnull().sum()}")

    return df


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    run_clean_data()