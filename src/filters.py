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
    "AMD",
    "Qualcomm",
    "Visa",
    "Mastercard",
    "PayPal",
    "Walmart Global Tech",
    "Intuit",
    "ServiceNow",
    "Autodesk",
    "JPMorgan Chase",
    "Goldman Sachs",
    "Morgan Stanley",
    "Samsung",
    "Dell",
    "Siemens",
    "Ericsson",
    "Bosch",
    "GE Healthcare",
    "Honeywell",
    "Target",
}


def is_recent(posted):
    posted = (posted or "").lower()

    keywords = [
        "just now",
        "minute",
        "minutes",
        "hour",
        "hours",
        "today",
        "1 day",
        "day ago",
        "24 hours",
        "23 hours",
    ]

    return any(word in posted for word in keywords)


def is_frontend(title):
    title = (title or "").lower()

    keywords = [
        "frontend",
        "front-end",
        "front end",
        "react",
        "reactjs",
        "react.js",
        "angular",
        "vue",
        "next.js",
        "nextjs",
        "javascript",
        "typescript",
        "ui",
        "web",
        "full stack",
        "fullstack",
        "software engineer",
        "associate software engineer",
        "graduate software engineer",
        "entry level software engineer",
        "member of technical staff",
    ]

    return any(word in title for word in keywords)


def is_bangalore(location):
    location = (location or "").lower()

    return (
        "bengaluru" in location
        or "bangalore" in location
        or "remote" in location
        or "hybrid" in location
    )


def is_fresher(title):
    title = (title or "").lower()

    blocked = [
        "senior",
        "sr.",
        "lead",
        "manager",
        "principal",
        "staff engineer",
        "architect",
        "director",
        "head",
        "5+",
        "4+",
        "3+",
        "2+",
        "experienced",
        "expert",
        "qa",
        "tester",
        "testing",
        "automation tester",
        "automation engineer",
        "devops",
        "site reliability",
        "sre",
        "data engineer",
        "machine learning",
        "ml engineer",
        "ai engineer",
        "backend",
        "android",
        "ios",
    ]

    return not any(word in title for word in blocked)


def is_top_company(company):
    company = (company or "").lower().strip()

    return any(top.lower() in company for top in TOP_COMPANIES)


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