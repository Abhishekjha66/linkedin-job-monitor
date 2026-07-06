import asyncio

from collector import collect_jobs
from storage import save_jobs, get_new_jobs
from telegram_bot import send_message


def main():

    jobs = collect_jobs()

    save_jobs(jobs)

    new_jobs = get_new_jobs(jobs)

    print(f"\nFound {len(new_jobs)} NEW jobs\n")

    if not new_jobs:
        print("No new jobs found.")
        return

    for job in new_jobs:

        print("=" * 70)
        print("Title    :", job["title"])
        print("Company  :", job["company"])
        print("Location :", job["location"])
        print("Posted   :", job["time"])
        print("Apply    :", job["url"])

        message = f"""
🚀 <b>Fresher Job Alert</b>

💼 <b>Role:</b>
{job["title"]}

🏢 <b>Company:</b>
{job["company"]}

📍 <b>Location:</b>
{job["location"]}

🕒 <b>Posted:</b>
{job["time"]}

🔗 <b>Apply Now:</b>
{job["url"]}

━━━━━━━━━━━━━━━━━━━━
"""

        asyncio.run(send_message(message))


if __name__ == "__main__":
    main()