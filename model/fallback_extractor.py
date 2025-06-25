COLLEGE_KEYWORDS = [
    "osmania university", "jntu kakinada", "anna university", "nit trichy", "iit bombay",
    "sr university", "rgm college", "rgmcet", "iiit hyderabad", "iit madras", "jntu hyderabad"
]

BRANCH_KEYWORDS = [
    "mechanical engineering", "electronics and communication", "computer science", "civil engineering",
    "electrical engineering", "cse", "cse ai", "cse ai&ml", "cse ai&ds", "cse ml", "cse data science",
    "ece", "eee", "it", "eie", "cse iot", "csd", "csbs", "csai", "csd", "cseds", "cse (ai&ml)", "cse (ds)",
    "Civil Engineering",
    "Computer Science and Engineering",
    "Mechanical Engineering",
    "Electrical Engineering",
    "Electronics and Communication Engineering",
    "Information Technology"
]

import re
def fallback_extract(text: str) -> dict:
    text = text.lower()
    result = {}

    # College fallback
    for college in COLLEGE_KEYWORDS:
        if college in text:
            result["college"] = college.title()
            break

    # Branch fallback
    for branch in BRANCH_KEYWORDS:
        if branch in text:
            result["branch"] = branch.title()
            break

    # Roll number fallback (e.g., 22JNT5377)
    match = re.search(r"\b\d{2}[A-Z]{2,}[0-9]{2,}\b", text)
    if match:
        result["roll_number"] = match.group().upper()

    # Valid year fallback (like 2025, 2026...)
    year_match = re.search(r"\b(20\d{2})\b", text)
    if year_match:
        result["valid_upto"] = year_match.group()

    return result