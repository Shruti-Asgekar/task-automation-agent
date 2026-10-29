import subprocess
import time
import requests
import sys

def main():
    print("Starting Streamlit process...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(4)
    try:
        resp = requests.get("http://localhost:8501/_stcore/health", timeout=5)
        print("Streamlit Healthcheck Status:", resp.status_code)
        if resp.status_code == 200:
            print("Streamlit local server verified successfully!")
        else:
            print("Unexpected status code:", resp.status_code)
    except Exception as e:
        print("Failed to reach Streamlit:", e)
    finally:
        proc.terminate()
        proc.kill()
        print("Streamlit process stopped.")

if __name__ == "__main__":
    main()
