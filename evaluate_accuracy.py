import os
import json
from model.ocr import image_to_text
from model.regex_extractor import extract_fields
from model.ner_extractor import extract_entities
from model.fallback_extractor import fallback_extract

# 💡 Text cleaner
def clean_text(text):
    return text.replace("\n", " ").replace("  ", " ")

# 🎯 Fields to evaluate
FIELDS = ["name", "college", "roll_number", "branch", "valid_upto"]

# ✅ Load all test cases
labels_dir = "dataset/labels"
images_dir = "dataset/images"

total_fields = 0
correct_fields = 0

for label_file in os.listdir(labels_dir):
    if not label_file.endswith(".json"):
        continue

    with open(os.path.join(labels_dir, label_file), "r") as f:
        ground_truth = json.load(f)["extracted_fields"]

    image_file = label_file.replace(".json", ".png")
    image_path = os.path.join(images_dir, image_file)

    # Step 1: OCR
    text = image_to_text(image_path)
    cleaned_text = clean_text(text)

    # Step 2: Run pipeline
    regex_output = extract_fields(text)["extracted_fields"]
    ner_output = extract_entities(cleaned_text)
    fallback_output = fallback_extract(cleaned_text)

    # Step 3: Merge
    final_output = regex_output.copy()
    final_output.update({k: v for k, v in ner_output.items() if v})
    for k, v in fallback_output.items():
        if not final_output.get(k):
            final_output[k] = v
    for field in FIELDS:
        if not final_output.get(field):
            final_output[field] = "Unknown"

    # Step 4: Compare with ground truth
    for field in FIELDS:
        total_fields += 1
        gt = ground_truth.get(field, "").strip().lower()
        pred = final_output.get(field, "").strip().lower()

        if gt == pred:
            correct_fields += 1
        else:
            print(f"❌ {field} mismatch in {label_file}")
            print(f"   GT: {gt}")
            print(f"   PR: {pred}\n")

# Step 5: Report
accuracy = correct_fields / total_fields
print(f"\n✅ Total Fields: {total_fields}")
print(f"✅ Correct Fields: {correct_fields}")
print(f"🎯 Field-Level Accuracy: {accuracy * 100:.2f}%")
