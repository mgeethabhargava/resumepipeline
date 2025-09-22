from file_handler import extract_text_from_file
from pii_sanitizer import extract_pii, sanitize_text
from extractor import extract_resume_data
from analyzer import analyze_resume
from llm_summary import generate_llm_summary
from utils import save_json
import time

if __name__ == "__main__":
    file_path = "resume_test2.pdf"  # Supports: .doc, .docx, .pdf, .jpg, .png

    # Step 1: Extract raw text from file
    raw_text = extract_text_from_file(file_path)

    # Step 2: Extract and mask PII
    pii = extract_pii(raw_text)
    sanitized_text = sanitize_text(raw_text)

    # Step 3: Manually parsed data (you can improve it later using LLM/NER)
    resume_data = extract_resume_data(sanitized_text)
    resume_data["pii"] = pii
    print(resume_data)
    save_json(resume_data, f"sample_resume_output_{int(time.time())}.json")

    # Step 4: AI/NLP Analysis
    insights = analyze_resume(resume_data)
    insights["professional_summary"] = generate_llm_summary(sanitized_text)
    save_json(insights, f"insights_{int(time.time())}.json")

    print("✅ Resume processed successfully!")
