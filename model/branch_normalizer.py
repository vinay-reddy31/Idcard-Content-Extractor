# 📁 model/branch_normalizer.py

import re

BRANCH_ALIASES = {
    "cse": "Computer Science Engineering",
    "computer science": "Computer Science Engineering",
    "computer science engineering": "Computer Science Engineering",
    "computer science and engineering": "Computer Science Engineering",
    "computer scienceengineering": "Computer Science Engineering",
    "computer science valid": "Computer Science Engineering",
    "cs": "Computer Science Engineering",
    "ece": "Electronics and Communication Engineering",
    "electronics and communication": "Electronics and Communication Engineering",
    "electronics and communication engineering": "Electronics and Communication Engineering",
    "electronics and communication valid": "Electronics and Communication Engineering",
    "eee": "Electrical Engineering",
    "electrical engineering": "Electrical Engineering",
    "me": "Mechanical Engineering",
    "mechanical engineering": "Mechanical Engineering",
    "civil engineering": "Civil Engineering",
    "civil": "Civil Engineering",
    "it": "Information Technology",
    "information technology": "Information Technology",
    "information engineering": "Information Technology",
    "informatics": "Information Technology"
}

def normalize_branch(text: str) -> str:
    if not text:
        return "Unknown"
    
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower()).strip()
    text = re.sub(r"\s+", " ", text)  # Normalize extra spaces

    for alias, canonical in BRANCH_ALIASES.items():
        if alias in text:
            return canonical

    return text.title()
