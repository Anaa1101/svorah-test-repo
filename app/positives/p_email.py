"""P-EMAIL | pii-in-email | DPDP-029 | expected: HIGH (pan in body)."""
from app.lib.infra import mailer
from app.models.user import User


def notify(user: User):
    mailer.send_mail(to="ops@example.com", body="Customer PAN on file: " + user.pan)
