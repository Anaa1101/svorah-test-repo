"""In-repo sink objects.

- `cache` is a recognised cache sink (receiver-constrained: `cache.set`).
- `r` is a bare client whose `set` is NOT a recognised cache sink (X-ALIAS).
- `mailer.send_mail(to=..., body=...)`: only PII in `body` is a finding; the
  `to=` recipient is excluded (N-RECIP).
"""


class _Cache:
    def set(self, key, value):
        pass

    def get(self, key):
        return None


class _BareClient:
    def set(self, key, value):
        pass


class _Mailer:
    def send_mail(self, to=None, body=None, subject=None):
        pass


cache = _Cache()
r = _BareClient()
mailer = _Mailer()
