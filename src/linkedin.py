from scraper import fetch_linkedin_page
from job_parser import parse_jobs


# ============================================================
# LINKEDIN SEARCH CONFIGURATION
# ============================================================

SEARCH_KEYWORDS = [
    "Frontend Developer",
    "Frontend Engineer",
    "React Developer",
    "Software Engineer",
    "Software Developer",
    "Associate Software Engineer",
    "Associate Software Developer",
    "Full Stack Developer",
    "SDE",
    "SDE-I",
    "Graduate Engineer Trainee",
    "Graduate Trainee",
    "UI Developer",
    "Web Developer",
]


LOCATIONS = [
    "India",
    "Remote",
]


# ============================================================
# LINKEDIN JOB SEARCH
# ============================================================

def build_search_url(keyword, location):
    return (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={keyword.replace(' ', '%20')}"
        f"&location={location.replace(' ', '%20')}"
        "&f_TPR=r7200"
        "&f_E=2"
        "&sortBy=DD"
    )


def get_linkedin_jobs():
    all_jobs = []

    for keyword in SEARCH_KEYWORDS:

        for location in LOCATIONS:

            url = build_search_url(keyword, location)

            print(
                f"\nSearching LinkedIn: {keyword} | {location}"
            )

            try:
                html = fetch_linkedin_page(url)

                jobs = parse_jobs(html)

                # LinkedIn search is restricted to Entry Level.
                for job in jobs:
                    job["experience"] = "Entry Level"

                print(
                    f"Found {len(jobs)} jobs"
                )

                all_jobs.extend(jobs)

            except Exception as e:
                print(
                    f"Search failed: {keyword} | "
                    f"{location} | {e}"
                )

    return all_jobs