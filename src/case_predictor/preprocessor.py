"""src/case_predictor/preprocessor.py"""
import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from config.settings import MODELS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

CATEGORICAL_FEATURES = ["case_type","court_level","taxpayer_category","legal_grounds","representation"]
NUMERICAL_FEATURES   = ["disputed_amount","case_duration_days","prior_compliance_score",
                        "num_prior_disputes","taxpayer_risk_score"]
TARGET = "outcome"


def engineer_features(df):
    df = df.copy()
    df["log_disputed_amount"] = np.log1p(df["disputed_amount"])
    df["complexity_score"] = (df["case_duration_days"]/365*0.3 +
                               df["num_prior_disputes"]*0.2 +
                               np.log1p(df["disputed_amount"])/20*0.5).round(4)
    df["is_high_court"]     = (df["court_level"] != "Tax Appeals Tribunal").astype(int)
    df["has_counsel"]       = (df["representation"] == "Legal Counsel").astype(int)
    df["taxpayer_risk_flag"]= ((df["taxpayer_risk_score"] > 65) & (df["prior_compliance_score"] < 40)).astype(int)
    return df


def build_preprocessor():
    extended_num = NUMERICAL_FEATURES + ["log_disputed_amount","complexity_score",
                                         "is_high_court","has_counsel","taxpayer_risk_flag"]
    return ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_FEATURES),
        ("num", StandardScaler(), extended_num),
    ], remainder="drop")


def prepare_data(df):
    df = engineer_features(df)
    drop_cols = ["case_id", TARGET] if TARGET in df.columns else ["case_id"]
    drop_cols = [c for c in drop_cols if c in df.columns]
    X = df.drop(columns=drop_cols)
    y = df[TARGET] if TARGET in df.columns else None
    logger.info("Prepared: %d rows × %d cols", X.shape[0], X.shape[1])
    return X, y


def save_preprocessor(preprocessor, path=None):
    path = path or MODELS_DIR / "case_predictor" / "preprocessor.pkl"
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, path)

def load_preprocessor(path=None):
    path = path or MODELS_DIR / "case_predictor" / "preprocessor.pkl"
    return joblib.load(path)
