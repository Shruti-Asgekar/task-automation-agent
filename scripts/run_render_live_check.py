import os
import time
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOTS_DIR = r"C:\Users\Shruti\.gemini\antigravity\scratch\task-automation-agent\docs\screenshots"
LIVE_URL = "https://task-automation-agent-ojxn.onrender.com"

def test_live():
    print(f"Connecting to live app: {LIVE_URL}")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--disable-gpu", "--no-sandbox"]
        )
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        # Topic 1
        print("Navigating to live app on Render...")
        page.goto(LIVE_URL, wait_until="networkidle", timeout=60000)
        time.sleep(4)

        print("Testing Topic 1: MLOps Deployment on Render")
        input_elem = page.locator("input[type='text']")
        input_elem.fill("MLOps Deployment on Render")
        button = page.get_by_role("button", name="Generate Brief")
        button.click()

        page.wait_for_selector("text=Research Brief", timeout=45000)
        time.sleep(3)
        screenshot1 = os.path.join(SCREENSHOTS_DIR, "render_live_topic1.png")
        page.screenshot(path=screenshot1)
        print(f"Captured {screenshot1}")

        # Topic 2
        print("Testing Topic 2: Automated CI/CD Pipelines in 2026")
        input_elem.fill("Automated CI/CD Pipelines in 2026")
        button.click()
        time.sleep(4)

        page.wait_for_selector("text=Research Brief", timeout=45000)
        time.sleep(3)
        screenshot2 = os.path.join(SCREENSHOTS_DIR, "render_live_topic2.png")
        page.screenshot(path=screenshot2)
        print(f"Captured {screenshot2}")

        browser.close()
        print("Live testing completed successfully!")

if __name__ == "__main__":
    test_live()
