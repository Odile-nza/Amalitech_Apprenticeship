# STEP 4: DATA VISUALIZATION

# This file creates visualizations for the TMDB movie dataset
# using Pandas and Matplotlib
#############################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Loading
df = pd.read_csv("data/analysis_movies.csv")

#converting release_date to datetime for yearly trend analysis
df['release_date'] = pd.to_datetime(df['release_date'])

#Extracting year from release_date
df['release_year'] = df['release_date'].dt.year

print(f"Data loaded: {df.shape}")

# VISUALIZATION 1 — REVENUE VS BUDGET
# ============================================================
# Line chart showing how revenue and budget changed over years

# Group by release year and calculate totals
yearly = df.groupby('release_year').agg(
    total_revenue = ('revenue_musd', 'sum'),
    total_budget  = ('budget_musd',  'sum')
).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

# Plot revenue line
ax.plot(
    yearly['release_year'],
    yearly['total_revenue'],
    marker='o',
    color='steelblue',
    linewidth=2,
    label='Total Revenue (MUSD)'
)

# Plot budget line
ax.plot(
    yearly['release_year'],
    yearly['total_budget'],
    marker='s',
    color='tomato',
    linewidth=2,
    label='Total Budget (MUSD)'
)

# Show only integer years on x axis
ax.set_xticks(yearly['release_year'])
plt.xticks(rotation=45)

ax.set_title('Revenue vs Budget Trends Over Time (Million USD)', fontsize=14, fontweight='bold')
ax.set_xlabel('Release Year', fontsize=12)
ax.set_ylabel('Amount (Million USD)', fontsize=12)
ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig('data/viz1_revenue_vs_budget.png', dpi=150)
plt.show()
print("Visualization 1 saved!")

# VISUALIZATION 2: ROI DISTRIBUTION BY GENRE

# This bar chart shows the average ROI for each genre
####################################################################

genre_df = df[['title', 'roi', 'genres']].copy()
genre_df = genre_df.dropna(subset=['roi', 'genres'])

# Split the genres string into a list
genre_df['genres'] = genre_df['genres'].str.split('|')

# Explode — each genre gets its own row
genre_df = genre_df.explode('genres')

# Calculate mean ROI per genre
genre_roi = genre_df.groupby('genres')['roi'].mean().sort_values(ascending=False).round(2)

fig, ax = plt.subplots(figsize=(12, 6))

# Generate a unique color for each genre bar
colors = plt.cm.tab20.colors[:len(genre_roi)]

# Create vertical bar chart — genre on x axis
bars = ax.bar(
    genre_roi.index,    # genre names on x axis
    genre_roi.values,   # ROI values on y axis
    color=colors,       # different color per genre
    edgecolor='black',
    linewidth=0.5
)

# Add value labels on top of each bar
for bar, val in zip(bars, genre_roi.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # center of bar
        bar.get_height() + 0.1,              # just above bar
        f'{val:.2f}x',                       # label text
        ha='center',
        fontsize=9,
        fontweight='bold'
    )

ax.set_title('Average ROI Distribution by Genre', fontsize=14, fontweight='bold')
ax.set_xlabel('Genre', fontsize=12)
ax.set_ylabel('Average ROI (Revenue / Budget)', fontsize=12)
ax.set_xticks(range(len(genre_roi.index)))
ax.set_xticklabels(genre_roi.index, rotation=45, ha='right', fontsize=9)

plt.tight_layout()
plt.savefig('data/viz2_roi_by_genre.png', dpi=150)
plt.show()
print("Visualization 2 saved!")


# VISUALIZATION 3 — POPULARITY VS RATING

# This scatter plot shows whether popular movies are also
# highly rated — are they correlated?
####################################################################

fig, ax = plt.subplots(figsize=(12, 7))

# Color each dot by franchise vs standalone
colors = df['belongs_to_collection'].apply(
    lambda x: 'royalblue' if pd.notna(x) else 'green'
)

scatter = ax.scatter(
    df['popularity'],       # x axis = popularity score
    df['vote_average'],     # y axis = rating
    c=colors,               # color by franchise/standalone
    s=200,                  # dot size
    alpha=0.8,
    edgecolors='black',
    linewidth=0.5
)

# Add movie title labels
for idx, row in df.iterrows():
    ax.annotate(
        row['title'],
        (row['popularity'], row['vote_average']),
        fontsize=7,
        xytext=(5, 5),
        textcoords='offset points'
    )

# Add legend manually
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='royalblue', label='Franchise'),
    Patch(facecolor='green',    label='Standalone')
]
ax.legend(handles=legend_elements, fontsize=10)

ax.set_title('Popularity vs Rating', fontsize=14, fontweight='bold')
ax.set_xlabel('Popularity Score', fontsize=12)
ax.set_ylabel('Vote Average (Rating)', fontsize=12)

plt.tight_layout()
plt.savefig('data/viz3_popularity_vs_rating.png', dpi=150)
plt.show()
print(" Visualization 3 saved!")


# VISUALIZATION 4: YEARLY TRENDS IN BOX OFFICE PERFORMANCE

# This line chart shows how revenue, budget and profit
# have changed over the years
####################################################################

# Group by release year and calculate totals
yearly = df.groupby('release_year').agg(
    total_revenue = ('revenue_musd', 'sum'),
    total_budget  = ('budget_musd',  'sum'),
    total_profit  = ('profit_musd',  'sum'),
    movie_count   = ('title',        'count')
).reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot revenue, budget and profit as lines
ax1.plot(yearly['release_year'], yearly['total_revenue'],
         marker='o', color='green',  linewidth=2, label='Total Revenue')
ax1.plot(yearly['release_year'], yearly['total_budget'],
         marker='s', color='red',    linewidth=2, label='Total Budget')
ax1.plot(yearly['release_year'], yearly['total_profit'],
         marker='^', color='blue',   linewidth=2, label='Total Profit')

# Add movie count as bar chart on secondary axis
ax2 = ax1.twinx()   # create a second y axis sharing the same x axis
ax2.bar(
    yearly['release_year'],
    yearly['movie_count'],
    alpha=0.2,          # very transparent
    color='gray',
    label='Movie Count'
)
ax2.set_ylabel('Number of Movies', fontsize=11)
ax2.set_ylim(0, yearly['movie_count'].max() * 5)  # scale bars down

# Add value labels on each data point
for idx, row in yearly.iterrows():
    ax1.annotate(
        f"${row['total_revenue']:.0f}M",
        (row['release_year'], row['total_revenue']),
        textcoords='offset points',
        xytext=(0, 8),
        fontsize=7,
        color='green'
    )

ax1.set_title('Yearly Box Office Trends (Million USD)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Release Year', fontsize=12)
ax1.set_ylabel('Amount (Million USD)', fontsize=12)
ax1.legend(loc='upper left',  fontsize=10)
ax2.legend(loc='upper right', fontsize=10)

# Set x axis to show only integer years
ax1.set_xticks(yearly['release_year'])
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('data/viz4_yearly_trends.png', dpi=150)
plt.show()
print("Visualization 4 saved!")

# VISUALIZATION 5: FRANCHISE VS STANDALONE SUCCESS

# This grouped bar chart compares franchise and standalone movies across multiple KPIs
#########################################################################################

# Calculate averages for franchise vs standalone
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

# Create a grouped bar chart with multiple subplots
fig, axes = plt.subplots(1, 5, figsize=(18, 6))

# List of metrics and their labels
metrics = [
    ('mean_revenue',    'Mean Revenue\n(Million USD)',    'steelblue'),
    ('mean_budget',     'Mean Budget\n(Million USD)',     'tomato'),
    ('mean_profit',     'Mean Profit\n(Million USD)',     'green'),
    ('mean_popularity', 'Mean Popularity',                'purple'),
    ('mean_rating',     'Mean Rating',                   'orange'),
]

# Plot each metric as a separate bar chart
for ax, (metric, label, color) in zip(axes, metrics):
    bars = ax.bar(
        comparison.index,        # Franchise, Standalone
        comparison[metric],      # values
        color=[color, 'lightgray'],
        edgecolor='black',
        linewidth=0.5
    )

    # Add value labels on top of each bar
    for bar, val in zip(bars, comparison[metric]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # center of bar
            bar.get_height() + 0.5,              # just above bar
            f'{val:.1f}',                        # value label
            ha='center',
            fontsize=9,
            fontweight='bold'
        )

    ax.set_title(label, fontsize=10, fontweight='bold')
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=15)

fig.suptitle('Franchise vs Standalone Movie Performance',
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('data/viz5_franchise_vs_standalone.png', dpi=150, bbox_inches='tight')
plt.show()
print("Visualization 5 saved!")