import spacy
import os

model_path = "ner_model"
if not os.path.exists(model_path):
    raise Exception("NER model not trained yet!")

nlp = spacy.load(model_path)

def extract_entities(text):
    doc = nlp(text)
    output = {}
    for ent in doc.ents:
        print("ent:",ent)
        output[ent.label_.lower()] = ent.text
    return output
