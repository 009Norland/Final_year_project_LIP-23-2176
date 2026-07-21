"""
src/dashboard/case_store.py
Stores cases in local JSON file only. MongoDB disabled.
"""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from config.settings import DATA_DIR

LOCAL_STORE = DATA_DIR / "processed" / "case_store.json"
LOCAL_STORE.parent.mkdir(parents=True, exist_ok=True)


def _load_local():
    if not LOCAL_STORE.exists():
        return []
    try:
        with open(LOCAL_STORE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_local(records):
    with open(LOCAL_STORE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, default=str)


def add_case(case: dict) -> str:
    case = case.copy()
    case.setdefault("case_id", f"A{uuid.uuid4().hex[:8].upper()}")
    case.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    case.setdefault("status", "Open")
    records = _load_local()
    records.append(case)
    _save_local(records)
    return case["case_id"]


def get_all_cases():
    return _load_local()


def get_case(case_id: str):
    return next((c for c in _load_local() if c.get("case_id") == case_id), None)


def update_case(case_id: str, updates: dict) -> bool:
    records = _load_local()
    for c in records:
        if c.get("case_id") == case_id:
            c.update(updates)
            _save_local(records)
            return True
    return False


def delete_case(case_id: str) -> bool:
    records = _load_local()
    new_records = [c for c in records if c.get("case_id") != case_id]
    if len(new_records) != len(records):
        _save_local(new_records)
        return True
    return False


def seed_demo_cases():
    if _load_local():
        return
    demo = [
        {
            "case_id": "A0012345",
            "taxpayer_name": "Kipchoge Tea Exporters Ltd",
            "pin": "A012345678B",
            "plaintiff": "Kipchoge Tea Exporters Ltd",
            "defendant": "Kenya Revenue Authority",
            "case_type": "VAT",
            "disputed_amount": 17_635_000,
            "court_level": "High Court",
            "taxpayer_category": "Large Corporation",
            "legal_grounds": "Procedural Error",
            "representation": "Legal Counsel",
            "case_duration_days": 410,
            "prior_compliance_score": 58,
            "num_prior_disputes": 2,
            "taxpayer_risk_score": 22,
            "status": "Open",
            "prediction": "KRA Loses",
            "win_probability": 22.0,
            "risk_level": "High",
            "assigned_to": "",
            "created_by": "admin",
        },
        {
            "case_id": "A0012346",
            "taxpayer_name": "Rift Valley Mills Co.",
            "pin": "A019988776C",
            "plaintiff": "Rift Valley Mills Co.",
            "defendant": "Kenya Revenue Authority",
            "case_type": "Income Tax",
            "disputed_amount": 4_200_000,
            "court_level": "Tax Appeals Tribunal",
            "taxpayer_category": "SME",
            "legal_grounds": "Incorrect Assessment",
            "representation": "Tax Consultant",
            "case_duration_days": 180,
            "prior_compliance_score": 72,
            "num_prior_disputes": 0,
            "taxpayer_risk_score": 12,
            "status": "Pending",
            "prediction": "KRA Wins",
            "win_probability": 81.0,
            "risk_level": "Low",
            "assigned_to": "",
            "created_by": "admin",
        },
        {
            "case_id": "A0012347",
            "taxpayer_name": "Coastal Freight Movers",
            "pin": "A045566778D",
            "plaintiff": "Coastal Freight Movers",
            "defendant": "Kenya Revenue Authority",
            "case_type": "Customs Duty",
            "disputed_amount": 9_800_000,
            "court_level": "Court of Appeal",
            "taxpayer_category": "Multinational",
            "legal_grounds": "Transfer Pricing Dispute",
            "representation": "Legal Counsel",
            "case_duration_days": 920,
            "prior_compliance_score": 40,
            "num_prior_disputes": 5,
            "taxpayer_risk_score": 65,
            "status": "Closed",
            "prediction": "KRA Loses",
            "win_probability": 31.0,
            "risk_level": "High",
            "assigned_to": "",
            "created_by": "admin",
        },
        {
            "case_id": "A0012348",
            "taxpayer_name": "Nyeri Highland Produce",
            "pin": "A033221144E",
            "plaintiff": "Nyeri Highland Produce",
            "defendant": "Kenya Revenue Authority",
            "case_type": "Excise Duty",
            "disputed_amount": 650_000,
            "court_level": "Tax Appeals Tribunal",
            "taxpayer_category": "Individual",
            "legal_grounds": "Exemption Claim",
            "representation": "Self-Represented",
            "case_duration_days": 95,
            "prior_compliance_score": 88,
            "num_prior_disputes": 0,
            "taxpayer_risk_score": 5,
            "status": "Open",
            "prediction": "KRA Wins",
            "win_probability": 78.0,
            "risk_level": "Low",
            "assigned_to": "",
            "created_by": "admin",
        },
    ]
    for c in demo:
        add_case(c)