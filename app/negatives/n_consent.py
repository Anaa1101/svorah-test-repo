"""N-CONSENT | consent gate (CFG dominance) | pairs P-3P | expected: 0 findings.
The early return means the stripe call is unreachable without consent, so the guard
dominates the sink and the flow is cleared."""
import stripe

from app.lib.consent import check_consent
from app.models.user import User


def bill(user: User, data_principal_id):
    if not check_consent(data_principal_id):
        return
    stripe.customers.create(email=user.aadhaar)
