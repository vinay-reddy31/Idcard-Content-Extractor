from model.ocr import image_to_text
from model.regex_extractor import extract_fields
from model.ner_extractor import extract_entities
from model.fallback_extractor import fallback_extract  # <- you must have created this
import json

# Step 1: Read image
img_path = "dataset/images/stu_044.png"  # 👈 change as needed
text = image_to_text(img_path)

print("📝 OCR Output:", text)

# Step 2: Regex extraction
regex_output = extract_fields(text)
final_output = regex_output["extracted_fields"]

# Step 3: NER
cleaned_text = text.replace("\n", " ").replace("  ", " ")
ner_output = extract_entities(cleaned_text)

print("\n🧠 NER Output:")
print(json.dumps(ner_output, indent=2))

# Step 4: Update final output with NER results only if they exist
for key, value in ner_output.items():
    if value:  # not None or empty
        final_output[key] = value

# Step 5: Fallback extraction
fallback_output = fallback_extract(cleaned_text)

# ✅ ONLY update from fallback if key is still null or empty
for key, value in fallback_output.items():
    if not final_output.get(key):  # if None, "", or not present
        final_output[key] = value

# Step 6: Fill anything missing as "Unknown" (to make JSON complete)
for field in ["name", "college", "branch", "roll_number", "valid_upto"]:
    if not final_output.get(field):
        final_output[field] = "Unknown"

# Final Result
print("\n✅ Final Extracted Fields:")
print(json.dumps(final_output, indent=2))
