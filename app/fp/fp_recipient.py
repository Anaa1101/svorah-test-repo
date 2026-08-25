"""FP-RECIPIENT | recipient-only send with no PII in the body must not fire (cf. N-RECIP)."""
from app.lib.infra import mailer
from app.models.user import User


def notify(user: User):
    mailer.send_mail(to=user.email, subject="Hi")   # recipient + subject only, no body PII
