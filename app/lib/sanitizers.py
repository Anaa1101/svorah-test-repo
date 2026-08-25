"""Sanitisers defined in-repo.

- `mask` is a layer-1 sanitiser (recognised by verb).
- `to_stars` is NOT a built-in verb; it only clears taint when listed under
  `custom_sanitisers` in .svorah.yml (layer 3). N-CUSTOM / X-L3TOGGLE depend on it.
"""


def mask(value):
    s = "" if value is None else str(value)
    return (s[0] + "***") if s else s


def to_stars(value):
    return "****" if value else value


def toStars(value):
    """Same behaviour as to_stars, but this NAME is not in .svorah.yml
    custom_sanitisers ([to_stars]). A flow through toStars must therefore still FIRE."""
    return "****" if value else value
