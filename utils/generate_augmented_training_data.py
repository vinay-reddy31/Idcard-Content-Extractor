# 📁 utils/generate_augmented_training_data.py

import os
import json
import random

# Templates without field prefixes (cleaner training spans)
def normalize_field(field):
    field_aliases = {
        "institution": "college",
        "university": "college",
        "fullname": "name",
        "hno": "roll_number",
        "id": "roll_number"
    }
    return field_aliases.get(field.lower(), field.lower())

field_templates = {
    "name": ["{}", "Name: {}", "Full Name: {}", "Student: {}", "Student name is {}"],
    "college": ["{}", "College: {}", "Institution: {}", "University: {}", "{} University"],
    "branch": ["{}", "Branch: {}", "Dept: {}", "Stream: {}", "Field of study: {}"],
    "roll_number": ["{}", "Hno: {}", "Roll Number: {}", "ID: {}", "Htno: {}", "Roll_no: {}"],
    "valid_upto": ["Valid upto: {}", "Valid Upto: {}", "Expires: {}", "valid_upto: {}"]
}

def augment_training_text(entry):
    variations = []
    for _ in range(3):  # Generate 3 variations
        text_lines = []
        entities = []
        full_text = ""

        keys = list(entry.keys())
        random.shuffle(keys)

        for raw_field in keys:
            std_field = normalize_field(raw_field)
            if std_field not in field_templates:
                continue

            value = entry[raw_field]
            template = random.choice(field_templates[std_field])
            line = template.format(value)

            start = len(full_text) + line.find(value)
            end = start + len(value)
            entities.append((start, end, std_field.upper()))

            text_lines.append(line)
            full_text += line + "\n"

        variations.append((full_text.strip(), {"entities": entities}))
    return variations


def generate_training_data_from_merged(path="dataset/merge_labels.json"):
    with open(path) as f:
        data = json.load(f)

    all_data = []
    for item in data["results"]:
        fields = item.get("original_fields", {})
        augmented = augment_training_text(fields)
        all_data.extend(augmented)
    return all_data