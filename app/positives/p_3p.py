"""P-3P | pii-to-third-party | DPDP-028 | expected: CRITICAL (aadhaar)."""
import stripe

from app.models.user import User


def bill(user: User):
    stripe.customers.create(email=user.aadhaar)
