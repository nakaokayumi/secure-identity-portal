import re
from werkzeug.security import generate_password_hash, check_password_hash

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match((email or "").strip().lower()))

def is_strong_password(pw: str) -> bool:
    if not pw or len(pw) < 8:
        return False
    # at least 1 letter and 1 number
    has_letter = any(c.isalpha() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    return has_letter and has_digit

def hash_password(pw: str) -> str:
    return generate_password_hash(pw)

def verify_password(pw: str, pw_hash: str) -> bool:
    return check_password_hash(pw_hash, pw)
