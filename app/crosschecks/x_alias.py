"""X-ALIAS | receiver-constrained sinks.
`cache.set` is a recognised cache sink; a bare `r.set` is not."""
from app.lib.infra import cache, r
from app.models.user import User


def store(user: User):
    cache.set("k", user.email)   # expected: fires (MEDIUM)
    r.set("k", user.email)       # expected: no finding
