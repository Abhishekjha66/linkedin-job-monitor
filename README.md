# LinkedIn Job Monitor

An automated, personal job-search monitoring system built with Python, Playwright, GitHub Actions, and Telegram Bot API.

The project periodically collects LinkedIn job listings, filters relevant fresher and entry-level opportunities, prevents duplicate alerts, and sends matching job notifications through Telegram.

## Key Features

- Automated job collection using Python and Playwright
- Scheduled execution through GitHub Actions every 15 minutes
- Configurable job-title and location searches
- Filtering by job title, posting recency, location, company, experience information, and application URL
- Duplicate job detection using persistent URL history
- Telegram notifications for newly discovered matching jobs
- Job history persistence through GitHub Actions commits

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Browser Automation | Playwright |
| HTML Parsing | BeautifulSoup |
| Scheduling | GitHub Actions |
| Notifications | Telegram Bot API |
| Data Storage | JSON |
| Version Control | Git and GitHub |

## Project Structure

```text
linkedin-job-monitor/
│
├── .github/
│   └── workflows/
│       └── job_monitor.yml
│
├── data/
│   ├── jobs.json
│   ├── sent_jobs.json
│   └── telegram_users.json
│
├── src/
│   ├── collector.py
│   ├── config.py
│   ├── filters.py
│   ├── job_parser.py
│   ├── linkedin.py
│   ├── main.py
│   ├── models.py
│   ├── scraper.py
│   ├── sources.py
│   ├── storage.py
│   └── telegram_bot.py
│
├── requirements.txt
└── README.md
```

## How It Works

1. GitHub Actions triggers the monitoring workflow every 15 minutes.
2. Playwright opens configured LinkedIn job-search pages.
3. BeautifulSoup extracts job information such as title, company, location, posting time, and URL.
4. The filtering module checks the collected listings against configured criteria.
5. Duplicate listings are removed using normalized job URLs.
6. Previously unreported matching jobs are sent to Telegram.
7. Job history is saved and committed to the repository.

## Configuration

Job-search keywords, company preferences, and location settings are maintained in:

```text
src/config.py
src/linkedin.py
```

The automation uses environment variables for Telegram configuration:

```env
BOT_TOKEN=your_telegram_bot_token
CHAT_IDS=your_telegram_chat_id
```

**Never commit real tokens, passwords, or private credentials to GitHub.**

For GitHub Actions, configure the following repository secrets:

- `BOT_TOKEN`
- `CHAT_IDS`

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Abhishekjha66/linkedin-job-monitor.git
cd linkedin-job-monitor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Chromium

```bash
python -m playwright install chromium
```

### 5. Configure environment variables

Create a `.env` file in the repository root and add your Telegram credentials.

### 6. Run the monitor

```bash
python -B src/main.py
```

## Automation

The GitHub Actions workflow is located at:

```text
.github/workflows/job_monitor.yml
```

It supports scheduled execution and manual triggering through GitHub Actions.

## Important Notes

- This is a personal-use automation project, not a public job-search service.
- Job availability and listing information can change.
- Automated collection depends on LinkedIn page structure and access restrictions.
- Job matching is based on configured search and filtering rules; it does not guarantee eligibility.
- Use responsibly and respect the applicable website terms and access policies.

## Author

**Abhishek Jha**

- GitHub: https://github.com/Abhishekjha66
- LinkedIn: https://www.linkedin.com/in/abhishek-jha-tech66/
- Portfolio: https://abhishekjha66.github.io/PORTFOLIO/

