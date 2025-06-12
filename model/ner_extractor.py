import spacy
import os
from collections import defaultdict

model_path = "ner_model"
if not os.path.exists(model_path):
    raise Exception("NER model not trained yet!")

nlp = spacy.load(model_path)

def extract_entities(text):
    doc = nlp(text)
    print("Ner output:")
    result = { "name": "", "college": "", "roll_number": "", "branch": "", "valid_upto": "" }
    for ent in doc.ents:
        label = ent.label_.lower()
        if label in result:
            result[label] = ent.text
    return result