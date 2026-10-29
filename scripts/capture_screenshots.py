import os
import time
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOTS_DIR = r"C:\Users\Shruti\.gemini\antigravity\scratch\task-automation-agent\docs\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def capture_remaining():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--disable-gpu", "--no-sandbox"]
        )
        context = browser.new_context(viewport={"width": 1280, "height": 850})
        page = context.new_page()

        # 1. GitHub Actions Runs
        print("Capturing GitHub Actions...")
        page.goto("https://github.com/Shruti-Asgekar/task-automation-agent/actions", wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "green_actions_run.png"))
        print("Captured green_actions_run.png")

        # 2. Specific Green Actions Run
        print("Capturing specific green CI run...")
        page.goto("https://github.com/Shruti-Asgekar/task-automation-agent/actions/runs/40833378301", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "green_ci_job_detail.png"))
        print("Captured green_ci_job_detail.png")

        # 3. Hugging Face Space Page
        print("Capturing HF Space...")
        page.goto("https://huggingface.co/spaces/ShRutIAG/task-automation-agent", wait_until="domcontentloaded", timeout=30000)
        time.sleep(4)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "hf_space_logs.png"))
        print("Captured hf_space_logs.png")

        browser.close()

if __name__ == "__main__":
    capture_remaining()
