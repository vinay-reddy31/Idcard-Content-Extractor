# import re
# from difflib import get_close_matches

# # 🔧 Common field value lists for fuzzy matching
# KNOWN_COLLEGES = [
#     "Osmania University", "Anna University", "BITS Pilani", "IIT Bombay", 
#     "IIT Hyderabad", "RGMCET Nandyal", "NIT Trichy", "ABC Institute"
# ]

# KNOWN_BRANCHES = [
#     "Computer Science", "Mechanical Engineering", "Civil Engineering",
#     "Electrical Engineering", "Electronics and Communication",
#     "Information Technology", "Informatical Engineering"
# ]

# def fuzzy_match(word, choices, cutoff=0.7):
#     matches = get_close_matches(word, choices, n=1, cutoff=cutoff)
#     return matches[0] if matches else word

# def correct_field(field, value):
#     if not value or value.lower() == "unknown":
#         return value
    
#     value = re.sub(r"[^a-zA-Z0-9\s]", "", value)  # remove noise
#     value = value.strip()

#     if field == "college":
#         return fuzzy_match(value, KNOWN_COLLEGES)
#     elif field == "branch":
#         return fuzzy_match(value, KNOWN_BRANCHES)
#     elif field == "valid_upto":
#         match = re.search(r"\b(20\d{2})\b", value)
#         return match.group(1) if match else value
#     elif field == "roll_number":
#         return re.sub(r"[^\w\d]", "", value.upper())
#     elif field == "name":
#         return value.title()

#     return value
