from openai import OpenAI
import os
import unicodedata
import re
import json
from file_handler import extract_text_from_file
from pii_sanitizer import sanitize_text
from dotenv import load_dotenv

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

def extract_resume_data(sanitized_text: str) -> dict:
    # Step 1: Extract raw resume text
    safe_text = sanitized_text
    # Step 2: Your strict JSON-only parsing prompt
    prompt = f"""
            You are an expert resume parser.
    
    Given the content of a resume (in plain text), extract the following details in structured JSON format with the keys below:
    
    {{
        "name": "<Full name of the person>",
        "email": "<Primary email address or empty string if not present>",
        "phone": "<Phone number with country code if available or empty string if not present>",
        "location": "<Current city and country or state, if mentioned or empty string>",
        "skills": ["<List of relevant technical and non-technical skills, or empty list if none>"],
        "experience_count": "<Total number of work experiences with valid duration (start year - end year or Present)>",
        "domain_focus": "<Primary domain or field of expertise inferred from experience, e.g., 'Software Development', 'Data Science', 'Marketing'>",
        "experience": [
            {{
                "company": "<Company name>",
                "role": "<Job title or position>",
                "duration": "<Start year - End year or Present>"
            }}
        ],
        "education": [
            {{
                "degree": "<Degree or qualification>",
                "university": "<Name of university or institution>",
                "year": "<Year of graduation or completion>"
            }}
        ]
    }}
    
    Strict Rules:
    1. Return **JSON only**. No explanation, notes, or extra text.
    2. Do not hallucinate missing values. If a field is missing, use empty string (`""`) for single values or empty array (`[]`) for lists.
    3. Phone, email, and LinkedIn should be parsed only if explicitly mentioned in the resume.
    4. If multiple experiences or education entries exist, include all in array format.
    5. The `experience_count` field must reflect only experiences with a valid duration (ignore entries without start/end dates or "Present").
    6. The `domain_focus` field should be inferred from the roles, companies, and skills mentioned in the experience section.
    7. **Sanitize the output**:
       - Replace null values with `""`
       - Replace en-dashes `—` or tildes `~` in durations with standard hyphen `-`
       - Replace fancy quotes `“` and `”` with standard `"`
       - Ensure the JSON is strictly parseable by Python's `json.loads`
    
    Resume Content:
    \"\"\"
    {safe_text}
    \"\"\"
            """
    
    try:
        # Step 4: Call OpenAI GPT-4
        openai = OpenAI(api_key=api_key)

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0  # deterministic output
        )

        output = response.choices[0].message.content.strip()
        output = sanitize_json_text(output)
        # Step 5: Safely convert string to JSON
        return json.loads(output)

    except json.JSONDecodeError:
        print("❌ Failed to parse JSON. Raw output:")
        print(output)
        return {}

    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return {}
