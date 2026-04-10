# ============================================================
# Step 4: Data Visualization
# ============================================================
# Generates visualizations from the analysis dataset
# and saves them as PNG files in the outputs/ folder.
# ============================================================

import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from config import ANALYSIS_DATA_PATH, OUTPUT_PATH

# Get logger for this module
logger = logging.getLogger(__name__)

# Use a clean consistent style for all charts
plt.style.use('ggplot')


# ============================================================
# HELPER FUNCTION — SAVE CHART
# ============================================================

def save_chart(filename: str) -> None:
    """
    Saves the current matplotlib figure to the outputs folder.

    Why tight_layout: Prevents labels and titles from being
    clipped or overlapping when the chart is saved.

    Args:
        filename (str): Name of the output PNG file.
    """
    filepath = os.path.join(OUTPUT_PATH, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    logger.info(f"Chart saved: {filepath}")


# ============================================================
# VISUALIZATION 1 — REVENUE VS BUDGET TRENDS
# ============================================================

def plot_revenue_vs_budget(df: pd.DataFrame) -> None:
    """
    Plots total revenue and budget trends over time as a
    line chart showing year-by-year changes.

    Why line chart: Shows how values change over time
    (trend) rather than comparing individual movie values.
    A scatter plot would show relationships, not trends.

    Args:
        df (pd.DataFrame): Analysis DataFrame with
                           release_year column.
    """
    # Group by year and sum revenue and budget
    yearly = df.groupby('release_year').agg(
        total_revenue = ('revenue_musd', 'sum'),
        total_budget  = ('budget_musd',  'sum')
    ).reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot revenue and budget trend lines
    ax.plot(
        yearly['release_year'], yearly['total_revenue'],
        marker='o', color='steelblue', linewidth=2,
        label='Total Revenue (MUSD)'
    )
    ax.plot(
        yearly['release_year'], yearly['total_budget'],
        marker='s', color='tomato', linewidth=2,
        label='Total Budget (MUSD)'
    )

    # Add value labels on each data point
    for _, row in yearly.iterrows():
        ax.annotate(
            f"${row['total_revenue']:.0f}M",
            (row['release_year'], row['total_revenue']),
            textcoords='offset points',
            xytext=(0, 8), fontsize=8, color='steelblue'
        )

    ax.set_xticks(yearly['release_year'])
    ax.set_title(
        'Revenue vs Budget Trends Over Time (Million USD)',
        fontsize=14, fontweight='bold', pad=15
    )
    ax.set_xlabel('Release Year', fontsize=12)
    ax.set_ylabel('Amount (Million USD)', fontsize=12)
    ax.legend(fontsize=11)
    plt.xticks(rotation=45)

    save_chart('viz1_revenue_vs_budget.png')


# ============================================================
# VISUALIZATION 2 — ROI DISTRIBUTION BY GENRE
# ============================================================

def plot_roi_by_genre(df: pd.DataFrame) -> None:
    """
    Plots average ROI for each genre as a horizontal bar chart
    sorted from highest to lowest ROI.

    Why horizontal bars: Genre names are long strings that
    overlap when placed on the x-axis. Horizontal bars give
    each label enough space to be fully readable.

    Args:
        df (pd.DataFrame): Analysis DataFrame with
                           genres and roi columns.
    """
    # Explode genres since one movie can have multiple
    # Why explode: "Action|Adventure" must be split so each
    # genre gets its own row for accurate per-genre analysis
    genre_df = df[['roi', 'genres']].dropna()
    genre_df = genre_df.copy()
    genre_df['genres'] = genre_df['genres'].str.split('|')
    genre_df = genre_df.explode('genres')

    # Calculate mean ROI per genre
    genre_roi = (
        genre_df.groupby('genres')['roi']
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.barh(
        genre_roi.index,
        genre_roi.values,
        color='steelblue',
        edgecolor='black',
        linewidth=0.5
    )

    # Add value labels at end of each bar
    for bar, val in zip(bars, genre_roi.values):
        ax.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            f'{val:.2f}x',
            va='center', fontsize=10
        )

    ax.set_title(
        'Average ROI Distribution by Genre',
        fontsize=14, fontweight='bold', pad=15
    )
    ax.set_xlabel('Average ROI (Revenue / Budget)', fontsize=12)
    ax.set_ylabel('Genre', fontsize=12)

    save_chart('viz2_roi_by_genre.png')


# ============================================================
# VISUALIZATION 3 — POPULARITY VS RATING
# ============================================================

def plot_popularity_vs_rating(df: pd.DataFrame) -> None:
    """
    Plots popularity score against vote average as a scatter
    plot to explore whether popular movies are also
    highly rated.

    Why scatter plot: Best for showing the relationship
    between two continuous numerical variables.

    Args:
        df (pd.DataFrame): Analysis DataFrame with
                           popularity and vote_average.
    """
    from matplotlib.patches import Patch

    # Color by franchise vs standalone
    # Why: Adds a third dimension showing movie type
    # without cluttering the chart with additional axes
    colors = df['belongs_to_collection'].apply(
        lambda x: 'royalblue' if pd.notna(x) else 'tomato'
    )

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.scatter(
        df['popularity'], df['vote_average'],
        c=colors, s=200, alpha=0.8,
        edgecolors='black', linewidth=0.5
    )

    # Add movie title labels
    for _, row in df.iterrows():
        ax.annotate(
            row['title'],
            (row['popularity'], row['vote_average']),
            fontsize=7, xytext=(5, 5),
            textcoords='offset points'
        )

    # Manual legend for franchise vs standalone
    legend_elements = [
        Patch(facecolor='royalblue', label='Franchise'),
        Patch(facecolor='tomato',    label='Standalone')
    ]
    ax.legend(handles=legend_elements, fontsize=10)

    ax.set_title(
        'Popularity vs Rating',
        fontsize=14, fontweight='bold', pad=15
    )
    ax.set_xlabel('Popularity Score', fontsize=12)
    ax.set_ylabel('Vote Average (Rating out of 10)', fontsize=12)

    save_chart('viz3_popularity_vs_rating.png')


# ============================================================
# VISUALIZATION 4 — YEARLY BOX OFFICE TRENDS
# ============================================================

def plot_yearly_trends(df: pd.DataFrame) -> None:
    """
    Plots yearly box office performance showing total revenue,
    budget and profit trends with movie count as bars.

    Why dual axis: Revenue values (thousands of millions) and
    movie count (single digits) have very different scales.
    A second y-axis allows both to be displayed clearly
    without one dominating the other.

    Args:
        df (pd.DataFrame): Analysis DataFrame with
                           release_year and financial columns.
    """
    yearly = df.groupby('release_year').agg(
        total_revenue = ('revenue_musd', 'sum'),
        total_budget  = ('budget_musd',  'sum'),
        total_profit  = ('profit_musd',  'sum'),
        movie_count   = ('title',        'count')
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot revenue, budget and profit lines
    ax1.plot(
        yearly['release_year'], yearly['total_revenue'],
        marker='o', color='green', linewidth=2,
        label='Total Revenue'
    )
    ax1.plot(
        yearly['release_year'], yearly['total_budget'],
        marker='s', color='red', linewidth=2,
        label='Total Budget'
    )
    ax1.plot(
        yearly['release_year'], yearly['total_profit'],
        marker='^', color='blue', linewidth=2,
        label='Total Profit'
    )

    # Add revenue labels on data points
    for _, row in yearly.iterrows():
        ax1.annotate(
            f"${row['total_revenue']:.0f}M",
            (row['release_year'], row['total_revenue']),
            textcoords='offset points',
            xytext=(0, 8), fontsize=7, color='green'
        )

    # Second y-axis for movie count bars
    # Why twinx(): Creates a shared x-axis with independent y-axes
    ax2 = ax1.twinx()
    ax2.bar(
        yearly['release_year'], yearly['movie_count'],
        alpha=0.2, color='gray', label='Movie Count'
    )
    ax2.set_ylabel('Number of Movies', fontsize=11)
    ax2.set_ylim(0, yearly['movie_count'].max() * 5)

    ax1.set_xticks(yearly['release_year'])
    ax1.set_title(
        'Yearly Box Office Trends (Million USD)',
        fontsize=14, fontweight='bold', pad=15
    )
    ax1.set_xlabel('Release Year', fontsize=12)
    ax1.set_ylabel('Amount (Million USD)', fontsize=12)
    ax1.legend(loc='upper left',  fontsize=10)
    ax2.legend(loc='upper right', fontsize=10)
    plt.xticks(rotation=45)

    save_chart('viz4_yearly_trends.png')


# ============================================================
# VISUALIZATION 5 — FRANCHISE VS STANDALONE
# ============================================================

def plot_franchise_vs_standalone(df: pd.DataFrame) -> None:
    """
    Compares franchise and standalone movie performance
    across 5 KPI metrics using grouped bar charts.

    Why 5 subplots: Each KPI has a different scale making
    a single chart unreadable. Separate subplots allow
    each metric to use its own y-axis scale.

    Args:
        df (pd.DataFrame): Analysis DataFrame with
                           movie_type and KPI columns.
    """
    # Classify franchise vs standalone
    df = df.copy()
    df['movie_type'] = df['belongs_to_collection'].apply(
        lambda x: 'Franchise' if pd.notna(x) else 'Standalone'
    )

    comparison = df.groupby('movie_type').agg(
        mean_revenue    = ('revenue_musd', 'mean'),
        mean_budget     = ('budget_musd',  'mean'),
        mean_profit     = ('profit_musd',  'mean'),
        mean_popularity = ('popularity',   'mean'),
        mean_rating     = ('vote_average', 'mean')
    ).round(2)

    metrics = [
        ('mean_revenue',    'Mean Revenue\n(Million USD)',  'steelblue'),
        ('mean_budget',     'Mean Budget\n(Million USD)',   'tomato'),
        ('mean_profit',     'Mean Profit\n(Million USD)',   'green'),
        ('mean_popularity', 'Mean Popularity',              'purple'),
        ('mean_rating',     'Mean Rating',                  'orange'),
    ]

    fig, axes = plt.subplots(1, 5, figsize=(18, 6))

    for ax, (metric, label, color) in zip(axes, metrics):
        bars = ax.bar(
            comparison.index,
            comparison[metric],
            color=[color, 'lightgray'],
            edgecolor='black',
            linewidth=0.5
        )

        # Add value labels on top of each bar
        for bar, val in zip(bars, comparison[metric]):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f'{val:.1f}',
                ha='center', fontsize=9, fontweight='bold'
            )

        ax.set_title(label, fontsize=10, fontweight='bold')
        ax.tick_params(axis='x', rotation=15)

    fig.suptitle(
        'Franchise vs Standalone Movie Performance',
        fontsize=14, fontweight='bold', y=1.02
    )

    save_chart('viz5_franchise_vs_standalone.png')


# ============================================================
# MAIN FUNCTION
# ============================================================

def run_visualize():
    """
    Entry point for the visualization step.

    Loads analysis data and generates all 5 visualizations.
    Called by main.py as Step 5 of the pipeline.
    """
    logger.info("Starting visualization generation...")

    # Load analysis data from previous step
    df = pd.read_csv(ANALYSIS_DATA_PATH)

    # Convert release_date to datetime and extract year
    df['release_date'] = pd.to_datetime(
        df['release_date'], errors='coerce'
    )
    df['release_year'] = df['release_date'].dt.year

    logger.info(f"Analysis data loaded. Shape: {df.shape}")

    # Generate all visualizations
    plot_revenue_vs_budget(df)
    plot_roi_by_genre(df)
    plot_popularity_vs_rating(df)
    plot_yearly_trends(df)
    plot_franchise_vs_standalone(df)

    logger.info(
        f"All visualizations saved to {OUTPUT_PATH}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
    run_visualize()