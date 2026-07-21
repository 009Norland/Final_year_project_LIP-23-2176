"""src/dashboard/auth.py — User authentication for KRA-LIP."""
import json
import hashlib
from pathlib import Path
from config.settings import DATA_DIR

USERS_FILE = DATA_DIR / "processed" / "users.json"
USERS_FILE.parent.mkdir(parents=True, exist_ok=True)


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _load_users() -> list:
    if not USERS_FILE.exists():
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users: list):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def seed_admin():
    """Create a default admin account on first run."""
    users = _load_users()
    if any(u["username"] == "admin" for u in users):
        return
    users.append({
        "full_name": "System Administrator",
        "username":  "admin",
        "password":  _hash("admin123"),
        "role":      "Admin",
    })
    _save_users(users)


def sign_up(full_name: str, username: str, password: str, role: str) -> tuple[bool, str]:
    full_name = full_name.strip()
    username  = username.strip()
    password  = password.strip()

    if not full_name or not username or not password:
        return False, "All fields are required."
    if " " in username:
        return False, "Username cannot contain spaces. Example: JohnOmondi"
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users = _load_users()
    if any(u["username"] == username for u in users):
        return False, "That username is already taken. Please choose another."

    users.append({
        "full_name": full_name,
        "username":  username,
        "password":  _hash(password),
        "role":      role,
    })
    _save_users(users)
    return True, "Account created successfully."


def login(username: str, password: str) -> tuple[bool, dict]:
    users = _load_users()
    for u in users:
        if u["username"] == username.strip() and u["password"] == _hash(password.strip()):
            return True, {
                "full_name": u.get("full_name", u["username"]),
                "username":  u["username"],
                "role":      u["role"],
            }
    return False, {}


def get_all_users() -> list:
    return [
        {
            "full_name": u.get("full_name", "-"),
            "username":  u["username"],
            "role":      u["role"],
        }
        for u in _load_users()
    ]


def delete_user(username: str) -> bool:
    users = _load_users()
    new_users = [u for u in users if u["username"] != username]
    if len(new_users) == len(users):
        return False
    _save_users(new_users)
    return True