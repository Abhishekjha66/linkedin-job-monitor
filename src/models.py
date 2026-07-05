from dataclasses import dataclass


@dataclass
class Job:
    id: str
    title: str
    company: str
    location: str
    apply_url: str
    source: str