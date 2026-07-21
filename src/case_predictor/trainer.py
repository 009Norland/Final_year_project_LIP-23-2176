"""src/case_predictor/trainer.py"""
import joblib
import numpy as np
import pandas as pd
import shap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import (accuracy_score, f1_score, roc_auc_score,
                             classification_report, confusion_matrix, ConfusionMatrixDisplay)
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from src.case_predictor.data_generator import generate_cases, save_cases
from src.case_predictor.preprocessor import build_preprocessor, prepare_data
from src.utils.logger import get_logger
from config.settings import CASE_PREDICTOR, MODELS_DIR

logger = get_logger(__name__)
MODEL_DIR = MODELS_DIR / "case_predictor"


def get_models():
    return {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, n_jobs=-1),
        "XGBoost": XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05,
                                  subsample=0.8, colsample_bytree=0.8,
                                  eval_metric="logloss", random_state=42),
    }


def train(n_samples=1500):
    logger.info("═══ Case Outcome Predictor — Training ═══")

    df = generate_cases(n=n_samples)
    save_cases(df)
    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=CASE_PREDICTOR["test_size"],
        random_state=CASE_PREDICTOR["random_state"], stratify=y)
    logger.info("Train: %d  |  Test: %d", len(X_train), len(X_test))

    preprocessor = build_preprocessor()
    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in get_models().items():
        pipe = Pipeline([("preprocessor", preprocessor), ("model", model)])
        cv_auc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc")
        pipe.fit(X_train, y_train)
        y_pred  = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1]
        results[name] = {
            "accuracy":     round(accuracy_score(y_test, y_pred), 4),
            "f1":           round(f1_score(y_test, y_pred), 4),
            "roc_auc":      round(roc_auc_score(y_test, y_proba), 4),
            "cv_auc_mean":  round(cv_auc.mean(), 4),
            "cv_auc_std":   round(cv_auc.std(), 4),
            "pipeline": pipe,
        }
        logger.info("%s — Acc: %.4f | F1: %.4f | AUC: %.4f | CV-AUC: %.4f ± %.4f",
                    name, results[name]["accuracy"], results[name]["f1"],
                    results[name]["roc_auc"], results[name]["cv_auc_mean"], results[name]["cv_auc_std"])

    best_name = max(results, key=lambda k: results[k]["roc_auc"])
    best_pipe  = results[best_name]["pipeline"]
    logger.info("✅ Best model: %s (AUC = %.4f)", best_name, results[best_name]["roc_auc"])

    y_pred_best = best_pipe.predict(X_test)
    logger.info("\n%s", classification_report(y_test, y_pred_best, target_names=["KRA Wins","KRA Loses"]))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "xgb_case_model.pkl"
    joblib.dump(best_pipe, model_path)
    logger.info("Model saved → %s", model_path)

    _save_shap_explainer(best_pipe, X_train)
    _plot_confusion_matrix(y_test, y_pred_best, best_name)

    return best_pipe, results


def _save_shap_explainer(pipeline, X_train):
    try:
        X_tr = pipeline.named_steps["preprocessor"].transform(X_train)
        model = pipeline.named_steps["model"]
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        if isinstance(model, LogisticRegression):
            explainer = shap.LinearExplainer(model, X_tr)
        else:
            explainer = shap.TreeExplainer(model)
        path = MODEL_DIR / "shap_explainer.pkl"
        joblib.dump(explainer, path)
        logger.info("SHAP explainer saved → %s", path)
    except Exception as e:
        logger.warning("SHAP explainer could not be saved: %s", e)


def _plot_confusion_matrix(y_test, y_pred, model_name):
    try:
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(cm, display_labels=["KRA Wins","KRA Loses"])
        fig, ax = plt.subplots(figsize=(6, 5))
        disp.plot(ax=ax, colorbar=False, cmap="Blues")
        ax.set_title(f"Confusion Matrix — {model_name}")
        fig.savefig(MODEL_DIR / "confusion_matrix.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Confusion matrix saved")
    except Exception as e:
        logger.warning("Could not save confusion matrix: %s", e)


if __name__ == "__main__":
    train()
