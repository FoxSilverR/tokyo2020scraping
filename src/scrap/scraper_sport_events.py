import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import os
import time

DATA_DIR = r"C:\Users\Mattp\Documents\E4\projetTokyo\data"
INPUT_CSV = os.path.join(DATA_DIR, "sports_seo.csv")
OUTPUT_CSV = os.path.join(DATA_DIR, "events_rankings.csv")

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_event_links(sport_url: str) -> list:
    resp = requests.get(sport_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    anchors = soup.select('a[href*="/results/"]')
    links = set()
    for a in anchors:
        href = a.get("href")
        if href and "/en/olympic-games/tokyo-2020/results/" in href:
            full = urljoin(sport_url, href)
            links.add(full.split("?")[0])
    return sorted(links)

def scrape_event_ranking(event_url: str) -> list:
    resp = requests.get(event_url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    rows = soup.select('div[data-row-id^="event-result-row"]')
    classement = []
    for idx, row in enumerate(rows, start=1):
        ath = row.select_one('[data-cy="athlete-name"]')
        if ath:
            participant = ath.get_text(strip=True)
        else:
            cn = row.select_one('[data-cy^="country-name"]')
            participant = cn.get_text(strip=True) if cn else ""
        classement.append((idx, participant))
    return classement

def main():
    df_sports = pd.read_csv(INPUT_CSV)
    results = []
    for _, sport in df_sports.iterrows():
        sport_name = sport["name"]
        sport_url = sport["url"]
        print(f"> Traitement du sport : {sport_name}")
        try:
            event_links = get_event_links(sport_url)
        except Exception as e:
            print(f"Erreur récupération liens pour {sport_name} : {e}")
            continue
        for ev_url in event_links:
            ev_slug = ev_url.rstrip("/").split("/")[-1]
            print(f"Épreuve : {ev_slug}")
            try:
                classement = scrape_event_ranking(ev_url)
            except Exception as e:
                print(f"Erreur scraping {ev_slug} : {e}")
                continue
            for rank, participant in classement:
                results.append({
                    "Sport":       sport_name,
                    "Epreuve":     ev_slug,
                    "Rank":        rank,
                    "Participant": participant
                })
            time.sleep(1)
    df_out = pd.DataFrame(results)
    df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Tous les résultats ont été sauvegardés dans : {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
