import re

# Common prefixes and suffixes to remove
PREFIXES = ["mr", "ms", "mrs", "dr", "prof"]
SUFFIXES = ["phd", "md", "dvm", "msc", "btech"]

def normalize_name(name: str) -> str:
    name = name.strip()
    name_lower = name.lower()

    # Remove prefix (e.g., Dr. John → John)
    for prefix in PREFIXES:
        pattern = rf"^{prefix}\.?\s+"
        name_lower = re.sub(pattern, "", name_lower)

    # Remove suffix (e.g., John Smith DVM → John Smith)
    for suffix in SUFFIXES:
        pattern = rf"\s+{suffix}\.?"
        name_lower = re.sub(pattern, "", name_lower)

    # Cleanup spacing and title-case
    return re.sub(r"\s+", " ", name_lower).title()
