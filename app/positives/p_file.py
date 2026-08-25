"""P-FILE | pii-to-file | DPDP-006 | expected: HIGH (pan)."""
from pathlib import Path

from app.models.user import User


def dump(user: User):
    Path("export.txt").write_text(user.pan)
