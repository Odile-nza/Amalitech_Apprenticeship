# TMDB Movie Data Analysis

A complete end-to-end data engineering pipeline that fetches movie data from the TMDB API, cleans and transforms the dataset, calculates key performance indicators and presents findings through visualizations.

Built as part of the **AmaliTech Data Engineering Apprenticeship Programme**.

---

## Project Structure

```
TMDB_Analysis/
├── src/
│   ├── fetch_data.py         Step 1: Fetch raw movie data from TMDB API
│   ├── clean_data.py         Step 2: Clean and transform raw data
│   ├── fetch_credits.py      Step 3: Fetch cast and crew credits
│   ├── analysis.py           Step 4: KPI calculations and analysis
│   └── visualize.py          Step 5: Generate visualizations
├── data/
│   ├── raw/                  Raw data from TMDB API
│   └── processed/            Cleaned and analysis-ready data
├── outputs/                  Generated chart PNG files
├── tests/
│   ├── __init__.py
│   ├── create_test_data.py   Generates test data file
│   └── test_movies.py        Unit test cases
├── config.py                 Central configuration and settings
├── main.py                   Pipeline orchestrator
├── requirements.txt          Pinned Python dependencies
├── .env                      API key (not committed to GitHub)
├── .gitignore
└── README.md
```

---

## Project Objectives

- **API Data Extraction** — Fetch movie data from the TMDB API with retry logic and timeout handling
- **Data Cleaning** — Clean, transform and structure raw data for analysis
- **KPI Implementation** — Calculate profit, ROI and rankings across 10 metrics
- **Franchise Analysis** — Compare franchise vs standalone movie performance
- **Director Analysis** — Identify the most successful directors
- **Visualization** — Present key findings through 5 chart types

---

## Pipeline Steps

### Step 1 — Fetch Movie Data (`src/fetch_data.py`)
Connects to the TMDB API and fetches data for 18 movies. Implements retry logic with exponential backoff and request timeout to handle network errors gracefully. Saves raw data to `data/raw/raw_movies.csv`.

### Step 2 — Clean and Transform (`src/clean_data.py`)
Drops irrelevant columns, parses nested JSON fields like genres and production companies, fixes data types, replaces unrealistic zero values with NaN and converts budget and revenue to Million USD. Saves cleaned data to `data/processed/clean_movies.csv`.

### Step 3 — Fetch Credits (`src/fetch_credits.py`)
Fetches cast and crew data from the TMDB credits endpoint. Extracts the top 10 cast members and director for each movie. Saves enriched data to `data/processed/final_movies.csv`.

### Step 4 — KPI Analysis (`src/analysis.py`)
Calculates profit and ROI columns. Ranks movies across 10 KPI metrics using a reusable `rank_movies()` function. Performs franchise vs standalone comparison and director analysis. Saves results to `data/processed/analysis_movies.csv`.

### Step 5 — Visualization (`src/visualize.py`)
Generates 5 charts and saves them to the `outputs/` folder.

---

## Key Findings

### Top Performing Movies

| Rank | Movie | Revenue (MUSD) | Budget (MUSD) | ROI |
|---|---|---|---|---|
| 1 | Avatar | 2,923.7 | 237.0 | 12.3x |
| 2 | Avengers: Endgame | 2,799.4 | 356.0 | 7.9x |
| 3 | Titanic | 2,264.2 | 200.0 | 11.3x |

### Franchise vs Standalone

| Type | Mean Revenue | Median ROI | Mean Rating |
|---|---|---|---|
| Franchise | 1,682.7M | 7.79x | 7.39 |
| Standalone | 1,765.1M | 9.62x | 7.44 |

### Most Successful Directors

| Director | Movies | Total Revenue |
|---|---|---|
| James Cameron | 2 | 5,187.9M |
| Joss Whedon | 2 | 2,924.2M |

---

## Visualizations & Insights

### Visualization 1 — Revenue vs Budget Trends Over Time
Revenue consistently stayed above budget across all years. The biggest peak was 2015 with $6,661M total revenue driven by multiple blockbuster releases.

### Visualization 2 — ROI Distribution by Genre
Comedy and Romance genres delivered the highest ROI at 9.69x and 9.62x. Action and Animation had the lowest ROI despite being the most common blockbuster genres due to high production costs.

### Visualization 3 — Popularity vs Rating
No strong correlation between popularity and rating. The Avengers was the most popular but not the highest rated — showing audiences value entertainment and quality differently.

### Visualization 4 — Yearly Box Office Trends
Box office performance peaked in 2015 at $6,661M. The gap between revenue and budget widens over time suggesting increasing profitability.

### Visualization 5 — Franchise vs Standalone Performance
Standalone movies slightly outperformed franchise movies across all KPIs — however this result is based on only 2 standalone movies and is not statistically reliable.

---

## Conclusion

All 18 movies were financially successful with every movie earning significantly more than its budget. Higher budget does not guarantee higher ROI — Avatar achieved 12.3x ROI with a $237M budget while Avengers: Endgame had a $356M budget but only 7.9x ROI. Comedy and Romance genres deliver the best return on investment despite lower production budgets.

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Odile-nza/Amalitech_Apprenticeship.git
cd TMDB_Analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
```
TMDB_API_KEY=your_api_key_here
```

### 4. Run the full pipeline
```bash
python main.py
```

### 5. Run individual steps
```bash
python src/fetch_data.py
python src/clean_data.py
python src/fetch_credits.py
python src/analysis.py
python src/visualize.py
```

### 6. Run tests
```bash
pytest tests/test_movies.py -v
```

---

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Python 3.11 | Programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Requests | TMDB API calls |
| python-dotenv | Secure API key management |
| pytest | Unit testing |
| Git | Version control |

---

## Author

Odile Nzambazamariya — AmaliTech Data Engineering Apprentice