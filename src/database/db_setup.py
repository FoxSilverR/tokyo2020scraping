import sqlite3
import pandas as pd
from config import EVENTS_CSV, DB_PATH

def init_db():
    df = pd.read_csv(EVENTS_CSV)
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS sports (
      sport_id   INTEGER PRIMARY KEY AUTOINCREMENT,
      name       TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS events (
      event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
      sport_id    INTEGER NOT NULL,
      epreuve     TEXT NOT NULL,
      UNIQUE(sport_id, epreuve),
      FOREIGN KEY(sport_id) REFERENCES sports(sport_id)
    );

    CREATE TABLE IF NOT EXISTS participants (
      participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name           TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS results (
      result_id      INTEGER PRIMARY KEY AUTOINCREMENT,
      event_id       INTEGER NOT NULL,
      participant_id INTEGER NOT NULL,
      rank           INTEGER,
      UNIQUE(event_id, participant_id),
      FOREIGN KEY(event_id)       REFERENCES events(event_id),
      FOREIGN KEY(participant_id) REFERENCES participants(participant_id)
    );
    """)

    for _, row in df.iterrows():
        sport, epreuve, rang, part = (
            row["Sport"],
            row["Epreuve"],
            int(row["Rank"]),
            row["Participant"],
        )

        cur.execute("INSERT OR IGNORE INTO sports(name) VALUES(?)", (sport,))
        cur.execute("SELECT sport_id FROM sports WHERE name=?", (sport,))
        sport_id = cur.fetchone()[0]

        cur.execute(
            "INSERT OR IGNORE INTO events(sport_id, epreuve) VALUES(?, ?)",
            (sport_id, epreuve)
        )
        cur.execute(
            "SELECT event_id FROM events WHERE sport_id=? AND epreuve=?",
            (sport_id, epreuve)
        )
        event_id = cur.fetchone()[0]

        cur.execute(
            "INSERT OR IGNORE INTO participants(name) VALUES(?)",
            (part,)
        )
        cur.execute(
            "SELECT participant_id FROM participants WHERE name=?",
            (part,)
        )
        participant_id = cur.fetchone()[0]

        cur.execute(
            "INSERT OR REPLACE INTO results(event_id, participant_id, rank) VALUES(?, ?, ?)",
            (event_id, participant_id, rang)
        )

    conn.commit()
    conn.close()
    print(f"Base initialisée et peuplée dans {DB_PATH}")

if __name__ == "__main__":
    init_db()