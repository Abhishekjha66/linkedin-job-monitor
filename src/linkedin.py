from scraper import fetch_linkedin_page
from job_parser import parse_jobs

URL = (
    "https://www.linkedin.com/jobs/search/"
    "?keywords=Frontend%20Developer"
    "&location=Bangalore"
)


def get_linkedin_jobs():
    html = fetch_linkedin_page(URL)
    jobs = parse_jobs(html)
    return jobs