"""src/document_intelligence/data_generator.py"""
import random
import pandas as pd
from faker import Faker
from config.settings import SYNTHETIC_DIR, DOCUMENT_TYPES
from src.utils.logger import get_logger

fake = Faker()
logger = get_logger(__name__)

STATUTES  = ["Section 31 of the Value Added Tax Act","Section 47 of the Income Tax Act",
             "Section 12 of the Tax Appeals Tribunal Act","Section 58 of the East African Customs Management Act",
             "Section 37 of the Tax Procedures Act","Regulation 15 of the VAT Regulations 2017"]
TAX_TYPES = ["VAT","Income Tax","Customs Duty","PAYE","Excise Duty","Withholding Tax"]
JUDGES    = ["Hon. Justice A. Mwangi","Hon. Justice B. Ochieng","Hon. Justice C. Wanjiku",
             "Hon. Justice D. Kiprop","Hon. J. Kariuki (TAT Member)","Hon. R. Omondi (TAT Chair)"]
OFFICES   = ["Times Tower, Nairobi","Mombasa Regional Office","Kisumu Regional Office"]


def _tax_assessment(i):
    amt = round(random.uniform(50_000, 50_000_000), 2)
    return {"doc_id": f"DOC-TAN-{i:05d}", "doc_type": "Tax Assessment Notice",
            "text": (f"KENYA REVENUE AUTHORITY\nTAX ASSESSMENT NOTICE\n\n"
                     f"To: {fake.company()}\nPIN: {fake.bothify('A###########B')}\n"
                     f"Date: {fake.date_between('-2y','today')}\nReference: {fake.bothify('KRA/??/####/####')}\n\n"
                     f"Pursuant to {random.choice(STATUTES)}, you are hereby notified that following a review "
                     f"of your tax returns, the Commissioner of {random.choice(TAX_TYPES)} has assessed additional "
                     f"tax liability of KES {amt:,.2f} for the period ending {fake.date_between('-1y','today')}.\n\n"
                     f"You are required to pay the assessed amount within thirty (30) days of this notice.")}

def _objection_letter(i):
    amt = round(random.uniform(50_000, 50_000_000), 2)
    return {"doc_id": f"DOC-OBJ-{i:05d}", "doc_type": "Objection Letter",
            "text": (f"THE COMMISSIONER\nKenya Revenue Authority\n{random.choice(OFFICES)}\n\n"
                     f"Date: {fake.date_between('-1y','today')}\nReference: {fake.bothify('OBJ/####/##')}\n\n"
                     f"RE: NOTICE OF OBJECTION — {random.choice(TAX_TYPES).upper()} ASSESSMENT\n\n"
                     f"I, {fake.name()}, on behalf of {fake.company()} (PIN: {fake.bothify('A###########B')}), "
                     f"hereby formally object to the assessment of KES {amt:,.2f} on the following grounds:\n\n"
                     f"1. The assessment is contrary to {random.choice(STATUTES)}.\n"
                     f"2. The Commissioner failed to consider supporting documentation submitted.\n"
                     f"3. The assessed amount is excessive and not supported by the evidence on record.\n\n"
                     f"We respectfully request a review and withdrawal of the said assessment.")}

def _court_summons(i):
    case_no = fake.bothify("HC/TAX/####/####")
    return {"doc_id": f"DOC-SUM-{i:05d}", "doc_type": "Court Summons",
            "text": (f"IN THE HIGH COURT OF KENYA\nAT NAIROBI\nCOMMERCIAL AND TAX DIVISION\n\n"
                     f"CASE NO: {case_no}\n\nBETWEEN\n"
                     f"{fake.company().upper()}  ........................... PETITIONER\nAND\n"
                     f"KENYA REVENUE AUTHORITY  ........................... RESPONDENT\n\n"
                     f"SUMMONS\n\nTo: The Commissioner General, Kenya Revenue Authority, Times Tower, Nairobi.\n\n"
                     f"You are hereby summoned to appear before {random.choice(JUDGES)} on "
                     f"{fake.date_between('today','+6M')} at 9:00 AM in Court Room {random.randint(1,20)}.\n\n"
                     f"Served by: {fake.name()}, Advocate\nDate served: {fake.date_between('-30d','today')}")}

def _demand_notice(i):
    outstanding = round(random.uniform(10_000, 20_000_000), 2)
    penalties   = round(outstanding * random.uniform(0.02, 0.10), 2)
    return {"doc_id": f"DOC-DEM-{i:05d}", "doc_type": "Demand Notice",
            "text": (f"KENYA REVENUE AUTHORITY\nFINAL DEMAND NOTICE\n\n"
                     f"To: {fake.company()}\nPIN: {fake.bothify('A###########B')}\n"
                     f"Date: {fake.date_between('-6M','today')}\n"
                     f"Payment Ref: {fake.bothify('KRA-PAY-########')}\n\n"
                     f"TAKE NOTICE that you owe the Kenya Revenue Authority the following outstanding "
                     f"{random.choice(TAX_TYPES)} liabilities:\n\n"
                     f"  Principal Tax:   KES {outstanding:,.2f}\n"
                     f"  Penalties:       KES {penalties:,.2f}\n"
                     f"  Total Due:       KES {outstanding + penalties:,.2f}\n\n"
                     f"Payment is due by {fake.date_between('today','+30d')}.")}

def _tribunal_ruling(i):
    case_no  = fake.bothify("TAT/####/####")
    decision = random.choice(["Appeal Allowed","Appeal Dismissed","Appeal Partially Allowed"])
    return {"doc_id": f"DOC-RUL-{i:05d}", "doc_type": "Tribunal Ruling",
            "text": (f"TAX APPEALS TRIBUNAL\nRULING\n\n"
                     f"TAT CASE NO: {case_no}\nDate: {fake.date_between('-2y','today')}\n\n"
                     f"CORAM: {random.choice(JUDGES)}\n\nBETWEEN\n"
                     f"{fake.company().upper()}  ................. APPELLANT\nAND\n"
                     f"KENYA REVENUE AUTHORITY  ................. RESPONDENT\n\n"
                     f"Having considered the submissions of both parties and the evidence on record, "
                     f"this Tribunal finds that {random.choice(STATUTES)} was "
                     f"{random.choice(['correctly','incorrectly'])} applied by the Respondent.\n\n"
                     f"DECISION: {decision.upper()}.\n\nSigned: {random.choice(JUDGES)}")}

def _appeal_notice(i):
    return {"doc_id": f"DOC-APP-{i:05d}", "doc_type": "Appeal Notice",
            "text": (f"NOTICE OF APPEAL\n\nTO: The Registrar, Tax Appeals Tribunal\n"
                     f"FROM: {fake.company()} (PIN: {fake.bothify('A###########B')})\n"
                     f"Date: {fake.date_between('-1y','today')}\n"
                     f"Original Case Ref: {fake.bothify('TAT/####/####')}\n\n"
                     f"TAKE NOTICE that the Appellant, being dissatisfied with the ruling delivered on "
                     f"{fake.date_between('-6M','-1M')}, hereby appeals to the High Court of Kenya on the "
                     f"following grounds:\n\n"
                     f"1. The Tribunal erred in law in its interpretation of {random.choice(STATUTES)}.\n"
                     f"2. The Tribunal failed to consider material evidence submitted by the Appellant.\n"
                     f"3. The decision is against the weight of evidence.\n\n"
                     f"Signed: {fake.name()}, Advocate for the Appellant")}


GENERATORS = {
    "Tax Assessment Notice": _tax_assessment,
    "Objection Letter":      _objection_letter,
    "Court Summons":         _court_summons,
    "Demand Notice":         _demand_notice,
    "Tribunal Ruling":       _tribunal_ruling,
    "Appeal Notice":         _appeal_notice,
}


def generate_documents(n_per_type=250, random_seed=42):
    random.seed(random_seed)
    records = []
    for doc_type, gen_fn in GENERATORS.items():
        for i in range(n_per_type):
            records.append(gen_fn(i))
    df = pd.DataFrame(records)
    logger.info("Generated %d documents (%d types × %d)", len(df), len(GENERATORS), n_per_type)
    return df


def save_documents(df, filename="documents_synthetic.csv"):
    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    path = SYNTHETIC_DIR / filename
    df.to_csv(path, index=False)
    logger.info("Documents saved → %s", path)
    return path


if __name__ == "__main__":
    df = generate_documents(250)
    save_documents(df)
    print(df["doc_type"].value_counts())
