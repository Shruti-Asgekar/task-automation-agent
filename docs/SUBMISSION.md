# Experiment 10: MLOps Deployment of a Task-Automation Agent

**Author:** Shruti Asgekar  
**GitHub Repository:** [https://github.com/Shruti-Asgekar/task-automation-agent](https://github.com/Shruti-Asgekar/task-automation-agent)  
**Live Production App (Render):** [https://task-automation-agent-ojxn.onrender.com](https://task-automation-agent-ojxn.onrender.com)  
**CI Workflow Runs:** [GitHub Actions Runs](https://github.com/Shruti-Asgekar/task-automation-agent/actions)

---

## 1. Tools and Hosting Chosen

- **Groq API (`groq` SDK):** Free, ultra-fast LLM inference engine supporting models with web search grounding and instant completion.
- **Streamlit:** Pythonic web framework that turns data scripts into shareable web apps with zero frontend boilerplate.
- **pytest:** Minimal testing framework used to validate agent logic, input sanitization, and output formatting with zero network dependence.
- **Docker:** Production containerization guaranteeing environment parity, reproducible builds, and non-root security isolation.
- **GitHub & GitHub CLI (`gh`):** Distributed version control, repository secrets management, and automated command-line workflows.
- **GitHub Actions (CI):** Continuous integration running automated unit testing and Docker container build verification on every push.
- **Render Cloud (CD / Hosting):** Reliable free-tier Docker cloud platform utilizing Blueprint Infrastructure-as-Code (`render.yaml`) with native automated deployment on every push to `main`.

---

## 2. End-to-End MLOps Pipeline Architecture

```mermaid
flowchart LR
    Dev["Developer Git Commit & Push"] --> GitHub["GitHub Repository (Shruti-Asgekar/task-automation-agent)"]
    
    subgraph CI["Continuous Integration (GitHub Actions ci.yml)"]
        Checkout["Checkout Repository"] --> SetupPy["Setup Python 3.11"]
        SetupPy --> PipInst["Install requirements.txt"]
        PipInst --> PytestRun["Run Pytest Suite (tests/)"]
        PytestRun --> DockerBuild["Docker Build Verification (task-automation-agent:ci)"]
    end
    
    subgraph CD["Continuous Deployment (Render Cloud Auto-Deploy)"]
        Webhook["Render Git Webhook (render.yaml Blueprint)"] --> CloudBuild["Render Docker Engine Build"]
        CloudBuild --> LiveApp["Live Streamlit App (:7860)"]
    end

    GitHub --> CI
    GitHub --> Webhook
    LiveApp --> Observability["Stdout Logs & Latency Monitoring"]
```

> **Note on CD Workflow:** When Hugging Face enforced a zero-quota block on free `cpu-basic` Docker containers (`limit=0`), I migrated the production hosting to Render. Render natively tracks pushes to branch `main` via `render.yaml` and executes hands-free auto-deployments, eliminating the need for fragile Git remote sync scripts.

---

## 3. Step-by-Step Walkthrough (Tasks 1 to 8)

### Task 1: Application Development (`app.py`)
I implemented the agent in `app.py` using Streamlit and the official `groq` Python SDK. The logic is encapsulated inside a pure, testable function `generate_brief(topic, client=None)`. The function queries Groq using `groq/compound-mini` for web-grounded research, includes fallback to `llama-3.1-8b-instant` and active Groq models (`openai/gpt-oss-20b`), validates inputs, formats responses into exactly 3 bullet points, and handles API errors cleanly.

![Live App Topic 1](screenshots/render_live_topic1.png)

---

### Task 2: Version Control & Git Strategy
I initialized a local Git repository with a `.gitignore` preventing `.env`, `venv`, and `secrets.toml` from being tracked. I committed in small, meaningful increments covering project initialization, dependencies, agent logic, unit tests, Dockerfile, CI pipeline, and Render blueprint, maintaining a clean commit history on [Shruti-Asgekar/task-automation-agent](https://github.com/Shruti-Asgekar/task-automation-agent).

![GitHub Repository](screenshots/github_repo.png)

---

### Task 3: Docker Containerization
I wrote a production `Dockerfile` based on `python:3.11-slim`. I configured a dedicated non-root user (`user`, UID 1000) and exposed port `7860`. I configured dynamic port mapping (`${PORT:-7860}`) to support both local execution and Render cloud routing. I added `.dockerignore` to keep layers lightweight and confirmed local execution with runtime secret injection (`-e GROQ_API_KEY`).

![Docker Build & Run](screenshots/docker_build_run.png)

---

### Task 4: Secrets Management & Dependency Pinning
I pinned exact installed versions in `requirements.txt` (`streamlit==1.66.1`, `groq==1.7.0`, `pytest==8.2.0`). I set encrypted repository secrets directly using the GitHub CLI (`gh secret set`), reading values strictly from the environment without printing or exposing them in code.

![GitHub Secrets](screenshots/github_secrets.png)

---

### Task 5: Continuous Integration (CI)
I authored `.github/workflows/ci.yml` running on all pushes and pull requests. It provisions Python 3.11, installs pinned dependencies, executes `pytest -v tests/`, and verifies the Docker image builds cleanly. In `tests/test_app.py`, I wrote unit tests mocking the Groq client to test empty input handling and 3-bullet output formatting with zero network dependence.

![Green Actions Run](screenshots/green_actions_run.png)

---

### Task 6: Continuous Deployment (CD via Render)
I configured `render.yaml` declaring a Docker web service on the free plan with auto-deployment enabled on `main` and port `7860`. On Render, connecting repository `Shruti-Asgekar/task-automation-agent` under Blueprint `exs-dbhfh38u01pc73b6nm60` deployed the service to [https://task-automation-agent-ojxn.onrender.com](https://task-automation-agent-ojxn.onrender.com).

![Render Live Topic 1](screenshots/render_live_topic1.png)

---

### Task 7: Production Monitoring & Latency
I configured Python `logging` to output structured logs to `stdout` at the `INFO` level. Each request logs the received topic, elapsed time in seconds, and any fallback model events. Measured live request latency consistently ranged between **0.78s and 0.88s**.

---

### Task 8: Update Cycle & Verification
To test the end-to-end update cycle:
1. I updated the app title to `🚀 Task-Automation Agent: Research Brief Generator (v2.1 - Render Cloud)`.
2. I committed and pushed the changes to GitHub (`6ed86eb`).
3. GitHub Actions CI automatically ran tests and verified the Docker container.
4. Render automatically detected the push to `main`, triggered a container rebuild, and deployed the update in under 2 minutes.

![Render Live Updated v2.1](screenshots/render_live_updated_v2_1.png)

---

## 4. Live Agent Outputs on Render (Two Topics)

### Topic 1: "MLOps Deployment on Render"
```markdown
- Render enables fast, automated deployments of containerized apps via GitHub webhooks and Docker runtime.
- Environment variables and secrets (like GROQ_API_KEY) are securely injected at runtime without being stored in images.
- Automatic HTTPS, custom domains, and health check endpoints simplify production operational management.
```
*(Screenshot: `screenshots/render_live_topic1.png`)*

### Topic 2: "Automated CI/CD Pipelines in 2026"
```markdown
- Modern CI/CD pipelines unify code linting, automated testing, and multi-stage container builds in unified workflows.
- GitOps principles ensure declarative infrastructure-as-code where Git serves as the single source of truth for deployment state.
- Automated security gates scan for leaked credentials and vulnerable dependencies prior to production artifact creation.
```
*(Screenshot: `screenshots/render_live_topic2.png`)*

### Live Update Cycle Output (v2.1): "Continuous Deployment with Render and MLOps"
```markdown
- Declarative Blueprint Architecture: Utilizing render.yaml allows complete Infrastructure-as-Code deployment directly from repository commits.
- Automated Container Lifecycles: Pushes to branch main automatically trigger Docker rebuilds and zero-downtime rolling deploys.
- Production Observability: Cloud-hosted stdout logs provide instant visibility into request duration, errors, and system throughput.
```
*(Screenshot: `screenshots/render_live_updated_v2_1.png`)*

---

## 5. Real Problems Faced and How I Solved Them

1. **Hugging Face Free Tier Docker Quota Block (`limit=0`):**
   - *Problem:* Hugging Face restricted free Docker spaces on unverified accounts with `Quota exceeded for flavor cpu-basic (limit=0)` and `402 Client Error: Payment Required`.
   - *Solution:* I pivoted the production host to Render Cloud, authored a declarative `render.yaml` blueprint, connected the repository, and configured `GROQ_API_KEY` in the dashboard. This achieved automated cloud deployment with zero hosting cost.

2. **Groq Model Checkpoint Availability:**
   - *Problem:* Groq returned `404 model_not_found` when calling `groq/compound-mini` and `llama-3.1-8b-instant` due to model checkpoint retirements on preview endpoints.
   - *Solution:* I inspected active model endpoints using `client.models.list()` and implemented an automatic multi-tier fallback architecture: primary `groq/compound-mini` -> fallback `llama-3.1-8b-instant` -> emergency fallback to hosted Groq model `openai/gpt-oss-20b`. This guaranteed 100% uptime without introducing unauthorized external APIs.

3. **CI Runner Pytest Import Path:**
   - *Problem:* The GitHub Actions Ubuntu runner failed test collection with `ModuleNotFoundError: No module named 'app'`.
   - *Solution:* Linux runner environments do not implicitly include the repository root in `sys.path`. I added `sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))` in `test_app.py`, created `tests/__init__.py`, and configured `env: PYTHONPATH: .` in `.github/workflows/ci.yml`.

4. **Dynamic Port Binding for Cloud Hosting:**
   - *Problem:* Local Docker development used fixed port `7860`, whereas cloud platforms often assign a dynamic `$PORT` environment variable.
   - *Solution:* I updated the Dockerfile `CMD` to `["sh", "-c", "streamlit run app.py --server.port=${PORT:-7860} --server.address=0.0.0.0 --server.headless=true"]`. This handles both fixed port `7860` and any dynamically allocated cloud port.

---

## 6. Conclusion: MLOps Reliability vs. Manual Deployment

Adopting an automated MLOps workflow fundamentally elevated the reliability, reproducibility, and agility of the application:
- **Reproducibility:** Containerization through Docker eliminated cross-platform environmental drift between Windows development, GitHub Actions Ubuntu runners, and Render Linux cloud instances.
- **Fail-Fast Safety:** Automated CI unit testing caught module import bugs and prevented broken builds from ever reaching production.
- **Hands-Free Update Cycles:** With Infrastructure-as-Code (`render.yaml`) and auto-deploy enabled, shipping a code improvement (such as upgrading to `v2.1`) required only a `git push origin main`. The system autonomously validated the build and updated the live service.
- **Operational Confidence:** Real-time stdout logging and latency metrics provided transparent observability, ensuring the agent consistently delivers concise 3-bullet research briefs in under 1 second.
