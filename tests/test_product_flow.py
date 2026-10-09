from typing import Any
import pytest
from models.models import Product
from repositories import product_repository
from services import product_service


# ==============================================================================
# FIXTURES (Hooks for Setup and Teardown)
# ==============================================================================

@pytest.fixture(autouse=True)
def db_cleaner() -> None:
    """
    Setup & Teardown Hook: Resets the simulated database before every test.
    """
    product_repository.reset_db()


@pytest.fixture
def seeded_product() -> Product:
    """
    Helper Fixture: Seeds a valid product for testing update and delete flows.
    """
    prod = Product(name="Laptop", price=999.99, image="laptop.png")
    product_repository.create_product(prod)
    return prod


# ==============================================================================
# MODULE 1: PRODUCT REPOSITORY TESTS
# ==============================================================================

@pytest.mark.repository
@pytest.mark.positive
def test_repo_create_product_success() -> None:
    prod = Product(name="Smartphone", price=699.0, image="phone.png")
    new_id = product_repository.create_product(prod)
    fetched = product_repository.read_one(new_id)

    assert new_id == 1
    assert prod.product_id == 1
    assert fetched is not None
    assert fetched.name == "Smartphone"


@pytest.mark.repository
@pytest.mark.negative
@pytest.mark.parametrize("name, price, expected_err", [
    (None, 100.0, "Column cannot be null"),
    ("A" * 51, 100.0, "Product name too long"),
    ("ValidName", None, "Column cannot be null")
])
def test_repo_create_product_constraints(name: str | None, price: float | None, expected_err: str) -> None:
    prod = Product(name=name, price=price, image="img.png")
    # pytest.raises: verifies the code blocks the operation and throws a Repository exception
    with pytest.raises(product_repository.ProductRepositoryError) as exc_info:
        product_repository.create_product(prod)
    assert expected_err in str(exc_info.value)


@pytest.mark.repository
@pytest.mark.negative
def test_repo_create_duplicate_name_error(seeded_product: Product) -> None:
    duplicate_prod = Product(name="Laptop", price=450.0, image="another.png")
    with pytest.raises(product_repository.ProductRepositoryError) as exc_info:
        product_repository.create_product(duplicate_prod)
    assert "Product name exists" in str(exc_info.value)


@pytest.mark.repository
@pytest.mark.positive
def test_repo_read_one_found_and_not_found(seeded_product: Product) -> None:
    assert seeded_product.product_id is not None  # Guard: Clears 'int | None' warning
    found = product_repository.read_one(seeded_product.product_id)
    not_found = product_repository.read_one(999)

    assert found is not None
    assert found.name == "Laptop"
    assert not_found is None


@pytest.mark.repository
@pytest.mark.positive
def test_repo_read_all_empty_and_populated() -> None:
    assert product_repository.read_all() == []
    product_repository.create_product(Product(name="Item1", price=10.0))
    assert len(product_repository.read_all()) == 1


@pytest.mark.repository
@pytest.mark.positive
def test_repo_update_product_success(seeded_product: Product) -> None:
    assert seeded_product.product_id is not None  # Guard: Clears 'int | None' warning
    seeded_product.name = "Ultra Laptop"
    result = product_repository.update_product(seeded_product)
    fetched = product_repository.read_one(seeded_product.product_id)

    assert result is True
    assert fetched is not None
    assert fetched.name == "Ultra Laptop"


@pytest.mark.repository
@pytest.mark.negative
def test_repo_update_product_not_found() -> None:
    ghost_product = Product(product_id=888, name="Ghost", price=50.0)
    result = product_repository.update_product(ghost_product)
    assert result is False


# ==============================================================================
# MODULE 2: PRODUCT SERVICE TESTS (Including Type, Error & Edge Cases)
# ==============================================================================

@pytest.mark.service
@pytest.mark.positive
def test_service_add_product_success() -> None:
    prod = Product(name="Tablet", price=299.99, image="tablet.png")
    new_id = product_service.add_product(prod)
    assert new_id == 1


@pytest.mark.service
@pytest.mark.negative
@pytest.mark.parametrize("name, price, expected_msg", [
    ("A", 100.0, "Product name must be at least 2 characters long."),
    ("Valid", -5.0, "Product price must be positive."),
    ("", 20.0, "Product name must be at least 2 characters long."),
    ("Valid", None, "Product price must be positive.")
])
def test_service_add_product_input_validation(name: str, price: float | None, expected_msg: str) -> None:
    prod = Product(name=name, price=price)
    with pytest.raises(product_service.ProductServiceError) as exc_info:
        product_service.add_product(prod)
    assert str(exc_info.value) == expected_msg


@pytest.mark.service
@pytest.mark.edge
@pytest.mark.parametrize("name, price", [
    ("AB", 0),
    ("A" * 50, 1000)
])
def test_service_add_edge_cases(name: str, price: float) -> None:
    prod = Product(name=name, price=price)
    new_id = product_service.add_product(prod)
    assert new_id > 0


@pytest.mark.service
@pytest.mark.types
@pytest.mark.parametrize("bad_name, bad_price", [
    (12345, 100),
    ("Valid", "Free"),
    (True, False)
])
def test_service_invalid_types(bad_name: Any, bad_price: Any) -> None:
    """
    Type Safety Testing: Ensures the service layer rejects or handles unexpected types properly.
    """
    prod = Product(name=bad_name, price=bad_price)  # type: ignore
    with pytest.raises((product_service.ProductServiceError, TypeError)):
        product_service.add_product(prod)


@pytest.mark.service
@pytest.mark.negative
def test_service_get_product_not_found() -> None:
    with pytest.raises(product_service.ProductNotFoundServiceError):
        product_service.get_product(999)


@pytest.mark.service
@pytest.mark.positive
def test_service_update_product_success(seeded_product: Product) -> None:
    assert seeded_product.product_id is not None  # Guard: Clears 'int | None' warning
    seeded_product.name = "New Laptop Name"
    product_service.update_product(seeded_product)
    assert product_service.get_product(seeded_product.product_id).name == "New Laptop Name"


@pytest.mark.service
@pytest.mark.positive
def test_service_delete_product_flow(seeded_product: Product) -> None:
    assert seeded_product.product_id is not None  # Guard: Clears 'int | None' warning
    product_service.delete_product(seeded_product.product_id)
    with pytest.raises(product_service.ProductNotFoundServiceError):
        product_service.get_product(seeded_product.product_id)


@pytest.mark.repository
@pytest.mark.negative
def test_repo_create_product_invalid_image_type() -> None:
    """
    Negative Test: Validates that passing an invalid data type (e.g., int/dict)
    as the image path behaves safely or throws a database connection wrapper error
    if strictly checked by types.
    """
    # Using an integer instead of a string path for image attribute
    invalid_img_prod = Product(name="ImageTypeErrorItem", price=99.9, image=12345)  # type: ignore

    # In a real dynamic database or strict orm configuration, this should either fail gracefully
    # or be caught by validation. We ensure the creation handles it safely or raises proper constraints.
    try:
        new_id = product_repository.create_product(invalid_img_prod)
        assert new_id > 0
    except product_repository.ProductRepositoryError:
        # Pass smoothly if the repository constraint catches it
        pass


@pytest.mark.service
@pytest.mark.negative
@pytest.mark.parametrize("malformed_image", [
    [],  # Empty List passed as image path
    {},  # Dict passed as image path
    True  # Boolean passed as image path
])
def test_service_malformed_image_type_handling(malformed_image: Any) -> None:
    """
    Negative Test: Verifies the service layer resilience when receiving highly unexpected
    data types inside the product image attribute.
    """
    prod = Product(name="MalformedImageItem", price=50.0, image=malformed_image)

    with pytest.raises((product_service.ProductServiceError, TypeError)):
        product_service.add_product(prod)
