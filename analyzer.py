import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def analyze_resume(data):
    skill_text = " ".join(data.get("skills", []))
    doc = nlp(skill_text)
    categories = defaultdict(list)

    # Define mappings
    programming = {"Python", "Java", "Elixir", "SQL"}
    devops = {"Docker", "Kubernetes"}
    tools = {"Git", "VS Code", "PyCharm", "IntelliJ"}

    for token in doc:
        skill = token.text.strip()
        if skill in programming:
            categories["Programming Languages"].append(skill)
        elif skill in devops:
            categories["DevOps"].append(skill)
        elif skill in tools:
            categories["Tools"].append(skill)

    return {
        "skill_categories": categories,
        "total_experience": f"{data.get('experience_count', 0)} years",
        "domain_focus": f"{data.get('domain_focus', 'N/A')}"
    }
