# test_pipeline.py

from model.ocr import image_to_text
from model.regex_extractor import extract_fields
from model.ner_extractor import extract_entities
from model.fallback_extractor import fallback_extract
import json

# Step 1: OCR the input image
img_path = "test_dataset/images/test_002.png"  # ✅ Change this per test
text = image_to_text(img_path)

print("📝 OCR Output:", text)

# Step 2: Run Regex Extraction
regex_output = extract_fields(text)
final_output = regex_output["extracted_fields"]

# Step 3: Clean OCR text & run NER
cleaned_text = text.replace("\n", " ").replace("  ", " ")
print("cleaned_txt:", cleaned_text)

ner_output = extract_entities(cleaned_text)
print("\n🧠 NER Output:")
print(json.dumps(ner_output, indent=2))

# Step 4: Override fields with NER values if they exist
for key, value in ner_output.items():
    if value:
        final_output[key] = value

# Step 5: Fallback — only use if the field is missing
fallback_output = fallback_extract(cleaned_text)
for key, value in fallback_output.items():
    if not final_output.get(key):
        final_output[key] = value

# Step 6: Ensure all required fields are present
for field in ["name", "college", "branch", "roll_number", "valid_upto"]:
    if not final_output.get(field):
        final_output[field] = "Unknown"

# Final Output
print("\n✅ Final Extracted Fields:")
print(json.dumps(final_output, indent=2))
