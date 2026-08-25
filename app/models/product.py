"""Non-person entity. `Product.name` looks like `User.name` textually but is NOT
personal data. Used by N-NOTPII and X-NAMEGATE to prove the person-noun gate."""


class Product:
    def __init__(self):
        self.name = ""       # NOT personal data (product, not a person)
        self.sku = ""
        self.price = 0


def load_product() -> "Product":
    return Product()
