import sqlite3
import pandas as pd
from config import DB_PATH

def main():
    conn = sqlite3.connect(DB_PATH)
    while True:
        sql = input("SQL> ").strip()
        if sql.lower() in ("exit", "quit"):
            break
        try:
            df = pd.read_sql_query(sql, conn)
            if df.empty:
                print("Aucun résultat.")
            else:
                print(df.to_markdown(index=False))
        except Exception as e:
            print(e)
    conn.close()

if __name__ == "__main__":
    main()