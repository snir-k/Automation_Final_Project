import pytest
from models.models import Product
from services import product_service
from services.product_service import ProductServiceError


@pytest.mark.repository
@pytest.mark.service
@pytest.mark.positive
@pytest.mark.xray(test_key="KAN-5")
def test_flow_create_and_read_product(db_cleaner):
    """Verifies complete cycle of product generation and DB auto-increment sequencing."""
    prod = Product(product_id=0, name="Integration Phone", price=899.90, image="phone.png")
    new_id = product_service.add_product(prod)
    assert new_id > 0

    fetched = product_service.get_product(new_id)
    assert fetched.name is not None
    assert fetched.name.startswith("Integration Phone")
    assert fetched.price == 899.90


@pytest.mark.repository
@pytest.mark.service
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-6")
@pytest.mark.parametrize("bad_price", [-1.0, -99.9, -0.01, -500.00, -1200.50])
def test_flow_create_negative_price_boundaries(db_cleaner, bad_price):
    """Fixes Bug #1: Ensures that negative prices are blocked by the service guard clauses."""
    prod = Product(product_id=0, name="Bad Price Board", price=bad_price, image="img.png")
    with pytest.raises(ProductServiceError):
        product_service.add_product(prod)


@pytest.mark.repository
@pytest.mark.service
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-7")
@pytest.mark.parametrize("corrupt_type", [[], {}, (), {"a": 1}, (5,), [1, 2, 3]])
def test_flow_create_type_safety_clash(db_cleaner, corrupt_type):
    """Fixes Bug #4: Ensures arbitrary malformed matrix types trigger dynamic TypeErrors."""
    # noinspection PyTypeChecker
    prod = Product(product_id=0, name="Type Clash", price=corrupt_type, image="img.png")
    with pytest.raises(TypeError):
        product_service.add_product(prod)


@pytest.mark.repository
@pytest.mark.service
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-8")
@pytest.mark.parametrize("dup_index", range(16))
def test_flow_prevent_duplicate_names(db_cleaner, dup_index):
    """Fixes Bug #2: Triggers validation constraints to completely prohibit duplicate item titles."""
    prod = Product(product_id=0, name=f"Unique Token {dup_index}", price=10.0, image="a.png")
    product_service.add_product(prod)

    prod_dup = Product(product_id=0, name=f"Unique Token {dup_index}", price=25.0, image="b.png")
    with pytest.raises(ProductServiceError):
        product_service.add_product(prod_dup)

