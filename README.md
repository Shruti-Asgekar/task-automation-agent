# Task-Automation Agent: Research Brief Generator

An autonomous, minimal MLOps-deployed research assistant agent. Enter any research topic and receive an automated 3-bullet-point brief generated using the Groq API.

## Features
- **Streamlit UI**: Clean and minimal single-input interface.
- **Groq AI Integration**: Powered by `groq/compound-mini` with fallback to `llama-3.1-8b-instant` and active Groq models (`openai/gpt-oss-20b`).
- **Dockerized**: Containerized deployment running as non-root user on port 7860.
- **CI Automation**: GitHub Actions workflow running tests and verifying Docker builds on every push and pull request.
- **Continuous Deployment**: Native Render auto-deployment via `render.yaml` blueprint on every push to `main`.
- **Production Observability**: Request timing and structured stdout logging.

## Local Development
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Groq API key:
   ```bash
   export GROQ_API_KEY="your-groq-key"
   ```
4. Run Streamlit:
   ```bash
   streamlit run app.py
   ```

## Running with Docker
```bash
docker build -t task-automation-agent .
docker run -p 7860:7860 -e GROQ_API_KEY="your-groq-key" task-automation-agent
```

## Cloud Deployment (Render)
This project is configured for automated cloud deployment on Render via `render.yaml`.
- **Runtime:** Docker
- **Plan:** Free
- **Auto-Deploy:** Enabled on branch `main`
- **Environment Secret:** `GROQ_API_KEY` (configured securely in Render dashboard)
