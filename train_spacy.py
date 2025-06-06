import spacy
from spacy.training import Example
from utils.generate_training_data import get_training_data
import random

def train_ner_model(output_dir="ner_model"):
    training_data = get_training_data()

    nlp = spacy.blank("en")  # Empty English pipeline
    ner = nlp.add_pipe("ner")

    # Add custom labels
    for _, annotations in training_data:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])

    # Disable other pipes (if any)
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for epoch in range(15):
            random.shuffle(training_data)  
            for text, annotations in training_data:
                example = Example.from_dict(nlp.make_doc(text), annotations)
                nlp.update([example], sgd=optimizer, drop=0.2)

    # Save model
    nlp.to_disk(output_dir)
    print(f"✅ Model trained and saved to {output_dir}/")

if __name__ == "__main__":
    train_ner_model()