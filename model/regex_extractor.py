import re
import json

def extract_fields(text: str, config_path: str = "config.json") -> dict:
    with open(config_path, "r") as f:
        config = json.load(f)
        # print("🔍 Loaded config:", config)

    result = {}
    confidence = []

    for field, details in config["fields"].items():
        value = None
        for pattern in details.get("regex_patterns", []):
            match = re.search(pattern, text)
            print(f"🔍 Searching for pattern: {pattern} in text: {text}")
            if match:
                value = match.group(0)
                break
        result[field] = value
        if value:
            confidence.append(details["confidence_weight"])

    confidence_score = round(sum(confidence) / len(config["fields"]), 2)
    print(f"🔍 Confidence score: {confidence_score}")
    missing_fields = [f for f, v in result.items() if not v]
    if missing_fields:
        print(f"🔍 Missing fields: {missing_fields}")

    return {
        "extracted_fields": result,
        "confidence_score": confidence_score,
        "missing_fields": missing_fields,
        "status": "success" if not missing_fields else "partial_success"
    }
    