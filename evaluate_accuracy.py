# 📁 evaluate_accuracy.py

import os
import json
from difflib import SequenceMatcher
from collections import defaultdict
from model.ocr import image_to_text
from model.regex_extractor import extract_fields
from model.ner_extractor import extract_entities
from model.fallback_extractor import fallback_extract
from sklearn.metrics import classification_report
import re

FIELDS = ["name", "college", "roll_number", "branch", "valid_upto"]

def clean_text(text):
    return text.replace("\n", " ").replace("  ", " ")

def normalize_value(val):
    return val.strip().lower().replace(" ", "").replace("-", "")

def normalize(pred):
    pred = pred.strip().lower()
    pred = pred.replace("name:", "").replace("branch:", "")
    pred = re.sub(r"\s+", " ", pred)
    return pred.title().strip()

def is_similar(a, b, threshold=0.9):
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio() >= threshold

# 📁 NEW: merged label structure
with open("dataset/merge_labels.json") as f:
    merged_data = json.load(f)["results"]

images_dir = "dataset/images"

# Overall counters
total_fields = 0
correct_fields = 0

# For field-wise accuracy
field_true = defaultdict(list)
field_pred = defaultdict(list)

print("\n🔎 Field mismatches:\n")

for item in merged_data:
    user_id = item["user_id"]
    ground_truth = item["original_fields"]
    image_path = os.path.join(images_dir, f"{user_id}.png")

    text = image_to_text(image_path)
    cleaned_text = clean_text(text)

    # Run full pipeline
    regex_output = extract_fields(text)["extracted_fields"]
    ner_output = extract_entities(cleaned_text)
    fallback_output = fallback_extract(cleaned_text)

    # Merge outputs: regex → ner → fallback
    final_output = regex_output.copy()
    final_output.update({k: v for k, v in ner_output.items() if v})
    for k, v in fallback_output.items():
        if not final_output.get(k):
            final_output[k] = v

    for field in FIELDS:
        if not final_output.get(field):
            final_output[field] = "Unknown"

        total_fields += 1
        gt = ground_truth.get(field, "").strip()
        pred = final_output.get(field, "").strip()

        field_true[field].append(gt)
        field_pred[field].append(pred)

        if normalize(gt) == normalize(pred) or is_similar(gt, pred) or normalize_value(gt) == normalize_value(pred):
            correct_fields += 1
        else:
            print(f"❌ {field.upper()} mismatch for {user_id}")
            print(f"   GT: {gt}")
            print(f"   PR: {pred}\n")

# Overall accuracy
accuracy = correct_fields / total_fields
print(f"\n✅ Total Fields: {total_fields}")
print(f"✅ Correct Fields: {correct_fields}")
print(f"🎯 Field-Level Accuracy: {accuracy * 100:.2f}%")

# Detailed field-wise report
print("\n📊 Field-wise Precision / Recall / F1:\n")
for field in FIELDS:
    print(f"📌 {field.upper()}")
    print(classification_report(field_true[field], field_pred[field], zero_division=0))
