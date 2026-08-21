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

    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            "",
            "",
        )
    )


def load_sent_jobs():
    path = "data/sent_jobs.json"

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, OSError):
        return []


def save_sent_jobs(urls):
    os.makedirs("data", exist_ok=True)

    with open("data/sent_jobs.json", "w", encoding="utf-8") as f:
        json.dump(
            sorted(set(urls)),
            f,
            indent=4,
            ensure_ascii=False,
        )


def save_jobs(jobs):
    os.makedirs("data", exist_ok=True)

    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(
            jobs,
            f,
            indent=4,
            ensure_ascii=False,
        )


def get_new_jobs(jobs):
    """
    Return only jobs that have never been sent before.

    Previously sent job URLs are preserved permanently
    in data/sent_jobs.json.
    """

    old = set(load_sent_jobs())

    new_jobs = []

    # IMPORTANT:
    # Start with the existing history instead of replacing it.
    updated_sent_urls = set(old)

    for job in jobs:

        clean_url = normalize_url(job.get("url", ""))

        if not clean_url:
            continue

        job["url"] = clean_url

        # Send only if this URL has never been sent before.
        if clean_url not in old:
            new_jobs.append(job)

        # Preserve this URL in the permanent history.
        updated_sent_urls.add(clean_url)

    # Save OLD + NEW URLs.
    save_sent_jobs(updated_sent_urls)

    return new_jobs