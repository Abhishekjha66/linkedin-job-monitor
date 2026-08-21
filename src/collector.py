from linkedin import get_linkedin_jobs
from filters import apply_filters


def collect_jobs():
    print("\n" + "=" * 70)
    print("STARTING LINKEDIN JOB COLLECTION")
    print("=" * 70)

    # Use the complete LinkedIn search configuration
    # from linkedin.py:
    # - All accepted job titles
    # - India
    # - Remote
    # - Last 2 hours
    # - Newest jobs first
    all_jobs = get_linkedin_jobs()

    print(f"\nScraped jobs: {len(all_jobs)}")

    # -------------------------------------------------
    # Remove duplicates
    # Same title + company + normalized URL
    # -------------------------------------------------

    unique = {}

    for job in all_jobs:

        key = (
            job.get("title", "").strip().lower(),
            job.get("company", "").strip().lower(),
            job.get("url", "").split("?")[0].strip().lower(),
        )

        if key not in unique:

            job["url"] = job.get("url", "").split("?")[0]

            unique[key] = job

    jobs = list(unique.values())

    print(f"After duplicate removal: {len(jobs)}")

    # -------------------------------------------------
    # Apply final filters
    # -------------------------------------------------

    jobs = apply_filters(jobs)

    print(f"Final matching jobs: {len(jobs)}")

    return jobs