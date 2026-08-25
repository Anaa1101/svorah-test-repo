"""P-URL | pii-in-url | DPDP-004 | expected: MEDIUM (phone)."""
from urllib.parse import urlencode

from app.models.user import User


def build_tracking_link(user: User):
    query = urlencode({"p": user.phone})
    return "https://track.example/open?" + query
