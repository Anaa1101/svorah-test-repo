"""P-CACHE | pii-in-cache | DPDP-027 | expected: MEDIUM (email)."""
from app.lib.infra import cache
from app.models.user import User


def store(user: User):
    cache.set("k", user.email)
