"""FN-INTERPROC (file 1/3) | reads PII, hands it to a helper in another file.
Flow: interproc_a.run -> interproc_b.forward -> interproc_c.emit (logger.info).
Expected: ONE finding at the sink (interproc_c.py), pii=aadhaar, CRITICAL."""
from app.fn.interproc_b import forward
from app.models.user import User


def run(user: User):
    data = user.aadhaar
    forward(data)
