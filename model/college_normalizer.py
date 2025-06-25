# 📦 model/college_normalizer.py

import re

# 🔁 Mapping of normalized forms
NORMALIZED_COLLEGES = {
    "anna university": "Anna University",
    "ann university": "Anna University",
    "anna annuniversity": "Anna University",
    "college: anna university": "Anna University",

    "bits pilani": "BITS Pilani",
    "college: bits pilani": "BITS Pilani",

    "iiit hyderabad": "IIIT Hyderabad",
    "iit bombay": "IIT Bombay",
    "iit hyderabad": "IIT Hyderabad",
    "jntu kakinada": "JNTU Kakinada",
    "jntu": "JNTU Kakinada",
    "jntu-kakinada": "JNTU Kakinada",
    "jntu university": "JNTU Kakinada",
    "jntu university kakinada": "JNTU Kakinada",

    "osmania university": "Osmania University",
    "osmania university": "Osmania University",

    "nit trichy": "NIT Trichy",
    "rect trichy": "NIT Trichy",

    "rgmcet nandyal": "RGMCET Nandyal",
    "college: rgmcet nandyal": "RGMCET Nandyal",

    "abc institute": "ABC Institute",
    "abcd institute": "ABC Institute",
    "ghi university": "GHI University",
    "pqr university": "PQR University",
    "uvw college": "UVW College",
}

def normalize_college(raw_value: str) -> str:
    if not raw_value:
        return "Unknown"

    # 🧹 Clean value: lower + remove extra spaces/punctuation
    value = raw_value.lower().strip()
    value = re.sub(r"[\s\-_:]+", " ", value)
    value = value.replace("college ", "").replace("university ", "").strip()

    # 🔁 Match from mapping
    for key in NORMALIZED_COLLEGES:
        if key in value:
            return NORMALIZED_COLLEGES[key]

    return raw_value.strip().title()
