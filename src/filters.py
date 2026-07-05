TOP_COMPANIES = {
    "Google",
    "Microsoft",
    "Amazon",
    "Adobe",
    "Atlassian",
    "Salesforce",
    "LinkedIn",
    "Uber",
    "Airbnb",
    "Flipkart",
    "Meesho",
    "Swiggy",
    "Zomato",
    "Razorpay",
    "PhonePe",
    "CRED",
    "Groww",
    "Myntra",
    "Paytm",
    "Accenture",
    "CGI",
    "Ecolab",
    "PVH Corp.",
    "HappyFox",
    "Deloitte",
    "Oracle",
    "SAP",
    "IBM",
    "Intel",
    "Cisco",
    "NVIDIA",
}


def is_recent(posted):
    posted = (posted or "").lower()

    keywords = [
        "today",
        "hour",
        "hours",
        "minute",
        "minutes",
        "just now",
        "1 day",
    ]

    return any(k in posted for k in keywords)


def is_frontend(title):
    title = (title or "").lower()

    keywords = [
        "frontend",
        "front-end",
        "front end",
        "react",
        "javascript",
        "ui",
        "web",
        "angular",
        "vue",
    ]

    return any(k in title for k in keywords)


def is_bangalore(location):
    location = (location or "").lower()

    return (
        "bengaluru" in location
        or "bangalore" in location
        or "remote" in location
        or "hybrid" in location
    )


def is_fresher(title):
    """
    Reject senior roles.
    Keep fresher / junior roles.
    """
    title = (title or "").lower()

    blocked = [
        "senior",
        "sr.",
        "lead",
        "manager",
        "principal",
        "staff",
        "architect",
        "director",
        "head",
        "5+",
        "4+",
        "3+",
        "2+",
        "experienced",
        "expert",
    ]

    return not any(word in title for word in blocked)


def is_top_company(company):
    company = (company or "").strip()
    return company in TOP_COMPANIES


def apply_filters(jobs):
    filtered = []

    for job in jobs:

        if not is_frontend(job["title"]):
            continue

        if not is_recent(job["time"]):
            continue

        if not is_bangalore(job["location"]):
            continue

        if not is_fresher(job["title"]):
            continue

        if not is_top_company(job["company"]):
            continue

        filtered.append(job)

    return filtered