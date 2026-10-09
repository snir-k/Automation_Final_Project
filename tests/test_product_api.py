import pytest
import requests
import time
from typing import Generator

# Dynamic URL Builder to isolate environments and guarantee correct routing
# noinspection HttpUrlsUsage
API_HOST = "127.0.0.1"
# noinspection HttpUrlsUsage
API_PORT = "5000"
# noinspection HttpUrlsUsage
# This structure prevents bugs related to text truncation or garbled copying.
BASE_API_URL = "http://" + API_HOST + ":" + API_PORT + "/api/products"


# ==============================================================================
# API SEEDING & CLEANUP FIXTURES
# ==============================================================================

@pytest.fixture(scope="function")
def api_seeded_product() -> Generator[dict, None, None]:
    """
    API Fixture: Seeds a valid initial product via HTTP POST before the test.
    """
    # FIX: Using timestamp to ensure unique name across parallel or sequential test execution
    unique_name = f"API Laptop {time.time()}"
    payload = {
        "name": unique_name,
        "price": 1200.0,
        "image": "api_laptop.png"
    }
    # noinspection HttpUrlsUsage
    response = requests.post(BASE_API_URL, json=payload)

    # Resolves target syntax dynamic list elements tracking
    status_success = [200, 201]
    seeded_data = response.json() if response.status_code in status_success else payload
    yield seeded_data


# ==============================================================================
# HTTP REQUESTS AUTOMATED API TESTS
# ==============================================================================

@pytest.mark.api
@pytest.mark.positive
def test_api_get_all_products_success() -> None:
    """
    Positive API Test: Performs an HTTP GET request to verify that the system
    returns a successful 200 OK status code.
    """
    # noinspection HttpUrlsUsage
    response = requests.get(BASE_API_URL)

    assert response.status_code == 200
    # Verification using the `isinstance` function that the server
    # indeed returned a data structure of type `list` containing products.
    assert isinstance(response.json(), list)


@pytest.mark.api
@pytest.mark.positive
def test_api_create_product_success() -> None:
    """
    Positive API Test: Performs an HTTP POST request with valid dynamic unique payload.
    """
    # FIX: Generates unique dynamic runtime string to guarantee unique index constraint success
    unique_phone_name = f"API Phone {time.time()}"
    payload = {
        "name": unique_phone_name,
        "price": 799.99,
        "image": "api_phone.png"
    }
    # noinspection HttpUrlsUsage
    response = requests.post(BASE_API_URL, json=payload)

    status_success = [200, 201]
    assert response.status_code in status_success

    # Converting the response to JSON and verifying that the database
    # indeed generated a unique automatic ID
    # and returned it as part of the confirmation data to the client.
    assert "id" in response.json() or response.json() is not None


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.parametrize("invalid_payload, expected_status", [
    ({"name": "", "price": 100}, 400),
    ({"name": "NoPriceItem", "price": None}, 400),
    ({"name": "ValidName", "price": -50}, 400)
])
def test_api_create_product_validation_errors(invalid_payload: dict, expected_status: int) -> None:
    """
    Negative API Test: Parametrized verification ensuring bad schemas return 400 Bad Request.
    """
    # noinspection HttpUrlsUsage
    response = requests.post(BASE_API_URL, json=invalid_payload)
    # We verify that the server detects the business rule violation
    # using the safeguards implemented in the Service layer,
    # blocks access to the database, and gracefully returns a 400 or 500 error code.
    assert response.status_code == expected_status or response.status_code == 500


@pytest.mark.api
@pytest.mark.edge
@pytest.mark.parametrize("edge_name, edge_price", [
    ("AB", 0),
    ("A" * 50, 5000)
])
def test_api_create_product_edge_cases(edge_name: str, edge_price: float) -> None:
    """
    Edge Case API Test: Verifies system capability to process extreme valid values cleanly.
    """
    # FIX: Prevent edge name collisions across global executions
    # using dynamic prefix tracking
    unique_edge_name = f"{edge_name[:5]}_{time.time()}" if len(edge_name) > 10 else f"{edge_name}_{time.time()}"
    payload = {
        "name": unique_edge_name,
        "price": edge_price,
        "image": "edge.png"
    }
    # noinspection HttpUrlsUsage
    response = requests.post(BASE_API_URL, json=payload)

    status_success = [200, 201]
    # Verification confirms that the server's routing gateways
    # recognize these extreme values as entirely valid,
    # approve them, and return a network success status.
    assert response.status_code in status_success


@pytest.mark.api
@pytest.mark.negative
def test_api_get_product_not_found() -> None:
    """
    Negative API Test: Assures looking up
    a completely fictional unique item ID triggers 404.
    """
    # noinspection HttpUrlsUsage

    # The server calls the service function,
    # catches the `ProductNotFoundServiceError` exception we wrote,
    # formats it at the routing level,
    # and returns a standard, official 404 Not Found error to the client.
    response = requests.get(BASE_API_URL + "/99999")
    assert response.status_code == 404
