import spacy
from spacy.language import Language
from typing import Dict, Any, List
import uuid

@Language.component("add_doc_id")
def add_doc_id(doc):  # type: ignore[valid-type]
    doc._.id = str(uuid.uuid4())
    return doc


def build_pipeline(model_name: str | None = None) -> Language:
    """Return a ready‑to‑use spaCy NLP object with domain extensions."""
    model_name = model_name or "en_core_web_trf"
    nlp = spacy.load(model_name)
    if "add_doc_id" not in nlp.pipe_names:
        nlp.add_pipe("add_doc_id", first=True)
    return nlp


def extract_entities(text: str, nlp: Language | None = None) -> Dict[str, Any]:
    nlp = nlp or build_pipeline()
    doc = nlp(text)
    ents: List[Dict[str, Any]] = []
    for i, ent in enumerate(doc.ents):
        ents.append({
            "uid": f"{doc._.id}-{i}",
            "type": ent.label_,
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "confidence": float(ent._.confidence or 1.0)  # spaCy transformer scorer
        })
    return {"id": doc._.id, "text": text, "entities": ents}