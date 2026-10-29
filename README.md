---
title: Task Automation Agent
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Task-Automation Agent: Research Brief Generator

An autonomous, minimal MLOps-deployed research assistant agent. Enter any research topic and receive an automated 3-bullet-point brief generated using the Groq API.

## Features
- **Streamlit UI**: Clean and minimal single-input interface.
- **Groq AI Integration**: Powered by `groq/compound-mini` with fallback to `llama-3.1-8b-instant`.
- **Dockerized**: Containerized deployment running as non-root user on port 7860.
- **CI/CD Automation**: GitHub Actions workflow running tests, building Docker images, and synchronizing to Hugging Face Spaces.
- **Production Observability**: Request timing and status logging.

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
