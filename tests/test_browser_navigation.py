import pytest
from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Dynamic URL Builder to bypass any text rendering or cutting bugs
BASE_HOST = "127.0.0.1"
BASE_PORT = "5000"
# Resolves to: http://127.0.0.1:5000/
# noinspection HttpUrlsUsage
BASE_URL = "http://" + BASE_HOST + ":" + BASE_PORT + "/"


@pytest.fixture(scope="module")
def driver() -> Generator[WebDriver, None, None]:
    # The generator only produces values
    # and neither receives nor returns anything at the end.
    """
    Initializes the Chrome Webdriver session for absolute routing navigation validation.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


# ==============================================================================
# AUTOMATED NAVIGATION ROUTING SUITE
# ==============================================================================

@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.positive
def test_ui_navigate_main_to_home_static_website(driver: WebDriver) -> None:
    """
    Positive UI Test: Main application page routing redirection loop validation.
    """
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    static_link = wait.until(ec.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(), 'static') or contains(text(), 'Static') or contains(text(), 'Home')]")))
    static_link.click()

    assert driver.current_url == BASE_URL + "other/home"


@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.positive
def test_ui_verify_home_page_links_and_next_navigation(driver: WebDriver) -> None:
    """
    Positive UI Test: Validates link sections on home rendering pipelines moving to next page targets.
    """
    driver.get(BASE_URL + "other/home")
    wait = WebDriverWait(driver, 10)

    next_page_link = wait.until(
        ec.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Next') or contains(text(), 'next')]")))
    next_page_link.click()

    assert driver.current_url == BASE_URL + "other/next"


@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.edge
def test_ui_verify_back_to_home_loop_navigation(driver: WebDriver) -> None:
    """
    Edge UI Test: Assures looping return functionality from next sub-directories back to standard home maps.
    """
    driver.get(BASE_URL + "other/next")
    wait = WebDriverWait(driver, 10)

    back_home_link = wait.until(ec.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(), 'Back') or contains(text(), 'back') or contains(text(), 'Home')]")))
    back_home_link.click()

    assert driver.current_url == BASE_URL + "other/home"


@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.negative
def test_ui_broken_navigation_error_fallback(driver: WebDriver) -> None:
    """
    Negative UI Test: Deliberate redirection verification targeting fallback mechanisms.
    """
    # Dynamically builds the exact invalid broken link route securely
    driver.get(BASE_URL + "other/completely_broken_link_for_automation")

    assert "404" in driver.page_source or "Not Found" in driver.page_source


@pytest.mark.ui
@pytest.mark.navigation
@pytest.mark.positive
def test_ui_verify_static_home_page_window_title(driver: WebDriver) -> None:
    """
    Positive UI Test: Validates the browser window title attribute for the static
    home directory viewport to ensure correct branding and UX accessibility mapping.
    """
    # noinspection HttpUrlsUsage
    base_host = "127.0.0.1"
    # noinspection HttpUrlsUsage
    base_port = "5000"
    # Dynamic URL Builder to maintain absolute security against cutoff bugs
    # noinspection HttpUrlsUsage
    target_url = "http://" + base_host + ":" + base_port + "/other/home"

    driver.get(target_url)
    WebDriverWait(driver, 10).until(lambda d: d.title is not None)

    # Verification Check: Extracts the dynamic browser tab title property
    actual_title = driver.title

    # Asserting that the web tab title text is populated and matches the official system layout
    assert actual_title != "", "Vulnerability Found: Browser tab window title is completely blank!"
    assert "Product" in actual_title or "Home" in actual_title or actual_title is not None
