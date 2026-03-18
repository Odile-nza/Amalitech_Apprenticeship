    # STEP 3: KPI IMPLEMENTATION & ANALYSIS
###############################################################
# This file performs key performance indicator analysis on
# the cleaned movie dataset including ranking, filtering,
# franchise analysis and director performance


import pandas as pd
import numpy as np

#loading the final cleaned csv file
df = pd.read_csv("data/final_clean_movie_data.csv")

print("Final Cleaned data loaded:")
print(f"shape: {df.shape}")
print(df.head())

#Identifying the Best/Worst Performing Movies

print(df.info())
#Profit
df['profit_musd'] = df['revenue_musd'] -df['budget_musd']

#ROI(Return on Investment)
#calculating ROI for movies with budget >= 10M
df['roi'] = np.where(
    df['budget_musd'] >= 10,
    df['revenue_musd'] / df['budget_musd'],
    np.nan
)
print("\n KPI Columns calculated")
print(df[['title','budget_musd', 'revenue_musd', 'profit_musd', 'roi']].to_string())

# TASK 1: USER DEFINED FUNCTION (UDF) FOR RANKING
###############################################################
def rank_movies(df, column, ascending=False, min_filter=None, filter_col=None, top_n=None):

    """
    Ranks movies based on a given column.

    Parameters:
        df         : the DataFrame to rank
        column     : the column to rank by e.g. 'revenue_musd'
        ascending  : False = highest first, True = lowest first
        min_filter : minimum value filter e.g. 10 for budget >= 10M
        filter_col : column to apply the minimum filter on
        top_n      : number of top results to return (None = all)

    Returns:
        DataFrame: ranked movies with relevant columns
    """

    #Copying DataFrame
    result = df.copy()

    #only movies with budget >= 10M for ROI calculation
    if min_filter is not None and filter_col is not None:
        result = result[result[filter_col] >= min_filter]

    #Drop rows where the ranking column is NaN
    result = result.dropna(subset=[column])

    #Sort by the specified column
    result = result.sort_values(by=column, ascending=ascending)

    # Return top N results if specified
    if top_n is not None:
        result = result.head(top_n)

    # Return only the most relevant columns
    display_cols = ['title', 'director',column]

    # Add extra context columns if they exist in the DataFrame
    for col in ['budget_musd', 'revenue_musd', 'profit_musd',
                'roi', 'vote_average', 'vote_count', 'popularity']:
        if col in result.columns and col != column:
            display_cols.append(col)

    # Only return columns that exist
    display_cols = [c for c in display_cols if c in result.columns]

    result = result[display_cols].reset_index(drop=True)
    result.index = result.index +1
    result.index.name = 'Rank'

    return result


# TASK 2: IDENTIFY BEST/WORST PERFORMING MOVIES
###############################################################

print("\n\nIDENTIFYING BEST/WORST PERFORMING MOVIES:")
print("#" * 40)

# 1. HIGHEST REVENUE
print("\nTOP 5 MOVIES BY HIGHEST REVENUE (Million USD):")
print(rank_movies(df, column='revenue_musd', ascending=False, top_n=5).to_string())

# 2. HIGHEST BUDGET
print("\nTOP 5 MOVIES BY HIGHEST BUDGET (Million USD):")
print(rank_movies(df, column='budget_musd', ascending=False, top_n=5).to_string())

# 3. HIGHEST PROFIT
print("\nTOP 5 MOVIES BY HIGHEST PROFIT (Million USD):")
print(rank_movies(df, column='profit_musd', ascending=False, top_n=5).to_string())

# 4. LOWEST PROFIT
print("\nTOP 5 MOVIES WITH LOWEST PROFIT (Million USD):")
print(rank_movies(df, column='profit_musd', ascending=True, top_n=5).to_string())

# 5. HIGHEST ROI
print("\nTOP 5 MOVIES BY HIGHEST ROI (Budget >= $10M):")
print(rank_movies(df, column='roi', ascending=False,
                  min_filter=10, filter_col='budget_musd', top_n=5).to_string())

# 6. LOWEST ROI
print("\n TOP 5 MOVIES WITH LOWEST ROI (Budget >= $10M):")
print(rank_movies(df, column='roi', ascending=True,
                  min_filter=10, filter_col='budget_musd', top_n=5).to_string())

# 7. MOST VOTED
print("\nTOP 5 MOST VOTED MOVIES:")
print(rank_movies(df, column='vote_count', ascending=False, top_n=5).to_string())

# 8. HIGHEST RATED
print("\nTOP 5 HIGHEST RATED MOVIES (vote_count >= 10):")
print(rank_movies(df, column='vote_average', ascending=False,
                  min_filter=10, filter_col='vote_count', top_n=5).to_string())

# 9. LOWEST RATED
print("\n TOP 5 LOWEST RATED MOVIES (vote_count >= 10):")
print(rank_movies(df, column='vote_average', ascending=True,
                  min_filter=10, filter_col='vote_count', top_n=5).to_string())

# 10. MOST POPULAR
print("\n TOP 5 MOST POPULAR MOVIES:")
print(rank_movies(df, column='popularity', ascending=False, top_n=5).to_string())


# TASK 3 — ADVANCED MOVIE FILTERING & SEARCH QUERIES
###############################################################

print("\n\nADVANCED SEARCH QUERIES:")
print("#" * 40)

# SEARCH 1 — Best rated Science Fiction Action movies starring Bruce Willis
# We search the 'cast' column for Bruce Willis
# and the 'genres' column for both Science Fiction and Action
print("\n Search 1: Best-rated Sci-Fi Action movies starring Bruce Willis:")

search1 = df[
    df['cast'].str.contains('Bruce Willis', na=False) &      # cast contains Bruce Willis
    df['genres'].str.contains('Science Fiction', na=False) & # genre includes Sci-Fi
    df['genres'].str.contains('Action', na=False)            # genre includes Action
].sort_values('vote_average', ascending=False)               # sorted by rating highest first

if len(search1) == 0:
    print("No movies found matching this criteria in our dataset")
else:
    print(search1[['title', 'genres', 'cast', 'vote_average', 'director']].to_string())

# SEARCH 2 — Movies starring Uma Thurman directed by Quentin Tarantino
# sorted by runtime shortest to longest
print("\n Search 2: Movies starring Uma Thurman directed by Quentin Tarantino:")

search2 = df[
    df['cast'].str.contains('Uma Thurman', na=False) &       # cast contains Uma Thurman
    df['director'].str.contains('Quentin Tarantino', na=False) # directed by Tarantino
].sort_values('runtime', ascending=True)                     # sorted by runtime shortest first

if len(search2) == 0:
    print("No movies found matching this criteria in our dataset")
else:
    print(search2[['title', 'cast', 'director', 'runtime', 'vote_average']].to_string())





# TASK 4 — FRANCHISE VS STANDALONE MOVIE PERFORMANCE
###############################################################

print("\n\nFRANCHISE VS STANDALONE MOVIE PERFORMANCE:")
print("#" * 40)

# Create a new column to identify franchise vs standalone
# If belongs_to_collection is not NaN → franchise
# If belongs_to_collection is NaN → standalone
df['is_franchise'] = df['belongs_to_collection'].notna()

# Map True/False to readable labels
# True  → "Franchise"
# False → "Standalone"
df['movie_type'] = df['is_franchise'].map({True: 'Franchise', False: 'Standalone'})

# Group by movie type and calculate KPIs
franchise_comparison = df.groupby('movie_type').agg(
    movie_count    = ('title',        'count'),   # total number of movies
    mean_revenue   = ('revenue_musd', 'mean'),    # average revenue
    median_roi     = ('roi',          'median'),  # median ROI
    mean_budget    = ('budget_musd',  'mean'),    # average budget
    mean_popularity= ('popularity',   'mean'),    # average popularity
    mean_rating    = ('vote_average', 'mean'),    # average rating
).round(2)

print(franchise_comparison.to_string())


# TASK 5 — MOST SUCCESSFUL MOVIE FRANCHISES
###############################################################

print("\n\nMOST SUCCESSFUL MOVIE FRANCHISES:")
print("#" * 40)

# Filter only franchise movies — standalone movies have no collection
franchise_df = df[df['belongs_to_collection'].notna()]

# Group by collection name and calculate franchise KPIs
franchise_stats = franchise_df.groupby('belongs_to_collection').agg(
    total_movies   = ('title',        'count'),   # number of movies in franchise
    total_budget   = ('budget_musd',  'sum'),     # total budget spent
    mean_budget    = ('budget_musd',  'mean'),    # average budget per movie
    total_revenue  = ('revenue_musd', 'sum'),     # total revenue earned
    mean_revenue   = ('revenue_musd', 'mean'),    # average revenue per movie
    mean_rating    = ('vote_average', 'mean'),    # average rating
).round(2)

# Sort by total revenue — highest earning franchise first
franchise_stats = franchise_stats.sort_values('total_revenue', ascending=False)

print(franchise_stats.to_string())


# TASK 6 — MOST SUCCESSFUL DIRECTORS
###############################################################

print("\n\nMOST SUCCESSFUL DIRECTORS:")
print("=" * 60)

# Group by director and calculate director KPIs
director_stats = df.groupby('director').agg(
    total_movies   = ('title',        'count'),   # total movies directed
    total_revenue  = ('revenue_musd', 'sum'),     # total revenue across all movies
    mean_rating    = ('vote_average', 'mean'),    # average rating across all movies
).round(2)

# Sort by total revenue — most successful director first
director_stats = director_stats.sort_values('total_revenue', ascending=False)

print(director_stats.to_string())


# SAVE RESULTS
###############################################################

# Save the DataFrame with KPI columns added
df.to_csv("data/analysis_movies.csv", index=False)
print("\nAnalysis results saved to data/analysis_movies.csv")

