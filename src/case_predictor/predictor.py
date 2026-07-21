"""src/case_predictor/predictor.py"""
import joblib
import numpy as np
import pandas as pd
from src.case_predictor.preprocessor import prepare_data
from src.utils.logger import get_logger
from config.settings import CASE_MODEL_PATH, SHAP_EXPLAINER_PATH, OUTCOME_LABELS

logger = get_logger(__name__)
_pipeline  = None
_explainer = None


def _load_model():
    global _pipeline
    if _pipeline is None:
        _pipeline = joblib.load(CASE_MODEL_PATH)
        logger.info("Case model loaded")
    return _pipeline


def _load_explainer():
    global _explainer
    if _explainer is None and SHAP_EXPLAINER_PATH.exists():
        _explainer = joblib.load(SHAP_EXPLAINER_PATH)
    return _explainer


def predict_case(case_data: dict) -> dict:
    pipeline = _load_model()
    df = pd.DataFrame([case_data])
    X, _ = prepare_data(df)
    proba      = pipeline.predict_proba(X)[0][1]
    pred_class = int(proba >= 0.5)
    label      = OUTCOME_LABELS[pred_class]
    confidence = round(proba * 100 if pred_class == 1 else (1 - proba) * 100, 1)

    if proba >= 0.70:
        rec = "⚠️ HIGH RISK — Consider early settlement or case review"
    elif proba >= 0.50:
        rec = "🔶 MEDIUM RISK — Strengthen legal arguments; additional evidence recommended"
    elif proba >= 0.35:
        rec = "🟡 MODERATE — Monitor closely; proceed with standard preparation"
    else:
        rec = "✅ LOW RISK — Proceed; case appears favourable for KRA"

    shap_vals = _get_shap(pipeline, X)
    return {"prediction": label, "probability": round(float(proba), 4),
            "confidence": confidence, "recommendation": rec, "shap_values": shap_vals}


def predict_batch(cases):
    return [predict_case(c) for c in cases]


def _get_shap(pipeline, X):
    return None