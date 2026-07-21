"""
src/case_predictor/data_generator.py
Generates synthetic KRA tax dispute case records.
"""
import random
import numpy as np
import pandas as pd
from faker import Faker
from config.settings import SYNTHETIC_DIR
from src.utils.logger import get_logger

fake = Faker()
logger = get_logger(__name__)

CASE_TYPES    = ["VAT","Income Tax","Customs Duty","Excise Duty","PAYE","Withholding Tax"]
COURT_LEVELS  = ["Tax Appeals Tribunal","High Court","Court of Appeal"]
TAXPAYER_CATS = ["Individual","SME","Large Corporation","Multinational"]
LEGAL_GROUNDS = ["Procedural Error","Incorrect Assessment","Statute of Limitations",
                 "Double Taxation","Transfer Pricing Dispute","Exemption Claim",
                 "Valuation Dispute","Input Tax Credit"]
REPRESENTATION = ["Self-Represented","Legal Counsel","Tax Consultant"]


def _outcome_probability(row):
    p = 0.30

    if row["disputed_amount"] > 5_000_000:  p += 0.12
    if row["disputed_amount"] > 20_000_000: p += 0.12

    if row["court_level"] == "High Court":        p += 0.14
    elif row["court_level"] == "Court of Appeal": p += 0.24

    if row["representation"] == "Legal Counsel":      p += 0.18
    elif row["representation"] == "Self-Represented": p -= 0.18

    if row["taxpayer_category"] == "Multinational":      p += 0.16
    elif row["taxpayer_category"] == "Large Corporation": p += 0.08
    elif row["taxpayer_category"] == "Individual":        p -= 0.08

    if row["legal_grounds"] == "Procedural Error":         p += 0.22
    elif row["legal_grounds"] == "Transfer Pricing Dispute": p += 0.14
    elif row["legal_grounds"] == "Incorrect Assessment":    p += 0.10
    elif row["legal_grounds"] == "Exemption Claim":         p -= 0.08

    if row["case_duration_days"] > 730:   p += 0.12
    elif row["case_duration_days"] < 120: p -= 0.08

    if row["prior_compliance_score"] < 30:   p -= 0.16
    elif row["prior_compliance_score"] < 50: p -= 0.08
    elif row["prior_compliance_score"] > 80: p += 0.10

    if row["num_prior_disputes"] > 5:     p += 0.10
    elif row["num_prior_disputes"] == 0:  p -= 0.06

    if row["taxpayer_risk_score"] > 70:   p -= 0.16
    elif row["taxpayer_risk_score"] < 20: p += 0.08

    return float(np.clip(p, 0.05, 0.95))


def generate_cases(n=1500, random_seed=42):
    random.seed(random_seed); np.random.seed(random_seed)
    records = []
    for i in range(n):
        row = {
            "case_id": f"KRA-CASE-{i+1:05d}",
            "case_type": random.choice(CASE_TYPES),
            "disputed_amount": round(random.uniform(50_000, 100_000_000), 2),
            "court_level": random.choices(COURT_LEVELS, weights=[0.60,0.30,0.10])[0],
            "taxpayer_category": random.choices(TAXPAYER_CATS, weights=[0.25,0.35,0.25,0.15])[0],
            "legal_grounds": random.choice(LEGAL_GROUNDS),
            "case_duration_days": random.randint(30, 1825),
            "prior_compliance_score": random.randint(0, 100),
            "representation": random.choices(REPRESENTATION, weights=[0.20,0.55,0.25])[0],
            "num_prior_disputes": random.randint(0, 15),
            "taxpayer_risk_score": random.randint(0, 100),
        }
        row["outcome"] = int(np.random.binomial(1, _outcome_probability(row)))
        records.append(row)
    df = pd.DataFrame(records)
    logger.info("Generated %d case records (KRA wins: %d | KRA loses: %d)",
                n, (df["outcome"]==0).sum(), (df["outcome"]==1).sum())
    return df


def save_cases(df, filename="cases_synthetic.csv"):
    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    path = SYNTHETIC_DIR / filename
    df.to_csv(path, index=False)
    logger.info("Cases saved → %s", path)
    return path


if __name__ == "__main__":
    df = generate_cases(1500)
    save_cases(df)
    print(df["outcome"].value_counts())
