import sys
from playwright.sync_api import sync_playwright

APP_URL = "https://sheettosocial-app-etecvygr55ok9vbcudm4tr.streamlit.app/"

def wake_streamlit_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print(f"Navigating to {APP_URL}...")
            page.goto(APP_URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(10000)

            wake_button = page.locator("button:has-text('Yes, get this app back up!')")
            if wake_button.count() > 0:
                print("App is sleeping. Clicking wake-up button...")
                wake_button.first.click()
                page.wait_for_timeout(30000)
                print("App wake-up triggered successfully.")
            else:
                print("App is already awake and active.")

        except Exception as e:
            print(f"Error waking app: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    wake_streamlit_app()
