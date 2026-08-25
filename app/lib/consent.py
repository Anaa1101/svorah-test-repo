"""Consent lookup. A call to `check_consent(...)` that dominates a sink (i.e. the
sink is unreachable unless consent is present) clears the flow. N-CONSENT depends
on this dominance relationship."""

_granted = set()


def check_consent(data_principal_id) -> bool:
    return data_principal_id in _granted


def grant(data_principal_id) -> None:
    _granted.add(data_principal_id)
