from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import re
import unicodedata

load_dotenv()  # This loads .env variables into os.environ

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Check your .env file.")

def sanitize_json_text(raw_text: str) -> str:
    # Normalize all Unicode to NFC (compose accents properly)
    cleaned = unicodedata.normalize("NFKC", raw_text)

    # Optional: Replace EN dash and EM dash with regular dash
    cleaned = cleaned.replace("—", "-").replace("–", "-")

    # Optional: Replace weird quotes if they exist
    cleaned = cleaned.replace("“", '"').replace("”", '"')

    # Optional: Replace tildes with dash (used for durations)
    cleaned = cleaned.replace("~", "-")
    cleaned = cleaned.replace("```", "")
    cleaned = cleaned.replace("json", "")

    return cleaned

def generate_llm_summary(sanitized_text):
    prompt = f"""
    Based on the following resume content, generate a concise 2-3 line professional summary.

    Resume (PII removed):
    {sanitized_text}  # Limit input to prevent token overflow

    The summary should focus on key roles, skills, and accomplishments.
    """

    try:
        openai = OpenAI(api_key=api_key)

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5  # some creativity
        )
        output = response.choices[0].message.content.strip()
        output = sanitize_json_text(output)
        print(f"LLM Summary: {output}")
        return output
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return "Summary not available"
