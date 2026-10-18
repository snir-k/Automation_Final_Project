import pytest
from unittest.mock import patch, MagicMock
from models.models import Product
from services import product_service # The Business Logic Layer


# ==============================================================================
# UNIT TESTS USING MOCKS (No Database Connections)
# ==============================================================================

@pytest.mark.unit
@pytest.mark.positive
@patch('repositories.product_repository.create_product')
@pytest.mark.xray(test_key="KAN-13")
def test_unit_add_product_success(mock_create: MagicMock) -> None:
    """
    Positive Unit Test: Verifies that a valid product is verified by the service
    and successfully passed to the repository layer using a mocked return value.
    """
    # Configure the mock to simulate a successful database record
    # insertion returning ID 55
    mock_create.return_value = 55


    prod = Product(name="Mocked Item", price=150.0, image="mock.png")
    result_id = product_service.add_product(prod)

    # Assertions to verify the service behaves correctly based on the mock output
    assert result_id == 55
    # A test verifying that the service layer
    # indeed called the repository exactly once.
    mock_create.assert_called_once_with(prod)


@pytest.mark.unit
@pytest.mark.negative
@patch('repositories.product_repository.create_product')
def test_unit_add_product_repository_exception_wrapping(mock_create: MagicMock) -> None:
    """
    Negative Unit Test: Verifies that if the data layer encounters a database error,
    the service successfully catches and wraps it into a ProductServiceError.
    """
    from repositories.product_repository import ProductRepositoryError

    # Configure the mock to raise a custom repository data mapping exception
    mock_create.side_effect = ProductRepositoryError("Database Unique Name Constraint Violated")

    # The executing code must fail and throw a ProductServiceError;
    # if it succeeds, the test will fail.

    # Service call for a product with a dual name.

    # The service calls the mock repository, encounters the wrapped error,
    # catches it, and converts it into a service error.

    prod = Product(name="DuplicateName", price=20.0)
    with pytest.raises(product_service.ProductServiceError) as exc_info:
        product_service.add_product(prod)

    # Verify that the recurring error message indeed
    # contains the precise explanation regarding the uniqueness violation,
    # thereby demonstrating a watertight blocking mechanism.
    assert "Database Unique Name Constraint Violated" in str(exc_info.value)
    mock_create.assert_called_once_with(prod)


@pytest.mark.unit
@pytest.mark.edge
@patch('repositories.product_repository.update_product')
def test_unit_update_product_edge_zero_price(mock_update: MagicMock) -> None:
    """
    Edge Case Unit Test: Validates that the service permits updating a product
    with a precise boundary price value of 0.
    """
    mock_update.return_value = True

    edge_prod = Product(product_id=10, name="Zero Price Item", price=0, image="zero.png")
    # Invoking the update function in the service.
    # The code verifies that the service's gatekeeper
    # approves the zero price, does not throw an error,
    # and successfully passes the request to the mock function.
    product_service.update_product(edge_prod)

    # Final verification that the mock was invoked once with the end product.
    mock_update.assert_called_once_with(edge_prod)

