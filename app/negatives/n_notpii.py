"""N-NOTPII | not personal data | pairs P-CACHE | expected: 0 findings.
`product.name` is textually a `.name` access but the receiver is not a person."""
from app.lib.infra import cache
from app.models.product import Product


def store(product: Product):
    cache.set("k", product.name)
