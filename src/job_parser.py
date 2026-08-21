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

        # Try to find experience information from the job card.
        experience = ""

        experience_selectors = [
            "span.job-search-card__metadata-item",
            "div.base-search-card__metadata",
            "span.base-search-card__metadata",
            "div.job-search-card__metadata",
        ]

        metadata_text = []

        for selector in experience_selectors:
            for element in card.select(selector):
                text = element.get_text(" ", strip=True)

                if text:
                    metadata_text.append(text)

        # Look for common experience phrases.
        experience_keywords = [
            "fresher",
            "freshers",
            "entry level",
            "entry-level",
            "graduate",
            "graduate trainee",
            "0 year",
            "0 years",
            "0-1 year",
            "0–1 year",
            "0 to 1 year",
            "1 year",
            "2 years",
            "2+ years",
            "3 years",
            "3+ years",
            "4 years",
            "4+ years",
            "5 years",
            "5+ years",
        ]

        for text in metadata_text:
            lower_text = text.lower()

            if any(keyword in lower_text for keyword in experience_keywords):
                experience = text
                break

        jobs.append({
            "title": title.get_text(strip=True) if title else "",
            "company": company.get_text(strip=True) if company else "",
            "location": location.get_text(strip=True) if location else "",
            "time": time.get_text(strip=True) if time else "N/A",
            "experience": experience,
            "url": link["href"] if link else "",
        })

    return jobs