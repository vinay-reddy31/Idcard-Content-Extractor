import os
import json
import re
from difflib import SequenceMatcher
from collections import defaultdict
from model.ocr import image_to_text
from model.regex_extractor import extract_fields
from model.ner_extractor import extract_entities
from model.fallback_extractor import fallback_extract
from sklearn.metrics import classification_report
from model.branch_normalizer import normalize_branch
from model.college_normalizer import normalize_college
from model.roll_number_normalizer import normalize_roll_number
from model.name_normalizer import normalize_name


# 🎯 Fields to evaluate
FIELDS = ["name", "college", "roll_number", "branch", "valid_upto"]

# 🔧 Utility Functions
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

# 📁 Dataset paths
labels_dir = "dataset/labels"
images_dir = "dataset/images"

# 🔢 Counters
total_fields = 0
correct_fields = 0
field_true = defaultdict(list)
field_pred = defaultdict(list)

print("\n🔎 Field mismatches:\n")

# 🚀 Loop through test dataset
for label_file in os.listdir(labels_dir):
    if not label_file.endswith(".json"):
        continue

    with open(os.path.join(labels_dir, label_file), "r") as f:
        ground_truth = json.load(f)["extracted_fields"]

    image_file = label_file.replace(".json", ".png")
    image_path = os.path.join(images_dir, image_file)

    # 📝 OCR
    text = image_to_text(image_path)
    cleaned_text = clean_text(text)

    # 🧠 Run full pipeline
    regex_output = extract_fields(text)["extracted_fields"]
    ner_output = extract_entities(cleaned_text)
    fallback_output = fallback_extract(cleaned_text)

    # 🔄 Merge results
    final_output = regex_output.copy()
    final_output.update({k: v for k, v in ner_output.items() if v})
    for k, v in fallback_output.items():
        if not final_output.get(k):
            final_output[k] = v

    for field in FIELDS:
        # Predicted value (default "Unknown" if None/empty)
        pred_value = (final_output.get(field) or "").strip()
        if not pred_value:
            pred_value = "Unknown"

        # Ground truth
        gt_value = (ground_truth.get(field) or "").strip()

        # 🔧 Normalize branch field
        if field == "branch":
            pred_value = normalize_branch(pred_value)
            gt_value = normalize_branch(gt_value)
        if field == "college":
            pred_value = normalize_college(pred_value)
            gt_value = normalize_college(gt_value)
            
        if field == "name":
            pred_value = normalize_name(pred_value)
            gt_value = normalize_name(gt_value)
        # 🔧 Normalize roll_number field
        if field == "roll_number":
            pred_value = normalize_roll_number(pred_value)
            gt_value = normalize_roll_number(gt_value)


        # Append to lists
        field_true[field].append(gt_value)
        field_pred[field].append(pred_value)

        # Match logic
        if normalize(gt_value) == normalize(pred_value) or is_similar(gt_value, pred_value) or normalize_value(gt_value) == normalize_value(pred_value):
            correct_fields += 1
        else:
            print(f"❌ {field.upper()} mismatch in {label_file}")
            print(f"   GT: {gt_value}")
            print(f"   PR: {pred_value}\n")

        total_fields += 1

# 📈 Accuracy Summary
accuracy = correct_fields / total_fields
print(f"\n✅ Total Fields: {total_fields}")
print(f"✅ Correct Fields: {correct_fields}")
print(f"🎯 Field-Level Accuracy: {accuracy * 100:.2f}%")

# 📊 Detailed Classification Report
print("\n📊 Field-wise Precision / Recall / F1:\n")
for field in FIELDS:
    print(f"📌 {field.upper()}")
    print(classification_report(field_true[field], field_pred[field], zero_division=0))
