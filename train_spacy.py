import spacy
from spacy.training import Example
from utils.generate_augmented_training_data import generate_training_data_from_merged
import random

def train_ner_model(output_dir="ner_model"):
    training_data = generate_training_data_from_merged()

    nlp = spacy.blank("en")  # Blank English pipeline
    ner = nlp.add_pipe("ner")

    for _, annotations in training_data:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for epoch in range(20):
            random.shuffle(training_data)
            losses = {}
            for text, annotations in training_data:
                example = Example.from_dict(nlp.make_doc(text), annotations)
                nlp.update([example], sgd=optimizer, losses=losses, drop=0.1)
            print(f"📚 Epoch {epoch+1} | Loss: {losses['ner']:.4f}")

    nlp.to_disk(output_dir)
    print(f"✅ Trained NER model saved to {output_dir}/")


if __name__ == "__main__":
    train_ner_model()