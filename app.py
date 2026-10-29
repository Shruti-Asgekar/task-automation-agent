import os
import sys
import time
import logging
from typing import Optional
import streamlit as st
from groq import Groq

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("task_automation_agent")

def generate_brief(topic: str, client: Optional[Groq] = None) -> str:
    """
    Generate a 3-bullet research brief using Groq.
    Attempts 'groq/compound-mini' first (built-in search),
    falls back to 'llama-3.1-8b-instant' (knowledge-based),
    and if needed to available Groq models (e.g. 'openai/gpt-oss-20b').
    """
    if not topic or not topic.strip():
        logger.warning("Empty topic received.")
        return "Error: Topic cannot be empty. Please enter a valid topic."

    cleaned_topic = topic.strip()
    logger.info("Topic received: %s", cleaned_topic)
    start_time = time.perf_counter()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key and client is None:
        logger.error("GROQ_API_KEY environment variable is not set.")
        return "Error: GROQ_API_KEY is not configured in the environment."

    if client is None:
        client = Groq(api_key=api_key)

    primary_model = "groq/compound-mini"
    primary_prompt = f"Conduct focused research on this topic using web search and reply with exactly 3 high-impact, concise bullet points:\n\nTopic: {cleaned_topic}"

    fallback_model = "llama-3.1-8b-instant"
    fallback_prompt = f"Note: Answering from internal knowledge. Conduct focused research on this topic and reply with exactly 3 high-impact, concise bullet points:\n\nTopic: {cleaned_topic}"

    emergency_model = "openai/gpt-oss-20b"

    # Attempt primary model
    try:
        response = client.chat.completions.create(
            model=primary_model,
            messages=[
                {"role": "system", "content": "You are an elite research assistant. Always reply with exactly 3 concise bullet points starting with '-' or '*'."},
                {"role": "user", "content": primary_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        content = response.choices[0].message.content.strip()
        elapsed = time.perf_counter() - start_time
        logger.info("Request completed using %s in %.2f seconds.", primary_model, elapsed)
        return content
    except Exception as e_primary:
        logger.warning("Primary model %s failed: %s. Attempting fallback %s.", primary_model, str(e_primary), fallback_model)

    # Attempt fallback model
    try:
        response = client.chat.completions.create(
            model=fallback_model,
            messages=[
                {"role": "system", "content": "You are an elite research assistant answering from your own knowledge. Always reply with exactly 3 concise bullet points starting with '-' or '*'."},
                {"role": "user", "content": fallback_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        content = response.choices[0].message.content.strip()
        elapsed = time.perf_counter() - start_time
        logger.info("Request completed using %s in %.2f seconds.", fallback_model, elapsed)
        return content
    except Exception as e_fallback:
        logger.warning("Fallback model %s failed: %s. Attempting emergency model %s.", fallback_model, str(e_fallback), emergency_model)

    # Attempt emergency model
    try:
        response = client.chat.completions.create(
            model=emergency_model,
            messages=[
                {"role": "system", "content": "You are an elite research assistant answering from your own knowledge. Always reply with exactly 3 concise bullet points starting with '-' or '*'."},
                {"role": "user", "content": fallback_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        content = response.choices[0].message.content.strip()
        elapsed = time.perf_counter() - start_time
        logger.info("Request completed using %s in %.2f seconds.", emergency_model, elapsed)
        return content
    except Exception as e_emergency:
        elapsed = time.perf_counter() - start_time
        logger.error("All models failed after %.2f seconds. Error: %s", elapsed, str(e_emergency))
        return f"Error generating brief: {str(e_emergency)}"

def main():
    st.set_page_config(page_title="Task-Automation Agent v2.0", page_icon="⚡")
    st.title("⚡ Task-Automation Agent: Fast Research Brief Generator (v2.0)")
    st.write("Enter any topic below to receive an automated 3-bullet high-impact research brief.")

    topic_input = st.text_input("Enter a topic for research:", placeholder="e.g. MLOps Best Practices 2026")

    if st.button("Generate Brief", type="primary"):
        if not topic_input or not topic_input.strip():
            st.warning("Please enter a valid topic before submitting.")
        else:
            with st.spinner("Generating 3-bullet research brief..."):
                brief = generate_brief(topic_input)
                if brief.startswith("Error"):
                    st.error(brief)
                else:
                    st.subheader("Research Brief (v2.0)")
                    st.markdown(brief)

if __name__ == "__main__":
    main()
