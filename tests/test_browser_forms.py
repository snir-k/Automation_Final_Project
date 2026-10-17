import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

@pytest.fixture
def driver():
    """Sets up the dynamic Chrome browser instances for automated UI execution loops."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    chrome_driver = webdriver.Chrome(options=options)
    # FIXES ADDRESS BUG: Points directly to the active Flask production port server
    # noinspection HttpUrlsUsage
    chrome_driver.get("http://127.0.0.1:5000")
    yield chrome_driver
    chrome_driver.quit()

@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-9")
def test_ui_validate_bug11_whitespace_name(driver):
    """FIXES BUG #11: Verifies that whitespace names display an inline red error box."""
    driver.find_element(By.ID, "product-name").send_keys("   ")
    driver.find_element(By.ID, "product-price").send_keys("250.00")
    driver.find_element(By.ID, "product-image").send_keys("item.png")
    driver.find_element(By.ID, "submit-btn").click()

    alert_box = WebDriverWait(driver, 5).until(
        ec.visibility_of_element_located((By.ID, "ui-alert-box"))
    )
    assert "Error" in alert_box.text

@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.xray(test_key="KAN-10")
def test_ui_validate_bug12_numeric_overflow_price(driver):
    """FIXES BUG #12: Verifies that numeric overflow prices trigger the local alert threshold."""
    driver.find_element(By.ID, "product-name").send_keys("Overflow Test")
    driver.find_element(By.ID, "product-price").send_keys("9999999999")
    driver.find_element(By.ID, "product-image").send_keys("item.png")
    driver.find_element(By.ID, "submit-btn").click()

    alert_box = WebDriverWait(driver, 5).until(
        ec.visibility_of_element_located((By.ID, "ui-alert-box"))
    )
    assert "Error" in alert_box.text
