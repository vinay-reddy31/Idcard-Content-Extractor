# ✅ utils/generate_training_data.py

import os
import json

def get_training_data(images_dir="dataset/images", labels_dir="dataset/labels"):
    training_data = []
    fields = ["name", "college", "branch", "roll_number", "valid_upto"]

    label_map = {
        "name": "Name",
        "college": "College",
        "branch": "Branch",
        "roll_number": "Hno",
        "valid_upto": "Valid upto"
    }

    for filename in os.listdir(labels_dir):
        if filename.endswith(".json"):
            label_path = os.path.join(labels_dir, filename)
            with open(label_path, "r") as f:
                data = json.load(f)

            text_lines = []
            entities = []

            full_text = ""
            for field in fields:
                label = label_map[field]
                value = data["extracted_fields"].get(field, "")
                line = f"{label}: {value}"
                start = len(full_text) + line.find(value)
                end = start + len(value)
                entities.append((start, end, field.upper()))
                text_lines.append(line)
                full_text += line + "\n"

            full_text = full_text.strip()
            training_data.append((full_text, {"entities": entities}))

    return training_data
