import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time

BASE = "https://www.shl.com"

visited = set()
pages = []

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def extract(url):
    if url in visited:
        return

    visited.add(url)
    print("Scraping:", url)

    try:
        page = requests.get(url, headers=HEADERS).text
    except:
        return

    soup = BeautifulSoup(page, "lxml")
    title = soup.title.text if soup.title else ""

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    main = (
    soup.find("main")
    or soup.find("article")
    or soup.find("div", class_="content")
    or soup.find("body")
)
    text = main.get_text(" ", strip=True) if main else ""
    pages.append({
        "url": url,
        "title": title,
        "content": text
    })

    for a in soup.find_all("a", href=True):
        href = a["href"]
        all = urljoin(BASE, href)
        if "/products/assessments/" in all:
            extract(all)

        time.sleep(0.1)


extract("https://www.shl.com/products/assessments/")

with open("data/catalog.json","w",encoding="utf8") as f:
    json.dump(pages,f,indent=2,ensure_ascii=False)

print()
print("Pages scraped:",len(pages))