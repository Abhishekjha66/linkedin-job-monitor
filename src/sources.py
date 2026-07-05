from models import Job


def get_google_jobs():
    return [
        Job(
            id="google-1",
            title="Frontend Developer",
            company="Google",
            location="Bangalore",
            apply_url="https://careers.google.com/",
            source="Google Careers",
        )
    ]


def get_microsoft_jobs():
    return [
        Job(
            id="microsoft-1",
            title="Software Engineer",
            company="Microsoft",
            location="Remote",
            apply_url="https://careers.microsoft.com/",
            source="Microsoft Careers",
        )
    ]