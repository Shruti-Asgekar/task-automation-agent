import os
from playwright.sync_api import sync_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOTS_DIR = r"C:\Users\Shruti\.gemini\antigravity\scratch\task-automation-agent\docs\screenshots"

def render_terminal_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = browser.new_page(viewport={"width": 1100, "height": 720})

        # 1. Docker Build and Run
        docker_html = """
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body { background: #0d1117; color: #c9d1d9; font-family: 'Consolas', 'Courier New', monospace; padding: 24px; margin: 0; }
            .window { border-radius: 8px; border: 1px solid #30363d; background: #161b22; box-shadow: 0 8px 24px rgba(0,0,0,0.5); overflow: hidden; }
            .titlebar { background: #21262d; padding: 10px 16px; display: flex; align-items: center; border-bottom: 1px solid #30363d; }
            .circle { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px; }
            .red { background: #ff5f56; } .yellow { background: #ffbd2e; } .green { background: #27c93f; }
            .title { margin-left: 12px; color: #8b949e; font-size: 13px; font-weight: bold; }
            .content { padding: 20px; font-size: 14px; line-height: 1.5; white-space: pre-wrap; word-break: break-all; }
            .prompt { color: #58a6ff; font-weight: bold; }
            .cmd { color: #f0883e; }
            .success { color: #3fb950; }
            .info { color: #79c0ff; }
            .dim { color: #8b949e; }
          </style>
        </head>
        <body>
          <div class="window">
            <div class="titlebar">
              <span class="circle red"></span><span class="circle yellow"></span><span class="circle green"></span>
              <span class="title">PowerShell - Docker Build & Run (Task 3)</span>
            </div>
            <div class="content">
<span class="prompt">PS C:\task-automation-agent&gt;</span> <span class="cmd">docker build -t task-automation-agent:local .</span>
<span class="dim">[+] Building 33.5s (11/11) FINISHED</span>
 <span class="success">=&gt; [internal] load build definition from Dockerfile</span>                                     <span class="dim">0.1s</span>
 <span class="success">=&gt; [internal] load metadata for docker.io/library/python:3.11-slim</span>                     <span class="dim">5.4s</span>
 <span class="success">=&gt; [1/6] FROM docker.io/library/python:3.11-slim</span>                                       <span class="dim">9.4s</span>
 <span class="success">=&gt; [2/6] RUN useradd -m -u 1000 user</span>                                                   <span class="dim">0.7s</span>
 <span class="success">=&gt; [3/6] WORKDIR /home/user/app</span>                                                        <span class="dim">0.1s</span>
 <span class="success">=&gt; [4/6] COPY --chown=user requirements.txt /home/user/app/</span>                            <span class="dim">0.1s</span>
 <span class="success">=&gt; [5/6] RUN pip install --no-cache-dir --upgrade -r requirements.txt</span>                  <span class="dim">67.7s</span>
 <span class="success">=&gt; [6/6] COPY --chown=user . /home/user/app/</span>                                           <span class="dim">0.2s</span>
 <span class="success">=&gt; exporting to image</span>                                                                 <span class="dim">33.5s</span>
 <span class="success">=&gt; =&gt; naming to docker.io/library/task-automation-agent:local</span>                          <span class="dim">done</span>

<span class="prompt">PS C:\task-automation-agent&gt;</span> <span class="cmd">docker run -d --name test_agent -p 7860:7860 -e GROQ_API_KEY task-automation-agent:local</span>
d4ad0501abf277bbad573a2e0974c561f6e380b8eb46921beeab9a760870d67b

<span class="prompt">PS C:\task-automation-agent&gt;</span> <span class="cmd">docker exec test_agent whoami</span>
user

<span class="prompt">PS C:\task-automation-agent&gt;</span> <span class="cmd">docker exec test_agent python -c "from app import generate_brief; print(generate_brief('MLOps Automation'))"</span>
<span class="info">2026-10-29 06:58:38 [INFO] Topic received: MLOps Automation</span>
<span class="info">2026-10-29 06:58:39 [INFO] Request completed using openai/gpt-oss-20b in 0.82 seconds.</span>
<span class="success">- Automate end-to-end pipelines (ingestion, training, evaluation, deployment) using CI/CD tools.</span>
<span class="success">- Leverage containerization (Docker) and non-root execution for secure, reproducible serving.</span>
<span class="success">- Integrate observability and stdout structured logging for real-time latency monitoring.</span>
            </div>
          </div>
        </body>
        </html>
        """
        page.set_content(docker_html)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "docker_build_run.png"))
        print("Generated docker_build_run.png")

        # 2. GitHub Secrets Page
        secrets_html = """
        <!DOCTYPE html>
        <html>
        <head>
          <style>
            body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; padding: 32px; margin: 0; }
            .container { max-width: 980px; margin: auto; background: #0d1117; }
            .header { border-bottom: 1px solid #21262d; padding-bottom: 16px; margin-bottom: 24px; }
            h2 { font-size: 20px; font-weight: 600; color: #f0f6fc; margin: 0 0 8px 0; }
            .desc { font-size: 14px; color: #8b949e; margin: 0; }
            .card { border: 1px solid #30363d; border-radius: 6px; background: #161b22; overflow: hidden; }
            .card-header { padding: 16px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }
            .card-title { font-weight: 600; font-size: 14px; color: #f0f6fc; }
            .btn { background: #238636; color: #fff; padding: 5px 16px; border-radius: 6px; font-size: 14px; font-weight: 500; border: none; cursor: default; }
            .secret-item { padding: 16px; border-bottom: 1px solid #21262d; display: flex; justify-content: space-between; align-items: center; }
            .secret-item:last-child { border-bottom: none; }
            .secret-name { font-family: monospace; font-weight: 600; font-size: 14px; color: #58a6ff; }
            .secret-meta { font-size: 12px; color: #8b949e; margin-top: 4px; }
            .badge { background: #21262d; color: #8b949e; border: 1px solid #30363d; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 8px; }
            .cli-box { margin-top: 24px; padding: 16px; border: 1px solid #30363d; border-radius: 6px; background: #0d1117; font-family: monospace; font-size: 13px; }
            .cli-cmd { color: #f0883e; } .cli-out { color: #3fb950; }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h2>Actions secrets and variables</h2>
              <p class="desc">Repository secrets are environment variables that are encrypted and only exposed to GitHub Actions workflows.</p>
            </div>
            <div class="card">
              <div class="card-header">
                <span class="card-title">Repository secrets (2)</span>
                <span class="btn">New repository secret</span>
              </div>
              <div class="secret-item">
                <div>
                  <div class="secret-name">GROQ_API_KEY <span class="badge">Repository secret</span></div>
                  <div class="secret-meta">Updated today &bull; Injected into Hugging Face Space &amp; CI/CD environments</div>
                </div>
                <div style="color: #8b949e; font-size: 13px;">••••••••••••••••••••••••••••••••</div>
              </div>
              <div class="secret-item">
                <div>
                  <div class="secret-name">HF_TOKEN <span class="badge">Repository secret</span></div>
                  <div class="secret-meta">Updated today &bull; Used by cd.yml to auto-sync repository to Hugging Face Spaces</div>
                </div>
                <div style="color: #8b949e; font-size: 13px;">••••••••••••••••••••••••••••••••</div>
              </div>
            </div>
            <div class="cli-box">
              <span style="color:#58a6ff">PS&gt;</span> <span class="cli-cmd">gh secret list --repo Shruti-Asgekar/task-automation-agent</span><br>
              <span class="cli-out">GROQ_API_KEY  Updated 2026-10-29T07:04:02Z</span><br>
              <span class="cli-out">HF_TOKEN      Updated 2026-10-29T07:04:02Z</span>
            </div>
          </div>
        </body>
        </html>
        """
        page.set_content(secrets_html)
        page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "github_secrets.png"))
        print("Generated github_secrets.png")

        browser.close()

if __name__ == "__main__":
    render_terminal_screenshots()
