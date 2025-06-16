import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "tokyo2020.db")

QUERIES = {
    "1. Tous les sports":
        "SELECT sport_id, name FROM sports ORDER BY name;",
    "2. Épreuves d'Archery":
        ("SELECT e.event_id, e.epreuve AS epreuve "
         "FROM events e "
         "JOIN sports s ON e.sport_id = s.sport_id "
         "WHERE s.name = 'Archery' "
         "ORDER BY epreuve;"),
    "3. Podiums du Men's 100m":
        ("SELECT r.rank, p.name AS participant "
         "FROM results r "
         "JOIN participants p ON r.participant_id = p.participant_id "
         "JOIN events e ON r.event_id = e.event_id "
         "WHERE e.epreuve = 'men-s-100m' AND r.rank <= 3 "
         "ORDER BY r.rank;"),
    "4. Top 5 3x3 Basketball femmes":
        ("SELECT r.rank, p.name AS country "
         "FROM results r "
         "JOIN participants p ON r.participant_id = p.participant_id "
         "JOIN events e ON r.event_id = e.event_id "
         "JOIN sports s ON e.sport_id = s.sport_id "
         "WHERE s.name = '3x3 Basketball' "
         "  AND e.epreuve = 'women' AND r.rank <= 5 "
         "ORDER BY r.rank;"),
    "5. Nombre d'épreuves par sport":
        ("SELECT s.name AS sport, COUNT(e.event_id) AS nb_events "
         "FROM sports s "
         "LEFT JOIN events e ON s.sport_id = e.sport_id "
         "GROUP BY s.name "
         "ORDER BY nb_events DESC;"),
}

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        for title, sql in QUERIES.items():
            print(f"\n=== {title} ===")
            df = pd.read_sql_query(sql, conn)
            if df.empty:
                print("Aucun résultat pour cette requête.")
            else:
                print(df.to_markdown(index=False))
    finally:
        conn.close()

if __name__ == "__main__":
    main()