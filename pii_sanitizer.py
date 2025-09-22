import re

def extract_pii(text):
    return {
        "email": re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text),
        "phone": re.findall(r"\+?\d{10,25}", text),
        "urls": re.findall(r"https?://[^\s]+|github\.com/\S+|linkedin\.com/in/\S+", text)
    }

def sanitize_text(text):
    text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL]", text)
    text = re.sub(r"\+?\d{10,25}", "[PHONE]", text)
    text = re.sub(r"https?://[^\s]+|github\.com/\S+|linkedin\.com/in/\S+", "[URL]", text)
    return text
