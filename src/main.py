from collector import collect_jobs
from storage import save_jobs, get_new_jobs


def main():

    jobs = collect_jobs()

    save_jobs(jobs)

    new_jobs = get_new_jobs(jobs)

    print(f"\nFound {len(new_jobs)} NEW jobs\n")

    for job in new_jobs:

        print("=" * 70)
        print("Title    :", job["title"])
        print("Company  :", job["company"])
        print("Location :", job["location"])
        print("Posted   :", job["time"])
        print("Apply    :", job["url"])


if __name__ == "__main__":
    main()