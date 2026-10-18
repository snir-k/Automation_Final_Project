import pytest
import time
# Imports your actual Flask app instance from the root folder
from app import app

@pytest.fixture
def client():
    """Configures a native Flask test client instance to evaluate API endpoints."""
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client

@pytest.mark.api
@pytest.mark.positive
@pytest.mark.xray(test_key="KAN-1")
def test_api_get_all_products(client):
    """Verifies that the GET endpoint successfully fetches the active product catalog."""
    response = client.get('/api/products')
    assert response.status_code == 200
    assert response.is_json

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-2")
@pytest.mark.parametrize("invalid_price", [-10.50, -100, -55.20])
def test_api_create_product_negative_price(client, invalid_price):
    """Verifies that the API blocks mutations containing negative price boundaries."""
    payload = {
        "name": f"API Price Gate {time.time()}",
        "price": str(invalid_price),
        "image": "test.png"
    }
    # Leverages native content_type parameters to force correct multipart boundaries
    response = client.post('/api/products', data=payload, content_type='multipart/form-data')
    assert response.status_code == 400

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-3")
@pytest.mark.parametrize("corrupt_price", ["abc", "one_hundred", "100$", "bad_val", "invalid"])
def test_api_create_product_bug16_string_price(client, corrupt_price):
    """FIXES BUG #16: Verifies that non-numeric price casting strings return a safe 400 Bad Request."""
    payload = {
        "name": f"API Bug16 Test {time.time()}",
        "price": corrupt_price,
        "image": "test.png"
    }
    response = client.post('/api/products', data=payload, content_type='multipart/form-data')
    assert response.status_code == 400

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-4")
@pytest.mark.parametrize("invalid_image", [" ", "   ", "uploads/", "bad.exe", "script.sh"])
def test_api_create_product_bug11_whitespace_image(client, invalid_image):
    """FIXES BUG #11: Verifies that whitespaces inside image field parameter targets are rejected."""
    payload = {
        "name": f"API Bug11 Image Test {time.time()}",
        "price": "150.00",
        "image": invalid_image
    }
    response = client.post('/api/products', data=payload, content_type='multipart/form-data')
    assert response.status_code == 400

