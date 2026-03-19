# TEST CASES FOR TMDB MOVIE ANALYSIS
# ============================================================

import pandas as pd
import numpy as np
import pytest

# Load small test data file
df = pd.read_csv("E:/Amalitech/DataEngineering/TMDB_Analysis/tests/test_data.csv")


# TEST 1 — DATA LOADED CORRECTLY
# ============================================================

def test_data_is_not_empty():
    """Check that our dataset is not empty"""
    assert len(df) > 0
    print(" Data is not empty!")

def test_data_has_correct_columns():
    """Check that important columns exist"""
    important_columns = ['id', 'title', 'budget_musd', 'revenue_musd', 'vote_average']
    for col in important_columns:
        assert col in df.columns, f"Column '{col}' is missing!"
    print(" All important columns exist!")

# ============================================================
# TEST 2 — DATA QUALITY CHECKS
# ============================================================

def test_title_is_never_missing():
    """Every movie must have a title"""
    assert df['title'].isnull().sum() == 0
    print(" No missing titles!")

def test_id_is_never_missing():
    """Every movie must have an ID"""
    assert df['id'].isnull().sum() == 0
    print(" No missing IDs!")

def test_no_duplicate_movies():
    """No movie should appear twice"""
    assert df.duplicated(subset=['id', 'title']).sum() == 0
    print(" No duplicate movies!")

# TEST 3 — FINANCIAL DATA CHECKS
# ============================================================

def test_budget_is_positive():
    """Budget should always be positive"""
    assert (df['budget_musd'] > 0).all()
    print(" All budgets are positive!")

def test_revenue_is_positive():
    """Revenue should always be positive"""
    assert (df['revenue_musd'] > 0).all()
    print(" All revenues are positive!")

def test_revenue_greater_than_budget():
    """All movies in our dataset made profit"""
    assert (df['revenue_musd'] > df['budget_musd']).all()
    print(" All movies made profit!")

# TEST 4 — KPI CALCULATIONS
# ============================================================

def test_profit_calculation():
    """Profit = Revenue - Budget"""
    df['profit_musd'] = df['revenue_musd'] - df['budget_musd']
    assert (df['profit_musd'] > 0).all()
    print(" Profit calculation is correct!")

def test_roi_calculation():
    """ROI = Revenue / Budget — should always be greater than 1"""
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    assert (df['roi'] > 1).all()
    print(" ROI calculation is correct!")


# TEST 5 — RATING CHECKS
# ============================================================

def test_rating_between_0_and_10():
    """Ratings must be between 0 and 10"""
    assert (df['vote_average'] >= 0).all()
    assert (df['vote_average'] <= 10).all()
    print(" All ratings are between 0 and 10!")

def test_vote_count_is_positive():
    """Vote count must be positive"""
    assert (df['vote_count'] > 0).all()
    print(" All vote counts are positive!")