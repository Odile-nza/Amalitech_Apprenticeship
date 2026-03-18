#STEP 2: DATA CLEANING AND PREPROCESSING

#This file loads, cleans, and
# organizes the unstructured movie data
# so that it may be analyzed.
#############################################################

import pandas as pd
import numpy as np
import ast

#loading the raw csv file
df = pd.read_csv('data/raw_movie_data.csv')
print("Raw Movie Data:")
print(f"Shape: {df.shape}")
print(df.head(10))

#TASK 1: DROP IRRELEVANT COLUMNS
#############################################################

#There is no analytical value in these columns for our project.
columns_to_drop = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
df.drop(columns_to_drop, axis=1, inplace=True)

# Confirm the columns were dropped
print("\n Irrelevant columns dropped!")
print(f"New Shape: {df.shape}")
print(f"\nRemaining Columns:\n{df.columns.tolist()}")

#TASK 2:EVALUATE JSON-LIKE COLUMNS
###############################################################

#Evaluate JSON-like columns
#The columns that contain nested JSON-like data
json_columns = [
    'belongs_to_collection',
    'genres',
    'production_countries',
    'production_companies',
    'spoken_languages'
]

def safe_parse(value):
    try:
        # ast.literal_eval safely evaluates a string as a Python expression
        # It is safer than eval() because it only handles data types
        # not executable code
        return ast.literal_eval(value)

    except (ValueError, SyntaxError):
        # If the value cannot be parsed return None
        return None

# ## Convert all JSON-like columns from strings to Python objects
# for col in JSON_columns:
#     df[col] = df[col].apply(safe_parse)


print("\nBEFORE CONVERSION — Raw string values:")
print("=" * 60)

for col in json_columns:
    print(f"\n Column: '{col}'")
    print(f"   Data type : {df[col].dtype}")        # shows 'object' = string
    print(f"   Non-null  : {df[col].notna().sum()}")
    print(f"   Null      : {df[col].isna().sum()}")
    print(f"   Sample    : {df[col].iloc[0]}")      # raw string value

# converting
for col in json_columns:
    df[col] = df[col].apply(safe_parse)

print("\n\nAFTER CONVERSION — Real Python objects:")
print("=" * 60)

for col in json_columns:
    print(f"\n Column: '{col}'")
    print(f"   Data type        : {df[col].dtype}")
    print(f"   Python type      : {type(df[col].iloc[0])}")  # list or dict
    print(f"   Non-null         : {df[col].notna().sum()}")
    print(f"   Null             : {df[col].isna().sum()}")
    print(f"   Sample           : {df[col].iloc[0]}")        # real Python object



# TASK 3 — EXTRACT AND CLEAN KEY DATA POINTS
#############################################################

# BELONGS TO COLLECTION
df['belongs_to_collection'] = df['belongs_to_collection'].apply(
    lambda x: x['name'] if isinstance(x, dict) else None
)

# GENRES

df['genres'] = df['genres'].apply(
    lambda x: '|'.join([g['name'] for g in x]) if isinstance(x, list) else None
)

# SPOKEN LANGUAGES

df['spoken_languages'] = df['spoken_languages'].apply(
    lambda x: '|'.join([l['english_name'] for l in x]) if isinstance(x, list) else None
)

# PRODUCTION COUNTRIES

df['production_countries'] = df['production_countries'].apply(
    lambda x: '|'.join([c['name'] for c in x]) if isinstance(x, list) else None
)

# PRODUCTION COMPANIES

df['production_companies'] = df['production_companies'].apply(
    lambda x: '|'.join([c['name'] for c in x]) if isinstance(x, list) else None
)

print("\n Values extracted from JSON-like columns!")

# Preview extracted columns
print("\nEXTRACTED COLUMNS PREVIEW:")
print("#" * 60)
print(df[json_columns].to_string())


# TASK 4: INSPECT WITH value_counts() TO FIND ANOMALIES
################################################################

print("\nINSPECTING JSON COLUMNS WITH value_counts():")
print("#" * 60)

for col in json_columns:
    print(f"\n {col}:")
    print(df[col].value_counts(dropna=False))


# TASK 5: CONVERT COLUMN DATA TYPES
###############################################################

df['budget']      = pd.to_numeric(df['budget'],      errors='coerce')
df['id']          = pd.to_numeric(df['id'],          errors='coerce')
df['popularity']  = pd.to_numeric(df['popularity'],  errors='coerce')
df['revenue']     = pd.to_numeric(df['revenue'],     errors='coerce')
df['runtime']     = pd.to_numeric(df['runtime'],     errors='coerce')
df['vote_count']  = pd.to_numeric(df['vote_count'],  errors='coerce')
df['vote_average']= pd.to_numeric(df['vote_average'],errors='coerce')

# Convert release_date string to proper datetime object
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

print("\n Data types converted!")
print(df.dtypes)


# TASK 6: REPLACE UNREALISTIC VALUES
###############################################################

# Replace 0 with NaN — 0 budget/revenue/runtime is unrealistic
df['budget']  = df['budget'].replace(0, np.nan)
df['revenue'] = df['revenue'].replace(0, np.nan)
df['runtime'] = df['runtime'].replace(0, np.nan)

# Convert budget and revenue to A Million USD
df['budget_musd']  = df['budget']  / 1_000_000
df['revenue_musd'] = df['revenue'] / 1_000_000

# Drop original budget and revenue — replaced by million USD versions
df.drop(columns=['budget', 'revenue'], inplace=True)

print("\n Budget and Revenue converted to Million USD!")
print(df[['title', 'budget_musd', 'revenue_musd']].to_string())

# Check movies with vote_count = 0
zero_votes = df[df['vote_count'] == 0]
print(f"\n Movies with vote_count = 0: {len(zero_votes)}")

# Set vote_average to NaN where vote_count is 0
df.loc[df['vote_count'] == 0, 'vote_average'] = np.nan

# Replace placeholder text in overview and tagline with NaN
placeholders = ['No Data', 'N/A', 'NA', 'none', 'None', '-', '']
df['overview'] = df['overview'].replace(placeholders, np.nan)
df['tagline']  = df['tagline'].replace(placeholders, np.nan)

print("\ Unrealistic values replaced!")
#print(df['tagline'])


# TASK 7: REMOVE DUPLICATES & DROP UNKNOWN ID/TITLE
###############################################################
print(f"\nBefore:")
print(f"Shape: {df.shape}")

df.drop_duplicates(subset=['id', 'title'], keep='first', inplace=True)
df.dropna(subset=['id', 'title'], inplace=True)

print(f"\n Duplicates removed!")
print(f"\nAfter:")
print(f"Shape: {df.shape}")


# TASK 8: KEEP ROWS WITH AT LEAST 10 NON-NaN VALUES
###############################################################

# Count non-NaN values per row
non_nan_counts = df.notna().sum(axis=1)

# Keep only rows with 10 or more non-NaN values
df = df[non_nan_counts >= 10]

print(f"\n Rows with fewer than 10 non-NaN values removed!")
print(f"Shape after filtering: {df.shape}")


# TASK 9: FILTER TO 'RELEASED' MOVIES ONLY
###############################################################

df = df[df['status'] == 'Released']
df.drop(columns=['status'], inplace=True)

print(f"\n Filtered to Released movies only!")
print(f"Shape after filtering: {df.shape}")

# TASK 10: ADD PLACEHOLDER COLUMNS FOR CAST & CREW
###############################################################

df['cast']      = np.nan
df['cast_size'] = np.nan
df['director']  = np.nan
df['crew_size'] = np.nan


# TASK 10 — REORDER COLUMNS
###############################################################

final_columns = [
    'id', 'title', 'tagline', 'release_date', 'genres',
    'belongs_to_collection', 'original_language', 'budget_musd',
    'revenue_musd', 'production_companies', 'production_countries',
    'vote_count', 'vote_average', 'popularity', 'runtime',
    'overview', 'spoken_languages', 'poster_path',
    'cast', 'cast_size', 'director', 'crew_size'
]

# ============================================================
# DEBUG — CHECK COLUMN MISMATCHES BEFORE REORDERING
# ============================================================

print("Columns in df but NOT in final_columns:")
print([col for col in df.columns if col not in final_columns])

print("\nColumns in final_columns but NOT in df:")
print([col for col in final_columns if col not in df.columns])

print(f"\ndf columns      : {df.columns.tolist()}")
print(f"final_columns   : {final_columns}")


# Only keep columns that exist in our DataFrame
existing_columns = [col for col in final_columns if col in df.columns]
df = df[existing_columns]

print(f"\nColumns reordered!")

# TASK 11 — RESET INDEX
###############################################################
df.reset_index(drop=True, inplace=True)

print(f"\nIndex reset!")


# FINAL PREVIEW & SAVE
###############################################################

print("\nFINAL CLEANED DATAFRAME:")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nFirst 3 rows:\n{df.head(3).to_string()}")

df.to_csv("data/clean_movie_data.csv", index=False)
print("\n Cleaned data saved to data/clean_movies.csv")

