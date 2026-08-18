from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def fetch_linkedin_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        try:
            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # Give LinkedIn a moment to finish redirects/dynamic navigation
            page.wait_for_timeout(3000)

            # Retry page.content() if the page is still navigating
            for _ in range(3):
                try:
                    html = page.content()
                    return html
                except Exception:
                    page.wait_for_timeout(2000)

            raise RuntimeError("Unable to retrieve LinkedIn page content.")

        finally:
            browser.close()