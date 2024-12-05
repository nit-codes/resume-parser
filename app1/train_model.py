import spacy
from spacy.training import Example
import random
import json
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def load_train_data_from_json(file_path):
    """Loads training data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        train_data = json.load(file)
    return train_data

def remove_overlapping_entities(entities):
    """Removes overlapping entities by keeping the longest entity."""
    # Sort entities by their start position (and by end position if start is the same)
    entities = sorted(entities, key=lambda ent: (ent[0], ent[1]))
    
    non_overlapping_entities = []
    prev_start, prev_end = -1, -1

    for start, end, label in entities:
        # If the current entity does not overlap with the previous one, add it
        if start >= prev_end:
            non_overlapping_entities.append((start, end, label))
            prev_start, prev_end = start, end
        else:
            # Handle overlap by keeping the longer entity
            if end - start > prev_end - prev_start:
                non_overlapping_entities[-1] = (start, end, label)
                prev_start, prev_end = start, end

    return non_overlapping_entities

def train_ner_model(train_data):
    # Load a pre-trained English model
    nlp = spacy.load("en_core_web_md")

    # Add the NER pipeline if not already present
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Add entity labels to the NER pipeline
    for entry in train_data:
        # Remove overlapping entities from each entry
        entry["entities"] = remove_overlapping_entities(entry["entities"])
        
        for ent in entry["entities"]:
            ner.add_label(ent[2])  # ent[2] is the label

    # Initialize the model's optimizer
    optimizer = nlp.resume_training()

    # Training loop
    for epoch in range(500):  # Number of training iterations
        random.shuffle(train_data)  # Shuffle the training data
        losses = {}
        for entry in train_data:
            text = entry["text"]
            annotations = {"entities": entry["entities"]}

            # Create an Example object
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            # Update the model with the example
            nlp.update([example], drop=0.2, losses=losses)
        print(f"Epoch {epoch + 1} - Losses: {losses}")

    # Save the trained model to disk
    nlp.to_disk("team_model")

if __name__ == "__main__":
    # Load training data from JSON file
    train_data = load_train_data_from_json('team.json')

    # Train the model with the loaded dataset
    train_ner_model(train_data)