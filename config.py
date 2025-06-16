import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
EVENTS_CSV = os.path.join(DATA_DIR, "events_rankings.csv")
DB_PATH    = os.path.join(DATA_DIR, "tokyo2020.db")