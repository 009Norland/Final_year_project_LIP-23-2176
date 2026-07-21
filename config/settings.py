import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

MONGO_URI     = os.getenv("MONGO_URI", "")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "kra_lip")
COLLECTIONS   = {"cases": "case_records", "documents": "legal_documents", "taxpayers": "taxpayer_profiles", "predictions": "predictions_log"}

FLASK_HOST  = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT  = int(os.getenv("FLASK_PORT", 5000))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
SECRET_KEY  = os.getenv("SECRET_KEY", "dev-secret-key")

MODELS_DIR          = BASE_DIR / "models"
CASE_MODEL_PATH     = MODELS_DIR / "case_predictor" / "xgb_case_model.pkl"
DOC_MODEL_PATH      = MODELS_DIR / "document_intelligence" / "tfidf_svm_doc_model.pkl"
SHAP_EXPLAINER_PATH = MODELS_DIR / "case_predictor" / "shap_explainer.pkl"

DATA_DIR      = BASE_DIR / "data"
RAW_DIR       = DATA_DIR / "raw"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
PROCESSED_DIR = DATA_DIR / "processed"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE  = BASE_DIR / "logs" / "kra_lip.log"

CASE_PREDICTOR = {
    "test_size": 0.2, "random_state": 42, "cv_folds": 5,
    "xgb_params": {"n_estimators": 300, "max_depth": 6, "learning_rate": 0.05,
                   "subsample": 0.8, "colsample_bytree": 0.8, "eval_metric": "logloss", "random_state": 42}
}
DOCUMENT_CLASSIFIER = {
    "test_size": 0.2, "random_state": 42,
    "tfidf_params": {"max_features": 10000, "ngram_range": (1, 2), "sublinear_tf": True},
    "svm_params": {"kernel": "linear", "C": 1.0, "probability": True}
}
DOCUMENT_TYPES = ["Tax Assessment Notice","Objection Letter","Court Summons","Demand Notice","Tribunal Ruling","Appeal Notice"]
OUTCOME_LABELS = {0: "KRA Wins", 1: "KRA Loses"}
