"""src/document_intelligence/trainer.py"""
import joblib
import re
import string
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score

from src.document_intelligence.data_generator import generate_documents, save_documents
from src.utils.logger import get_logger
from config.settings import MODELS_DIR, DOCUMENT_CLASSIFIER

logger = get_logger(__name__)
MODEL_DIR = MODELS_DIR / "document_intelligence"


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\d{4,}', 'NUM', text)
    text = re.sub(r'kes[\s,]*[\d,.]+', 'AMOUNT', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()


def train(n_per_type=250):
    logger.info("═══ Document Intelligence Engine — Training ═══")

    df = generate_documents(n_per_type=n_per_type)
    save_documents(df)

    df["clean_text"] = df["text"].apply(clean_text)
    X = df["clean_text"]
    y = df["doc_type"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=DOCUMENT_CLASSIFIER["test_size"],
        random_state=DOCUMENT_CLASSIFIER["random_state"], stratify=y)
    logger.info("Train: %d  |  Test: %d", len(X_train), len(X_test))

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(**DOCUMENT_CLASSIFIER["tfidf_params"])),
        ("svm",   CalibratedClassifierCV(SVC(kernel="linear", C=1.0), ensemble=False)),
    ])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_f1 = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1_macro")
    logger.info("CV Macro F1: %.4f ± %.4f", cv_f1.mean(), cv_f1.std())

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1  = f1_score(y_test, y_pred, average="macro")
    logger.info("✅ Accuracy: %.4f  |  Macro F1: %.4f", acc, f1)
    logger.info("\n%s", classification_report(y_test, y_pred))

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "tfidf_svm_doc_model.pkl"
    joblib.dump(pipeline, model_path)
    joblib.dump(list(y.unique()), MODEL_DIR / "doc_labels.pkl")
    logger.info("Document model saved → %s", model_path)

    _plot_confusion_matrix(y_test, y_pred, list(y.unique()))
    return pipeline


def _plot_confusion_matrix(y_test, y_pred, labels):
    try:
        cm = confusion_matrix(y_test, y_pred, labels=labels)
        fig, ax = plt.subplots(figsize=(9, 7))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_title("Document Classification — Confusion Matrix")
        ax.set_ylabel("True"); ax.set_xlabel("Predicted")
        plt.xticks(rotation=30, ha="right"); plt.tight_layout()
        fig.savefig(MODEL_DIR / "doc_confusion_matrix.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info("Confusion matrix saved")
    except Exception as e:
        logger.warning("Could not save confusion matrix: %s", e)


if __name__ == "__main__":
    train()
