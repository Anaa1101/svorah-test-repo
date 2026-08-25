"""FN-PARTIAL | sanitising one argument must not clear a different tainted argument.
`to=` is masked, but `body=` still carries raw aadhaar -> fires."""
from app.lib.infra import mailer
from app.lib.sanitizers import mask
from app.models.user import User


def notify(user: User):
    mailer.send_mail(to=mask(user.email), body=user.aadhaar)   # fires CRITICAL (body)
