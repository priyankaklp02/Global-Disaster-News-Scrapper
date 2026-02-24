import requests
from bs4 import BeautifulSoup
import csv
import time
import os

def get_disaster_updates(required_count):
    base_url = "https://reliefweb.int/updates"
    headers = {"User-Agent": "Mozilla/5.0"}

    disaster_keywords = [
        "earthquake", "flood", "cyclone", "storm",
        "wildfire", "drought", "landslide",
        "tsunami", "volcano", "heatwave"
    ]

    news_list = []
    seen_titles = set()
    page = 0

    while len(news_list) < required_count:
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("h3", class_="rw-river-article__title")

        if not articles:
            break  # no more pages

        for item in articles:
            if len(news_list) >= required_count:
                break

            link_tag = item.find("a")
            if not link_tag:
                continue

            title = link_tag.get_text(strip=True)
            link = link_tag.get("href")  # already full URL

            if any(k in title.lower() for k in disaster_keywords):
                if title not in seen_titles:
                    news_list.append({
                        "title": title,
                        "link": link
                    })
                    seen_titles.add(title)

        page += 1
        time.sleep(1)  # polite scraping

    return news_list


# -------- MAIN PROGRAM --------
n = int(input("Enter how many disaster news you want to see: "))

updates = get_disaster_updates(n)

if not updates:
    print("No disaster news found.")
    exit()

# -------- SAVE TO CSV --------
file_name = "disaster_news.csv"

# Check if file already exists
file_exists = os.path.isfile(file_name)

with open(file_name, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write header only if file is new
    if not file_exists:
        writer.writerow(["No", "Title", "Link"])

    for i, news in enumerate(updates, start=1):
        writer.writerow([i,news["title"],news["link"]])

# -------- DISPLAY --------
for i, news in enumerate(updates, start=1):
    print(f"News : {i}")
    print("Title :", news["title"])
    print("Link  :", news["link"])
    print("-" * 70)

print("📰 Data stored successfully in disaster_news.csv")
print("🌍 Stay informed. Stay prepared.")
print("Created By : Priyanka Sharma and Mausumi Haldar")
print("Copyright By : AIPA(2025),NSTI(W)Kolkata")




