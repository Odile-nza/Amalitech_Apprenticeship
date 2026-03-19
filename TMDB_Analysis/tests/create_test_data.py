# Run this once to create test data file
# import pandas as pd
#
# df = pd.read_csv("data/final_clean_movie_data.csv")
# df.head(5).to_csv("tests/test_data.csv", index=False)
# print("Test data file created!")

import pandas as pd

df = pd.read_csv("E:/Amalitech/DataEngineering/TMDB_Analysis/data/final_clean_movie_data.csv")

df.head(5).to_csv("E:/Amalitech/DataEngineering/TMDB_Analysis/tests/test_data.csv", index=False)

print("Test data file created!")