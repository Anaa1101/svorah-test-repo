"""FN-NAMEMISMATCH | .svorah.yml lists custom_sanitiser `to_stars`, but this code calls
`toStars` (different name). The name does not match, so taint is NOT cleared -> fires."""
from pathlib import Path

from app.lib.sanitizers import toStars
from app.models.user import User


def dump(user: User):
    Path("export.txt").write_text(toStars(user.pan))   # fires HIGH (pan)
