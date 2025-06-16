import subprocess
import sys

PY = sys.executable

def main():
    subprocess.run([PY, "src/scrap/scraper.py"], check=True)
    subprocess.run([PY, "src/scrap/scraper_sport_events.py"], check=True)
    subprocess.run([PY, "-m", "src.database.db_setup"], check=True)
    subprocess.run([PY, "-m", "src.database.query_examples"], check=True)
    subprocess.run([PY, "-m", "src.database.query_db"], check=True)

if __name__ == "__main__":
    main()