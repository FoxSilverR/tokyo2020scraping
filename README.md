# Tokyo 2020 Scraping

A Python project to scrape, organize, and analyze the results of the Tokyo 2020 Olympic Games. This project extracts sports, events, and participant rankings from the official Olympics website, stores them in a local database, and provides query tools for data exploration.

## Features

- **Web Scraping**: Collects sports and event data from the Tokyo 2020 Olympic Games website using Playwright and BeautifulSoup.
- **Data Storage**: Stores structured data (sports, events, participants, results) in a local SQLite database.
- **CSV Export**: Outputs intermediate and final data as CSV files for further analysis.
- **Data Querying**: Example and interactive scripts to run SQL queries against the dataset.

## Project Structure

```
main.py                       # Orchestrates the scraping and database setup pipeline
config.py                     # Paths and basic configuration
src/
  scrap/
    scraper.py                # Scrapes list of sports and their URLs
    scraper_sport_events.py   # Scrapes event and ranking data for each sport
  database/
    db_setup.py               # Creates and populates the SQLite database
    query_examples.py         # Runs example queries on the database
    query_db.py               # Interactive SQL querying shell
data/
  sports_seo.csv              # Scraped sports data (generated)
  events_rankings.csv         # Scraped event results data (generated)
  tokyo2020.db                # SQLite database (generated)
```

## Setup

### Requirements

- Python 3.7+
- [Playwright](https://playwright.dev/python/) (`pip install playwright`)
- pandas
- requests
- beautifulsoup4

Install requirements:
```bash
pip install -r requirements.txt
playwright install
```

### Directory Structure

- Ensure a `data/` directory exists at the project root:
  ```
  mkdir data
  ```

## Usage

Run the full scraping and database pipeline:
```bash
python main.py
```

### Script Details

- `main.py` runs all steps in order:
  1. Scrapes sports (`scraper.py`) → `data/sports_seo.csv`
  2. Scrapes events and rankings (`scraper_sport_events.py`) → `data/events_rankings.csv`
  3. Sets up and populates the SQLite database (`db_setup.py`)
  4. Shows example queries (`query_examples.py`)
  5. Launches an interactive SQL shell (`query_db.py`)

- To run individual scripts:
  ```bash
  python src/scrap/scraper.py
  python src/scrap/scraper_sport_events.py
  python src/database/db_setup.py
  python src/database/query_examples.py
  python src/database/query_db.py
  ```

## Example Queries

Some example queries included in `query_examples.py`:
- List all sports
- List all events for a given sport (e.g., Archery)
- Show podium for Men's 100m
- Top 5 for Women's 3x3 Basketball
- Number of events per sport

## Notes

- The scraping scripts target the official [olympics.com Tokyo 2020 results pages](https://www.olympics.com/en/olympic-games/seo/disciplines/tokyo-2020).
- Some scripts may require manual intervention (such as accepting cookies in Playwright).
- Ensure your environment supports running a browser (for Playwright).

