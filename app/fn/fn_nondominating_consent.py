"""FN-NONDOM-CONSENT | a consent check that does NOT dominate the sink must NOT clear it.
Contrast with N-CONSENT (early-return guard that DOES dominate)."""
import stripe

from app.lib.consent import check_consent
from app.models.user import User


def consent_in_other_branch(user: User, data_principal_id):
    if check_consent(data_principal_id):
        pass  # consent only gates this branch, not the sink below
    stripe.customers.create(email=user.aadhaar)   # fires CRITICAL


def consent_after_sink(user: User, data_principal_id):
    stripe.customers.create(email=user.aadhaar)   # fires CRITICAL (leak already happened)
    if not check_consent(data_principal_id):
        return
