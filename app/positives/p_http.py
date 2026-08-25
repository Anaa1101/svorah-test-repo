"""P-HTTP | pii-external-api | DPDP-028 | expected: MEDIUM (email)."""
import requests

from app.models.user import User


def send(user: User):
    requests.post("https://api.partner.example/collect", json={"email": user.email})
