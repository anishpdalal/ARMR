from pathlib import Path
import random
import spacy
from spacy.matcher import PhraseMatcher
from spacy.util import minibatch, compounding

TERMINOLOGY = [
        "history of present illness", "past medical and surgical history",
        "past medical history", "review of systems", "family history",
        "social history", "medications prior to admission",
        "allergies", "physical examination", "electrocardiogram", "impression",
        "recommendations"]


def load_model(model_dir):
    """Takes a file path to model weights and returns a SpaCy model"""
    return spacy.load(model_dir)


def prepare_note(model, text):
    """Output of spaCy text processing containing categories, text, diseases,
        and medications"""
    note_sections = categorize_note(model, text)
    for section in note_sections:
        diseases, medications = parse_entities(model, note_sections[section][
            'text'])
        note_sections[section]['diseases'] = diseases
        note_sections[section]['medications'] = medications
    return note_sections


def categorize_note(model, text):
    """Breakup notes into different sections"""
    categories = {}
    matcher = PhraseMatcher(model.vocab)
    patterns = [model.make_doc(text) for text in TERMINOLOGY]
    matcher.add("Categories", None, *patterns)
    doc_lower = model(text.lower())
    doc = model(text)
    matches = matcher(doc_lower)
    results = []
    for match_id, start, end in matches:
        span = doc_lower[start:end]
        results.append((span, start, end))
    results = sorted(results, key=lambda tup: tup[1])
    for i in range(len(results)):
        result = results[i]
        next_result = results[i+1] if i < len(results)-1 else None
        category = str(result[0])
        start = result[2] if i != 0 else result[2]
        end = next_result[1] if next_result else None
        if end:
            categories[category] = {'text': doc[start:end].text}
        else:
            categories[category] = {'text': doc[start:].text}
    return categories


def parse_entities(model, text):
    """model identifies clinical text from transcribed text"""
    diseases = []
    medications = []
    for entity in model(text).ents:
        if entity.label_ == 'DISEASE':
            diseases.append({'name': str(entity)})
        else:
            medications.append({'name': str(entity)})
    return diseases, medications


def train(model, train_data, output_dir, n_iter=100):
    """Named Entity Recognition Training loop"""
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
