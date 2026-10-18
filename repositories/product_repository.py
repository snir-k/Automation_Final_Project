from typing import List
from models.models import Product


class ProductRepositoryError(Exception): pass

# Simulation of the database for testing purposes
_db_mock: dict[int, Product] = {}
_id_counter: int = 1


def reset_db() -> None:
    global _db_mock, _id_counter
    _db_mock.clear()
    _id_counter = 1


def create_product(product: Product) -> int:
    global _id_counter
    if not product.name:
        raise ProductRepositoryError("Product Column cannot be null")
    if len(product.name) > 50:
        raise ProductRepositoryError(f"Product name too long: {len(product.name)}")
    if product.price is None:
        raise ProductRepositoryError("Product Column cannot be null")

    for p in _db_mock.values():
        if p.name == product.name:
            raise ProductRepositoryError(f"Product name exists: {product.name}")

    # Saving the current ID in a local variable which is definitely an int
    assigned_id = _id_counter

    # Updating the object and the dictionary
    product.product_id = assigned_id
    _db_mock[assigned_id] = Product(product.product_id, product.name, product.price, product.image)

    # Promoting the counter to the next level
    _id_counter += 1

    # Returning the local variable (which is a pure int)
    # completely resolves the warning!
    return assigned_id


def read_one(product_id: int) -> Product | None:
    return _db_mock.get(product_id, None)


def read_all() -> List[Product]:
    return list(_db_mock.values())


def update_product(product: Product) -> bool:
    # Guard against None product_id to resolve Expected type 'int' warning
    if product.product_id is None:
        return False

    if product.product_id not in _db_mock:
        return False
    if not product.name:
        raise ProductRepositoryError("Product Column cannot be null")
    if len(product.name) > 50:
        raise ProductRepositoryError(f"Product name too long: {len(product.name)}")
    if product.price is None:
        raise ProductRepositoryError("Product Column cannot be null")

    for p_id, p in _db_mock.items():
        if p.name == product.name and p_id != product.product_id:
            raise ProductRepositoryError(f"Product name exists: {product.name}")

    _db_mock[product.product_id] = Product(product.product_id, product.name, product.price, product.image)
    return True


def delete_product(product_id: int) -> bool:
    if product_id in _db_mock:
        del _db_mock[product_id]
        return True
    return False
