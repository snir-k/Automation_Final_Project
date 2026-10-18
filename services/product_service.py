from typing import List
from repositories import product_repository
from models.models import Product
from repositories.product_repository import ProductRepositoryError


class ProductNotFoundServiceError(Exception):
    """Exception raised when a product resource is not found in the repository."""
    pass


class ProductServiceError(Exception):
    """Exception raised for core business logic and validation failures."""
    pass


def _validate_product_types(product: Product) -> None:
    """
    Private Helper: Validates runtime data types, boundaries, and strips spaces
    to prevent server crashes, SQL injections, or unhandled exceptions.
    (Fixes Bug #3, #4 & #11)
    """
    # FIXES BUG #11: Strip whitespaces from text inputs to prevent text pollution fields
    if product.name is not None and isinstance(product.name, str):
        product.name = product.name.strip()

    if product.image is not None and isinstance(product.image, str):
        product.image = product.image.strip()

    # Validate Price Type and Range
    if product.price is not None and not isinstance(product.price, (int, float)):
        raise TypeError("Product price must be a number.")

    if product.price is None or product.price < 0:
        raise ProductServiceError("Product price must be positive.")

    # Validate Name Type and Range
    if product.name is not None and not isinstance(product.name, str):
        raise TypeError("Product name must be a string.")

    if not product.name or len(product.name) < 2:
        raise ProductServiceError("Product name must be at least 2 characters long.")

    # Validate Image Type (If provided, it must be a valid string path)
    if product.image is not None and not isinstance(product.image, str):
        raise TypeError("Product image path must be a string.")


def add_product(product: Product) -> int:
    """Triggers business validations and delegates persistence creation to the repository layer."""
    _validate_product_types(product)
    try:
        return product_repository.create_product(product)
    except ProductRepositoryError as e:
        raise ProductServiceError(str(e))


def get_product(product_id: int) -> Product:
    """Fixes Bug #5: Guard clause against invalid or negative IDs during product retrieval."""
    if not isinstance(product_id, int) or product_id <= 0:
        raise ProductNotFoundServiceError(f"Product not found: {product_id}")

    product = product_repository.read_one(product_id)
    if product is not None:
        return product
    raise ProductNotFoundServiceError(f"Product not found: {product_id}")


def get_all_products() -> List[Product]:
    """Retrieves all active product objects from the data repository matrix."""
    return product_repository.read_all()


def update_product(product: Product) -> None:
    """Fixes Bug #5: Guard clause against missing or invalid IDs during update pipelines."""
    if product.product_id is None or product.product_id <= 0:
        raise ProductNotFoundServiceError(f"Product not found: {product.product_id}")

    # Fixes Bug #4: Enforce same strict type checks during updates
    _validate_product_types(product)
    try:
        if not product_repository.update_product(product):
            raise ProductNotFoundServiceError(f"Product not found: {product.product_id}")
    except ProductRepositoryError as e:
        raise ProductServiceError(str(e))
    return None


def delete_product(product_id: int) -> None:
    """Fixes Bug #5: Guard clause against invalid IDs during deletion executions."""
    if not isinstance(product_id, int) or product_id <= 0:
        raise ProductNotFoundServiceError(f"Product not found: {product_id}")

    if not product_repository.delete_product(product_id):
        raise ProductNotFoundServiceError(f"Product not found: {product_id}")
    return None

