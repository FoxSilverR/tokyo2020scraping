from playwright.sync_api import sync_playwright
import pandas as pd

def get_sports_from_seo():
    url = "https://www.olympics.com/en/olympic-games/seo/disciplines/tokyo-2020"
    sports = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_load_state("networkidle")

        try:
            page.click("button:has-text('Tout accepter')")
        except:
            pass

        page.wait_for_selector("main a", timeout=10000)

        links = page.query_selector_all("main a")

        for link in links:
            href = link.get_attribute("href")
            name = link.inner_text().strip()
            if href and "/results/" in href and name:
                full_url = href if href.startswith("http") else f"https://www.olympics.com{href}"
                sports.append({"name": name, "url": full_url})

        browser.close()

    df = pd.DataFrame(sports).drop_duplicates(subset="url")
    df.to_csv("data/sports_seo.csv", index=False, encoding="utf-8")
    print(f"{len(sports)} sports extraits et enregistrés dans data/sports_seo.csv")

if __name__ == "__main__":
    get_sports_from_seo()