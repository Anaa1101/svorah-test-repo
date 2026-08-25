"""N-RECIP | email recipient excluded | pairs P-EMAIL | expected: 0 findings.
`to=user.email` is a delivery recipient, not PII disclosed in content; body is clean."""
from app.lib.infra import mailer
from app.models.user import User


def notify(user: User):
    mailer.send_mail(to=user.email, body="hi")
