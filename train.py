import spacy
from spacy.training.example import Example
from prepare_data import TRAIN_DATA

nlp = spacy.blank("en")

ner = nlp.add_pipe("ner")

labels = [
    "SYMPTOM",
    "DISEASE",
    "DRUG",
    "DOSAGE",
    "FREQUENCY",
    "DURATION"
]

for label in labels:
    ner.add_label(label)

optimizer = nlp.begin_training()

for epoch in range(30):
    losses = {}
    for text, annotations in TRAIN_DATA:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], sgd=optimizer, losses=losses)
    
    print(f"Epoch {epoch} Loss:", losses)

nlp.to_disk("model")
print("Model saved!")