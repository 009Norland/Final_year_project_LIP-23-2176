"""src/document_intelligence/classifier.py"""
import re
import joblib
try:
    import spacy
    _SPACY_AVAILABLE = True
except ImportError:
    _SPACY_AVAILABLE = False

from src.utils.logger import get_logger
from config.settings import DOC_MODEL_PATH, MODELS_DIR

logger = get_logger(__name__)
MODEL_DIR = MODELS_DIR / "document_intelligence"
_pipeline = None
_nlp      = None


def _load_model():
    global _pipeline
    if _pipeline is None:
        _pipeline = joblib.load(DOC_MODEL_PATH)
        logger.info("Document model loaded")
    return _pipeline


def _load_nlp():
    global _nlp
    if _nlp is None and _SPACY_AVAILABLE:
        try:
            _nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded")
        except Exception:
            logger.warning("spaCy en_core_web_sm not available — NER will use regex only.")
            _nlp = False
    return _nlp if _nlp else None


# ── Regex patterns ────────────────────────────────────────────────────────────
_PATTERNS = {
    "pin":         r"\b[A-Z]\d{9,11}[A-Z]\b",
    "amounts":     r"KES\s?[\d,]+(?:\.\d{2})?",
    "case_number": r"\b(?:HC|TAT|KRA|OBJ)[\/\-][\w\/\-]+\b",
    "dates":       r"\b\d{4}\-\d{2}\-\d{2}\b|\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b",
    "reference":   r"(?:reference|ref)[:\s]+[\w\/\-]+",
}


def extract_entities(text: str) -> dict:
    entities = {"pin": None, "amounts": [], "case_number": None,
                "dates": [], "reference": None, "organisations": [], "persons": []}

    for key, pattern in _PATTERNS.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            if key in ("amounts", "dates"):
                entities[key] = list(dict.fromkeys(matches))
            else:
                entities[key] = matches[0]

    nlp = _load_nlp()
    if nlp:
        doc = nlp(text[:2000])
        entities["organisations"] = list(dict.fromkeys(e.text for e in doc.ents if e.label_ == "ORG"))[:5]
        entities["persons"]       = list(dict.fromkeys(e.text for e in doc.ents if e.label_ == "PERSON"))[:5]

    return entities


def classify_document(text: str) -> dict:
    pipeline = _load_model()
    proba_arr = pipeline.predict_proba([text])[0]
    classes   = pipeline.classes_
    pred_idx  = proba_arr.argmax()
    doc_type  = classes[pred_idx]
    confidence= round(float(proba_arr[pred_idx]) * 100, 1)
    entities  = extract_entities(text)

    parts = [f"Document Type: {doc_type}."]
    if entities.get("pin"):        parts.append(f"PIN: {entities['pin']}.")
    if entities.get("amounts"):    parts.append(f"Amount(s): {', '.join(entities['amounts'][:2])}.")
    if entities.get("case_number"):parts.append(f"Case No: {entities['case_number']}.")
    if entities.get("dates"):      parts.append(f"Date(s): {', '.join(entities['dates'][:2])}.")
    summary = " ".join(parts)

    logger.info("Classified: '%s' (%.1f%%)", doc_type, confidence)
    return {
        "doc_type": doc_type, "confidence": confidence,
        "entities": entities, "summary": summary,
        "all_scores": {cls: round(float(p)*100, 2) for cls, p in zip(classes, proba_arr)},
    }
