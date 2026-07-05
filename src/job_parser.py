from bs4 import BeautifulSoup


def parse_jobs(html):
    soup = BeautifulSoup(html, "html.parser")

    jobs = []

    cards = soup.select("div.base-card")

    for card in cards:
        title = card.select_one("h3.base-search-card__title")
        company = card.select_one("h4.base-search-card__subtitle")
        location = card.select_one("span.job-search-card__location")
        link = card.select_one("a.base-card__full-link")
        time = card.select_one("time")

        jobs.append({
            "title": title.get_text(strip=True) if title else "",
            "company": company.get_text(strip=True) if company else "",
            "location": location.get_text(strip=True) if location else "",
            "time": time.get_text(strip=True) if time else "N/A",
            "url": link["href"] if link else ""
        })

    return jobs