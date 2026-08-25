"""X-NAMEGATE | person-noun gate.
`user.name` is personal data; `product.name` is not — same sink, same field name."""
from app.lib.infra import cache
from app.models.product import Product
from app.models.user import User


def store(user: User, product: Product):
    cache.set("u", user.name)      # expected: fires (MEDIUM)
    cache.set("p", product.name)   # expected: no finding
