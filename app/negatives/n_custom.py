"""N-CUSTOM | sanitiser layer 3 (.svorah.yml custom_sanitisers: [to_stars]) |
pairs P-FILE | expected: 0 findings WHILE `to_stars` is configured.
X-L3TOGGLE re-runs this file with that config removed -> it must flip to a positive."""
from pathlib import Path

from app.lib.sanitizers import to_stars
from app.models.user import User


def dump(user: User):
    Path("export.txt").write_text(to_stars(user.pan))
