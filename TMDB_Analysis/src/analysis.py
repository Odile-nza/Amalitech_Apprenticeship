# ============================================================
# Step 3: KPI Analysis
# ============================================================
# Calculates key performance indicators and performs
# advanced analysis on the enriched movie dataset.
# ============================================================

import logging
import numpy as np
import pandas as pd

from config import (
    FINAL_DATA_PATH,
    ANALYSIS_DATA_PATH,
    MIN_BUDGET_FOR_ROI,
    MIN_VOTES_FOR_RATING,
    TOP_N_RESULTS
)

# Get logger for this module
logger = logging.getLogger(__name__)


# ============================================================
# STEP 1 — CALCULATE KPI COLUMNS
# ============================================================

def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds derived KPI columns to the DataFrame.

    Why profit and ROI are calculated here and not during
    cleaning: These are analytical metrics derived from
    cleaned financial data — separating concerns keeps
    clean_data.py focused on cleaning only.

    Args:
        df (pd.DataFrame): Enriched movie DataFrame.

    Returns:
        pd.DataFrame: DataFrame with KPI columns added.
    """
    # Profit = Revenue - Budget (both in Million USD)
    df['profit_musd'] = df['revenue_musd'] - df['budget_musd']

    # ROI = Revenue / Budget
    # Why only for budget >= MIN_BUDGET_FOR_ROI:
    # Very low budget movies can show unrealistically high ROI
    # (e.g. a $1M budget earning $50M = 50x ROI)
    # which skews the analysis and misleads stakeholders
    df['roi'] = np.where(
        df['budget_musd'] >= MIN_BUDGET_FOR_ROI,
        df['revenue_musd'] / df['budget_musd'],
        np.nan
    )

    logger.info("KPI columns calculated: profit_musd, roi")
    return df


# ============================================================
# STEP 2 — USER DEFINED FUNCTION FOR RANKING
# ============================================================

def rank_movies(
    df: pd.DataFrame,
    column: str,
    ascending: bool = False,
    min_filter: float = None,
    filter_col: str = None,
    top_n: int = None
) -> pd.DataFrame:
    """
    Ranks movies based on a specified column with optional
    filtering and result limiting.

    Why a reusable UDF: The same ranking logic is needed
    for 10 different KPIs. A single function eliminates
    code duplication (DRY principle) and ensures consistent
    ranking behavior across all metrics.

    Args:
        df (pd.DataFrame): Movie DataFrame to rank.
        column (str): Column to rank by.
        ascending (bool): False = highest first (default).
        min_filter (float): Minimum value for filter_col.
        filter_col (str): Column to apply minimum filter on.
        top_n (int): Number of top results to return.

    Returns:
        pd.DataFrame: Ranked movies with relevant columns.
    """
    result = df.copy()

    # Apply minimum filter if specified
    # Why: Some KPIs require a minimum threshold
    # e.g. ROI only for budget >= 10M
    if min_filter is not None and filter_col is not None:
        result = result[result[filter_col] >= min_filter]

    # Drop rows where ranking column is NaN
    result = result.dropna(subset=[column])

    # Sort by the specified column
    result = result.sort_values(by=column, ascending=ascending)

    # Add rank column starting from 1
    result.insert(0, 'rank', range(1, len(result) + 1))

    # Return top N results if specified
    if top_n is not None:
        result = result.head(top_n)

    # Select display columns
    display_cols = ['rank', 'title', 'director', column]

    # Add context columns
    for col in [
        'budget_musd', 'revenue_musd', 'profit_musd',
        'roi', 'vote_average', 'vote_count', 'popularity'
    ]:
        if col in result.columns and col != column:
            display_cols.append(col)

    display_cols = [c for c in display_cols if c in result.columns]

    return result[display_cols].reset_index(drop=True)


# ============================================================
# STEP 3 — BEST/WORST PERFORMING MOVIES
# ============================================================

def analyze_movie_performance(df: pd.DataFrame) -> dict:
    """
    Ranks movies across 10 different KPI metrics to identify
    best and worst performing movies.

    Args:
        df (pd.DataFrame): Movie DataFrame with KPI columns.

    Returns:
        dict: Dictionary of ranking DataFrames keyed by metric.
    """
    rankings = {}

    metrics = [
        ('highest_revenue',  'revenue_musd',  False, None,                None,         TOP_N_RESULTS),
        ('highest_budget',   'budget_musd',   False, None,                None,         TOP_N_RESULTS),
        ('highest_profit',   'profit_musd',   False, None,                None,         TOP_N_RESULTS),
        ('lowest_profit',    'profit_musd',   True,  None,                None,         TOP_N_RESULTS),
        ('highest_roi',      'roi',           False, MIN_BUDGET_FOR_ROI,  'budget_musd',TOP_N_RESULTS),
        ('lowest_roi',       'roi',           True,  MIN_BUDGET_FOR_ROI,  'budget_musd',TOP_N_RESULTS),
        ('most_voted',       'vote_count',    False, None,                None,         TOP_N_RESULTS),
        ('highest_rated',    'vote_average',  False, MIN_VOTES_FOR_RATING,'vote_count', TOP_N_RESULTS),
        ('lowest_rated',     'vote_average',  True,  MIN_VOTES_FOR_RATING,'vote_count', TOP_N_RESULTS),
        ('most_popular',     'popularity',    False, None,                None,         TOP_N_RESULTS),
    ]

    for name, col, asc, min_f, f_col, n in metrics:
        rankings[name] = rank_movies(
            df, column=col, ascending=asc,
            min_filter=min_f, filter_col=f_col, top_n=n
        )
        logger.info(f"Ranking computed: {name}")
        logger.info(f"\n{rankings[name].to_string()}\n")

    return rankings


# ============================================================
# STEP 4 — FRANCHISE VS STANDALONE ANALYSIS
# ============================================================

def analyze_franchise_vs_standalone(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compares franchise and standalone movie performance
    across key financial and popularity metrics.

    Why median ROI instead of mean: ROI can have extreme
    outliers that skew the mean. Median is more robust
    and better represents the typical performance.

    Args:
        df (pd.DataFrame): Movie DataFrame with KPI columns.

    Returns:
        pd.DataFrame: Comparison statistics by movie type.
    """
    # Classify movies as franchise or standalone
    # Why notna(): belongs_to_collection is None for standalone
    df['movie_type'] = df['belongs_to_collection'].apply(
        lambda x: 'Franchise' if pd.notna(x) else 'Standalone'
    )

    comparison = df.groupby('movie_type').agg(
        movie_count     = ('title',        'count'),
        mean_revenue    = ('revenue_musd', 'mean'),
        median_roi      = ('roi',          'median'),
        mean_budget     = ('budget_musd',  'mean'),
        mean_popularity = ('popularity',   'mean'),
        mean_rating     = ('vote_average', 'mean')
    ).round(2)

    logger.info("Franchise vs Standalone analysis complete.")
    logger.info(f"\n{comparison.to_string()}\n")

    return comparison


# ============================================================
# STEP 5 — FRANCHISE ANALYSIS
# ============================================================

def analyze_franchises(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies the most successful movie franchises based
    on financial performance and audience ratings.

    Args:
        df (pd.DataFrame): Movie DataFrame with KPI columns.

    Returns:
        pd.DataFrame: Franchise statistics sorted by revenue.
    """
    # Filter franchise movies only
    franchise_df = df[df['belongs_to_collection'].notna()]

    franchise_stats = franchise_df.groupby(
        'belongs_to_collection'
    ).agg(
        total_movies  = ('title',        'count'),
        total_budget  = ('budget_musd',  'sum'),
        mean_budget   = ('budget_musd',  'mean'),
        total_revenue = ('revenue_musd', 'sum'),
        mean_revenue  = ('revenue_musd', 'mean'),
        mean_rating   = ('vote_average', 'mean')
    ).round(2).sort_values('total_revenue', ascending=False)

    logger.info("Franchise analysis complete.")
    logger.info(f"\n{franchise_stats.to_string()}\n")

    return franchise_stats


# ============================================================
# STEP 6 — DIRECTOR ANALYSIS
# ============================================================

def analyze_directors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifies the most successful directors based on
    total revenue, movie count and average rating.

    Args:
        df (pd.DataFrame): Movie DataFrame with KPI columns.

    Returns:
        pd.DataFrame: Director statistics sorted by revenue.
    """
    director_stats = df.groupby('director').agg(
        total_movies  = ('title',        'count'),
        total_revenue = ('revenue_musd', 'sum'),
        mean_rating   = ('vote_average', 'mean')
    ).round(2).sort_values('total_revenue', ascending=False)

    logger.info("Director analysis complete.")
    logger.info(f"\n{director_stats.to_string()}\n")

    return director_stats


# ============================================================
# STEP 7 — SEARCH QUERIES
# ============================================================

def search_movies(
    df: pd.DataFrame,
    cast_member: str = None,
    director_name: str = None,
    genre: str = None,
    sort_by: str = 'vote_average',
    ascending: bool = False
) -> pd.DataFrame:
    """
    Filters movies based on cast member, director and genre
    criteria with flexible sorting options.

    Why str.contains with na=False: Safely handles NaN values
    in string columns without raising errors.

    Args:
        df (pd.DataFrame): Movie DataFrame to search.
        cast_member (str): Name of cast member to search for.
        director_name (str): Name of director to search for.
        genre (str): Genre to filter by.
        sort_by (str): Column to sort results by.
        ascending (bool): Sort order.

    Returns:
        pd.DataFrame: Filtered and sorted search results.
    """
    result = df.copy()

    if cast_member:
        result = result[
            result['cast'].str.contains(cast_member, na=False)
        ]

    if director_name:
        result = result[
            result['director'].str.contains(director_name, na=False)
        ]

    if genre:
        result = result[
            result['genres'].str.contains(genre, na=False)
        ]

    result = result.sort_values(sort_by, ascending=ascending)

    logger.info(
        f"Search results: {len(result)} movies found "
        f"(cast={cast_member}, director={director_name}, "
        f"genre={genre})"
    )

    return result[
        ['title', 'genres', 'cast', 'director',
         'vote_average', 'runtime']
    ].reset_index(drop=True)


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_analysis():
    """
    Entry point for the KPI analysis step.

    Loads enriched data, calculates KPIs and performs all
    analytical queries. Called by main.py as Step 4 of
    the pipeline.

    Returns:
        pd.DataFrame: DataFrame with KPI columns added.
    """
    logger.info("Starting KPI analysis...")

    # Load enriched data from previous step
    df = pd.read_csv(FINAL_DATA_PATH)
    logger.info(f"Enriched data loaded. Shape: {df.shape}")

    # Calculate KPI columns
    df = calculate_kpis(df)

    # Run all analyses
    analyze_movie_performance(df)
    analyze_franchise_vs_standalone(df)
    analyze_franchises(df)
    analyze_directors(df)

    # Run search queries
    logger.info("Search 1: Sci-Fi Action movies with Bruce Willis")
    search_movies(
        df,
        cast_member='Bruce Willis',
        genre='Action'
    )

    logger.info("Search 2: Uma Thurman + Quentin Tarantino movies")
    search_movies(
        df,
        cast_member='Uma Thurman',
        director_name='Quentin Tarantino',
        sort_by='runtime',
        ascending=True
    )

    # Save analysis data
    df.to_csv(ANALYSIS_DATA_PATH, index=False)
    logger.info(f"Analysis data saved to {ANALYSIS_DATA_PATH}")

    return df


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    run_analysis()