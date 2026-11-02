import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Load local .env during development. Streamlit Cloud uses st.secrets.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_setting(name):
    """Read a setting from environment variables or Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st
        return st.secrets[name]
    except Exception:
        return None


# Read Gemini API key from local environment or Streamlit secrets.
api_key = get_setting("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not configured. Add it to your local .env "
        "or Streamlit Cloud Secrets."
    )

client = genai.Client(api_key=api_key)


def ask_gemini(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )
    return response.text
