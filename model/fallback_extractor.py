COLLEGE_KEYWORDS = [
    "osmania university",
    "jntu kakinada",
    "anna university",
    "nit trichy",
    "iit bombay"
]

BRANCH_KEYWORDS = [
    "mechanical engineering",
    "electronics and communication",
    "computer science",
    "electrical engineering",
    "civil engineering"
]

def fallback_extract(text: str) -> dict:
    text = text.lower()
    result = {}

    for college in COLLEGE_KEYWORDS:
        if college in text:
            result["college"] = college.title()
            break

    for branch in BRANCH_KEYWORDS:
        if branch in text:
            result["branch"] = branch.title()
            break

    return result
