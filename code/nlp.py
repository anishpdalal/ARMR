from pathlib import Path
import random
import spacy
from spacy.util import minibatch, compounding


def load_model(model_dir):
    return spacy.load(model_dir)


def parse_entities(model, text):
    entities = []
    for entity in model(text).ents:
        entities.append((entity, entity.label_))
    return entities


def train(model, train_data, output_dir, n_iter=100):
    other_pipes = [pipe for pipe in model.pipe_names if pipe != "ner"]
    with model.disable_pipes(*other_pipes):
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                model.update(
                    texts,
                    annotations,
                    drop=0.5,
                    losses=losses,
                )
            print("Losses", losses)

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        model.to_disk(output_dir)
        print("Saved model to ", output_dir)
