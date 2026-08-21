import re
from urllib.parse import urlparse


# ============================================================
# ACCEPTED JOB TITLES
# ============================================================

ACCEPTED_TITLES = {
    "frontend developer",
    "frontend engineer",
    "react developer",
    "software engineer",
    "software developer",
    "associate software engineer",
    "associate software developer",
    "full stack developer",
    "sde",
    "sde-i",
    "graduate engineer trainee",
    "graduate trainee",
    "ui developer",
    "web developer",
}


# ============================================================
# TOP PRODUCT COMPANIES / MNCs
# ============================================================

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


# ============================================================
# EXPERIENCE
# ============================================================

ACCEPTED_EXPERIENCE = {
    "fresher",
    "freshers",
    "graduate",
    "graduate trainee",
    "entry level",
    "entry-level",
    "0 year",
    "0 years",
    "0-1 year",
    "0–1 year",
    "0 to 1 year",
    "0–1 years",
}


REJECTED_EXPERIENCE_PATTERNS = [
    r"\b2\+?\s*years?\b",
    r"\b3\+?\s*years?\b",
    r"\b4\+?\s*years?\b",
    r"\b5\+?\s*years?\b",
    r"\b[6-9]\+?\s*years?\b",
    r"\b1[0-9]\+?\s*years?\b",
    r"\bexperienced\b",
    r"\bsenior\b",
    r"\bsr\.\b",
    r"\blead\b",
    r"\bprincipal\b",
    r"\bmanager\b",
    r"\barchitect\b",
    r"\bdirector\b",
    r"\bstaff\b",
]


# ============================================================
# RECENCY
# ============================================================

def is_recent(posted):
    """
    Accept ONLY jobs posted less than 2 hours ago.

    Accepted:
        just now
        X minutes ago
        1 hour ago

    Rejected:
        2 hours ago
        3+ hours ago
        today
        1 day ago
        23 hours ago
        unknown / missing time
    """

    posted = (posted or "").strip().lower()

    if not posted:
        return False

    # "Just now"
    if "just now" in posted:
        return True

    # Minutes: 0–119 minutes
    minute_match = re.search(r"(\d+)\s*minute", posted)

    if minute_match:
        minutes = int(minute_match.group(1))
        return 0 <= minutes < 120

    # Hours: strictly LESS than 2 hours
    hour_match = re.search(r"(\d+)\s*hour", posted)

    if hour_match:
        hours = int(hour_match.group(1))
        return 0 <= hours < 2

    # Reject everything else:
    # today, 2 hours ago, 23 hours ago, 1 day ago, etc.
    return False


# ============================================================
# JOB TITLE
# ============================================================

def normalize_title(title):
    title = (title or "").lower().strip()

    title = title.replace("–", "-")
    title = title.replace("—", "-")

    # Remove common separators around titles.
    title = re.sub(r"\s+", " ", title)

    return title


def is_accepted_title(title):
    title = normalize_title(title)

    if not title:
        return False

    # Reject clearly non-target roles.
    rejected_terms = [
        "senior",
        "sr.",
        "lead",
        "manager",
        "principal",
        "staff engineer",
        "architect",
        "director",
        "head",
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

    if any(term in title for term in rejected_terms):
        return False

    # Exact title or title followed by a separator/details.
    for accepted in ACCEPTED_TITLES:
        if title == accepted:
            return True

        if title.startswith(accepted + " -"):
            return True

        if title.startswith(accepted + " |"):
            return True

        if title.startswith(accepted + " ("):
            return True

        if title.startswith(accepted + ","):
            return True

    # Graduate Engineer Trainee (GET)
    if title.startswith("graduate engineer trainee"):
        return True

    return False


# ============================================================
# LOCATION
# ============================================================

def is_india_or_remote(location):
    location = (location or "").strip().lower()

    if not location:
        return False

    # Remote is always accepted.
    if "remote" in location:
        return True

    # India-wide jobs.
    if "india" in location:
        return True

    # Common Indian locations in case LinkedIn omits "India".
    indian_locations = [
        "bangalore",
        "bengaluru",
        "mumbai",
        "pune",
        "hyderabad",
        "delhi",
        "new delhi",
        "gurugram",
        "gurgaon",
        "noida",
        "chennai",
        "kolkata",
        "ahmedabad",
        "jaipur",
        "kochi",
        "coimbatore",
        "indore",
        "bhubaneswar",
        "chandigarh",
        "lucknow",
        "patna",
        "thiruvananthapuram",
        "vadodara",
        "surat",
        "nagpur",
        "mysore",
        "mysuru",
    ]

    return any(city in location for city in indian_locations)


# ============================================================
# EXPERIENCE CHECK
# ============================================================

def is_fresher(job):
    """
    Strict experience check.

    The parser should eventually provide:
        job["experience"]

    Until then, title-based rejection is used as a temporary
    safety check. We will update job_parser.py next to extract
    the actual experience requirement.
    """

    experience = str(job.get("experience", "") or "").strip().lower()

    title = str(job.get("title", "") or "").lower()

    # If actual experience information exists, enforce it.
    if experience:
        normalized = experience.replace("–", "-")

        for pattern in REJECTED_EXPERIENCE_PATTERNS:
            if re.search(pattern, normalized):
                return False

        if normalized in ACCEPTED_EXPERIENCE:
            return True

        # Accept common phrases containing accepted terms.
        accepted_patterns = [
            "fresher",
            "freshers",
            "graduate",
            "graduate trainee",
            "entry level",
            "entry-level",
            "0 year",
            "0 years",
            "0-1 year",
            "0-1 years",
            "0 to 1 year",
        ]

        return any(term in normalized for term in accepted_patterns)

    # Temporary fallback until job_parser.py extracts experience.
    # Reject obviously experienced titles.
    for pattern in REJECTED_EXPERIENCE_PATTERNS:
        if re.search(pattern, title):
            return False

    # IMPORTANT:
    # Without an experience field we cannot prove a job is fresher.
    return False


# ============================================================
# COMPANY
# ============================================================

def is_top_company(company):
    company = (company or "").strip().lower()

    if not company:
        return False

    return any(
        company == top.lower()
        or company.startswith(top.lower() + " ")
        or top.lower() in company
        for top in TOP_COMPANIES
    )


# ============================================================
# APPLICATION URL
# ============================================================

def is_valid_application_url(url):
    url = (url or "").strip()

    if not url:
        return False

    try:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return False

        hostname = (parsed.hostname or "").lower()

        if not hostname:
            return False

        # LinkedIn direct job pages are accepted.
        if hostname == "linkedin.com" or hostname.endswith(".linkedin.com"):
            return "/jobs/view/" in parsed.path.lower()

        # Official career/application domains of accepted companies.
        allowed_domains = {
            "google.com",
            "careers.google.com",
            "microsoft.com",
            "amazon.jobs",
            "adobe.com",
            "atlassian.com",
            "salesforce.com",
            "uber.com",
            "airbnb.com",
            "flipkartcareers.com",
            "meesho.io",
            "swiggy.com",
            "zomato.com",
            "razorpay.com",
            "phonepe.com",
            "cred.club",
            "groww.in",
            "myntra.com",
            "paytm.com",
            "accenture.com",
            "deloitte.com",
            "oracle.com",
            "sap.com",
            "ibm.com",
            "intel.com",
            "cisco.com",
            "nvidia.com",
            "amd.com",
            "qualcomm.com",
            "visa.com",
            "mastercard.com",
            "paypal.com",
            "walmart.com",
            "intuit.com",
            "servicenow.com",
            "autodesk.com",
            "jpmorganchase.com",
            "goldmansachs.com",
            "morganstanley.com",
            "samsung.com",
            "dell.com",
            "siemens.com",
            "ericsson.com",
            "bosch.com",
            "honeywell.com",
            "target.com",
        }

        # Accept only the exact official domain or its subdomains.
        return (
            hostname in allowed_domains
            or any(hostname.endswith("." + domain) for domain in allowed_domains)
        )

    except Exception:
        return False


# ============================================================
# MAIN FILTER
# ============================================================

def apply_filters(jobs):
    filtered = []

    for job in jobs:

        title = job.get("title", "")
        company = job.get("company", "")
        location = job.get("location", "")
        posted = job.get("time", "")
        url = job.get("url", "")

        # 1. Exact accepted role
        if not is_accepted_title(title):
            continue

        # 2. Posted within 24 hours
        if not is_recent(posted):
            continue

        # 3. India / Remote
        if not is_india_or_remote(location):
            continue

        # 4. Fresher / Graduate / Entry Level / 0-1 year
        if not is_fresher(job):
            continue

        # 5. Product company / Top MNC
        if not is_top_company(company):
            continue

        # 6. Direct/official/LinkedIn job URL
        if not is_valid_application_url(url):
            continue

        filtered.append(job)

    return filtered