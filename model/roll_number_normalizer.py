import re

# Common OCR errors in roll numbers
OCR_CORRECTIONS = {
    "o": "0",  # small o → zero
    "O": "0",  # capital O → zero
    "l": "1",  # lowercase l → one
    "I": "1",  # capital I → one
    "Z": "2",  # Z → 2
    "B": "8",  # B → 8
    "S": "5",  # S → 5 (optional, risky)
}

def correct_ocr_errors(text: str) -> str:
    corrected = ""
    for char in text:
        corrected += OCR_CORRECTIONS.get(char, char)
    return corrected

def normalize_roll_number(roll: str) -> str:
    roll = roll.strip().upper()
    roll = correct_ocr_errors(roll)
    roll = re.sub(r"[^A-Z0-9]", "", roll)  # Remove non-alphanumeric characters
    return roll
