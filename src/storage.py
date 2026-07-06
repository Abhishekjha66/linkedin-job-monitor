import json
import os
from urllib.parse import urlsplit, urlunsplit


def normalize_url(url):
    """
    Remove LinkedIn tracking parameters.
    Example:
    https://linkedin.com/jobs/view/123?trackingId=abc
    ->
    https://linkedin.com/jobs/view/123
    """
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def load_sent_jobs():
    path = "data/sent_jobs.json"

    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sent_jobs(urls):
    os.makedirs("data", exist_ok=True)

    with open("data/sent_jobs.json", "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=4)


def save_jobs(jobs):
    os.makedirs("data", exist_ok=True)

    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4, ensure_ascii=False)


def get_new_jobs(jobs):
    old = set(load_sent_jobs())

    new_jobs = []
    current_urls = []

    for job in jobs:
        clean_url = normalize_url(job["url"])
        job["url"] = clean_url

        current_urls.append(clean_url)

        if clean_url not in old:
            new_jobs.append(job)

    save_sent_jobs(current_urls)

    return new_jobs