from scraper import fetch_linkedin_page
from job_parser import parse_jobs
from filters import apply_filters

KEYWORDS = [
    "Frontend Developer",
    "Frontend Engineer",
    "React Developer",
    "React Engineer",
    "UI Developer",
    "Web Developer",
    "Software Engineer Frontend",
    "Software Engineer",
    "Graduate Software Engineer",
    "Entry Level Software Engineer",
]

LOCATION = "Bangalore"


def collect_jobs():
    all_jobs = []

    for keyword in KEYWORDS:

        print(f"\nSearching: {keyword}")

        url = (
            "https://www.linkedin.com/jobs/search/"
            f"?keywords={keyword.replace(' ', '%20')}"
            f"&location={LOCATION}"
        )

        html = fetch_linkedin_page(url)

        jobs = parse_jobs(html)

        all_jobs.extend(jobs)

    # -------------------------------------------------
    # Remove duplicates
    # (same title + company + normalized URL)
    # -------------------------------------------------

    unique = {}

    for job in all_jobs:

        key = (
            job["title"].strip().lower(),
            job["company"].strip().lower(),
            job["url"].split("?")[0].strip().lower(),
        )

        if key not in unique:
            job["url"] = job["url"].split("?")[0]
            unique[key] = job

    jobs = list(unique.values())

    # Apply filters
    jobs = apply_filters(jobs)

    print(f"\nTotal matching jobs: {len(jobs)}")

    return jobs