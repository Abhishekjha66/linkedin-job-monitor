from scraper import fetch_linkedin_page
from job_parser import parse_jobs

url = "https://www.linkedin.com/jobs/search/?keywords=Frontend%20Developer&location=Bangalore"

html = fetch_linkedin_page(url)

jobs = parse_jobs(html)

print(f"Found {len(jobs)} jobs\n")

for job in jobs[:10]:
    print("=" * 60)
    print(job["title"])
    print(job["company"])
    print(job["location"])
    print(job["url"])