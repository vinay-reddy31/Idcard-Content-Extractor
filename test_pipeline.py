from model.ocr import image_to_text
from model.regex_extractor import extract_fields
from model.ner_extractor import extract_entities
from model.fallback_extractor import fallback_extract  # <- you must have created this
from model.branch_normalizer import normalize_branch
from model.roll_number_normalizer import normalize_roll_number
from model.name_normalizer import normalize_name
from model.college_normalizer import normalize_college
import json

# Step 1: Read image
img_path = "test_dataset/images/id_001.png" 
text = image_to_text(img_path)
print("📝 OCR Output:", text)

# Step 2: Regex extraction
regex_output = extract_fields(text)
final_output = regex_output["extracted_fields"]

# Step 3: Data Cleaning and NER Extraction
cleaned_text = text.replace("\n", " ").replace("  ", " ")
print("cleaned_txt:", cleaned_text)

ner_output = extract_entities(cleaned_text)
print("\n🧠 NER Output:")

print(json.dumps(ner_output, indent=2))

# Step 4: Update final output with NER results only if they exist
for key, value in ner_output.items():
    if value:  
        final_output[key] = value

# Step 5: Fallback extraction
fallback_output = fallback_extract(cleaned_text)

# ✅ ONLY update from fallback if key is still null or empty
for key, value in fallback_output.items():
    if not final_output.get(key):  # if None, "", or not present
        final_output[key] = value

# Step 6: Normalize & complete missing fields
FIELDS = ["name", "college", "branch", "roll_number", "valid_upto"]

for field in FIELDS:
    value = final_output.get(field)

    # If value is None or empty string, treat as "Unknown"
    value = value.strip() if value else "Unknown"

    # Normalize specific fields
    if field == "branch":
        final_output[field] = normalize_branch(value)  if value != "Unknown" else "Unknown"

    elif field == "roll_number":
        final_output[field] = normalize_roll_number(value) if value != "Unknown" else "Unknown"

    elif field == "name":
        final_output[field] = normalize_name(value) if value != "Unknown" else "Unknown"

    elif field == "college":
        final_output[field] = normalize_college(value) if value != "Unknown" else "Unknown"

    else:
        final_output[field] = value

# ✅ Final Output
print("\n✅ Final Extracted Fields:")
print(json.dumps(final_output, indent=2))
