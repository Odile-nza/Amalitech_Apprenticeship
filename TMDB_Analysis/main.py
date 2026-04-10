import logging
import os
import sys

# LOGGING CONFIGURATION

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        # Print logs to console
        logging.StreamHandler(sys.stdout),
        # Save logs to a file
        logging.FileHandler("pipeline.log")
    ]
)

logger = logging.getLogger(__name__)

# ============================================================
# IMPORT PIPELINE STEPS
# ============================================================

from src.fetch_data     import run_fetch_data
from src.clean_data     import run_clean_data
from src.fetch_credits  import run_fetch_credits
from src.analysis       import run_analysis
from src.visualize      import run_visualize

# ============================================================
# CREATE REQUIRED FOLDERS
# ============================================================

def create_folders():
    """
    Creates required project folders if they do not exist.
    Ensures data/ and outputs/ directories are available
    before the pipeline starts writing files.
    """
    folders = [
        "data/raw",
        "data/processed",
        "outputs"
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    logger.info("Project folders verified.")

# ============================================================
# MAIN PIPELINE FUNCTION
# ============================================================

def main():
    """
    Orchestrates the complete TMDB Movie Analysis pipeline.

    Runs the following steps in order:
        1. Fetch raw movie data from TMDB API
        2. Clean and transform the raw data
        3. Fetch cast and crew credits
        4. Calculate KPIs and perform analysis
        5. Generate visualizations

    Each step logs its progress and raises an exception
    if it fails — stopping the pipeline immediately.
    """

    logger.info("=" * 60)
    logger.info("TMDB MOVIE ANALYSIS PIPELINE STARTED")
    logger.info("=" * 60)

    # Create required folders
    create_folders()

    try:
        # Step 1 — Fetch raw movie data
        logger.info("Step 1/5 — Fetching movie data from TMDB API...")
        run_fetch_data()
        logger.info("Step 1/5 — Complete.")

        # Step 2 — Clean and transform data
        logger.info("Step 2/5 — Cleaning and transforming data...")
        run_clean_data()
        logger.info("Step 2/5 — Complete.")

        # Step 3 — Fetch cast and crew credits
        logger.info("Step 3/5 — Fetching cast and crew credits...")
        run_fetch_credits()
        logger.info("Step 3/5 — Complete.")

        # Step 4 — KPI analysis
        logger.info("Step 4/5 — Running KPI analysis...")
        run_analysis()
        logger.info("Step 4/5 — Complete.")

        # Step 5 — Visualizations
        logger.info("Step 5/5 — Generating visualizations...")
        run_visualize()
        logger.info("Step 5/5 — Complete.")

        logger.info("=" * 60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

    except Exception as e:
        # Log the error and stop the pipeline
        logger.error(f"Pipeline failed: {e}")
        logger.error("Pipeline stopped. Check logs for details.")
        sys.exit(1)

# ============================================================
# ENTRY POINT
# ============================================================
# This ensures main() only runs when this file is executed
# directly — not when imported by another module

if __name__ == "__main__":
    main()