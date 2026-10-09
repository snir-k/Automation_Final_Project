import pytest
# Generator: We want to explicitly specify what the function yields,
# what it can receive (via `.send()`),
# and what it returns upon completion.
from typing import Generator
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec  # Fixes non-lowercase warning

# noinspection HttpUrlsUsage
BASE_HOST = "127.0.0.1"
# noinspection HttpUrlsUsage
BASE_PORT = "5000"
# noinspection HttpUrlsUsage
TARGET_URL = "http://" + BASE_HOST + ":" + BASE_PORT + "/other/home"  # Fixes HTTP insecure warning


@pytest.fixture(scope="module")
def driver() -> Generator[WebDriver, None, None]:
    # The generator only produces values
    # and neither receives nor returns anything at the end.
    """
    Initializes the automated Chrome browser instance for forms and elements verification.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


# ==============================================================================
# UI FORM & ELEMENT INTERACTION TESTS
# ==============================================================================

@pytest.mark.ui
@pytest.mark.positive
def test_ui_dropdown_selection_and_submit(driver: WebDriver) -> None:
    """
    Positive UI Test: Dynamic dropdown selection and submission via HTML IDs.
    """
    driver.get(TARGET_URL)
    wait = WebDriverWait(driver, 10)

    dropdown_element = wait.until(ec.presence_of_element_located((By.ID, "city")))
    select_box = Select(dropdown_element)
    select_box.select_by_value("Tel Aviv")

    driver.find_element(By.ID, "first-name").send_keys("John")
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    driver.find_element(By.ID, "email").send_keys("john@example.com")
    driver.find_element(By.ID, "mobile").send_keys("12345678")

    submit_btn = driver.find_element(By.ID, "submit-form")
    submit_btn.click()

    assert driver.current_url is not None


@pytest.mark.ui
@pytest.mark.positive
def test_ui_form_reset_functionality(driver: WebDriver) -> None:
    """
    Positive UI Test: Validates verified input id='reset-form' behavior
    on text fields.
    """
    driver.get(TARGET_URL)
    wait = WebDriverWait(driver, 10)

    text_input = wait.until(ec.presence_of_element_located((By.ID, "first-name")))
    text_input.send_keys("Reset Automation Test")

    reset_btn = wait.until(ec.element_to_be_clickable((By.ID, "reset-form")))
    reset_btn.click()

    assert text_input.get_attribute("value") == ""


@pytest.mark.ui
@pytest.mark.positive
def test_ui_gender_radio_and_profession_checkbox_selection(driver: WebDriver) -> None:
    """
    Positive UI Test: Toggles verified dynamic selection components found in HTML.
    """
    driver.get(TARGET_URL)
    wait = WebDriverWait(driver, 10)

    gender_radio = wait.until(ec.element_to_be_clickable((By.ID, "female")))
    gender_radio.click()

    profession_checkbox = wait.until(ec.element_to_be_clickable((By.ID, "math")))
    profession_checkbox.click()

    assert gender_radio.is_selected() is True
    assert profession_checkbox.is_selected() is True


@pytest.mark.ui
@pytest.mark.edge
def test_ui_download_button_complete_flow_and_ok_confirmation(driver: WebDriver) -> None:
    """
    Edge/Workflow UI Test: Fires the download progress bar, waits until it reaches
    100% and displays the green 'Download Finished! OK' button, clicks OK,
    and verifies that the counter successfully resets back to 0 baseline.
    """
    # noinspection HttpUrlsUsage
    base_host = "127.0.0.1"
    # noinspection HttpUrlsUsage
    base_port = "5000"
    # noinspection HttpUrlsUsage
    target_forms_url = "http://" + base_host + ":" + base_port + "/other/home"

    driver.get(target_forms_url)
    wait = WebDriverWait(driver, 10)

    # Step 1: Click the 'Start Downloading' button to initiate the interval progress
    download_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Downloading')]")))
    download_btn.click()

    # Step 2: Explicitly wait until the progress bar attribute reaches exactly 100
    progress_bar = driver.find_element(By.ID, "download-progress")
    wait.until(lambda d: progress_bar.get_attribute("value") == "100")

    # Step 3: FIX - Locate the confirmation button by its verified exact native onclick event attribute
    ok_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[@onclick='confirmMessage(this)']")))
    ok_button.click()

    # Step 4: Verification Check - Confirm that clicking OK successfully cleared the UI state and reset value to 0
    wait.until(lambda d: progress_bar.get_attribute("value") == "0")
    assert progress_bar.get_attribute(
        "value") == "0", "Vulnerability Found: Clicked OK but progress bar did not reset to 0!"


@pytest.mark.ui
@pytest.mark.positive
def test_ui_insert_text_and_clear_flow(driver: WebDriver) -> None:
    """
    Positive Workflow Test: Handles dynamic popup input fields using switchTo alert handlers.
    """
    driver.get(TARGET_URL)
    wait = WebDriverWait(driver, 10)

    insert_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Insert Text')]")))
    insert_btn.click()

    alert = driver.switch_to.alert
    alert.send_keys("Hello Instructor")
    alert.accept()

    paragraph_element = driver.find_element(By.ID, "text-p")
    assert paragraph_element.text == "Hello Instructor"

    clear_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear')]")
    clear_btn.click()

    assert paragraph_element.text == ""


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.xfail(
    reason="Vulnerability Found: Form inputs persist upon back navigation"
           " (Form Resubmission Bug). Frontend/PRG fix required.")
def test_ui_prevent_duplicate_form_resubmission_on_back_navigation(driver: WebDriver) -> None:
    """
    Negative UI Test: Detects the Form Resubmission Bug. Fills all required fields
    including gender validation parameters, submits, navigates back, and verifies inputs.
    """
    # noinspection HttpUrlsUsage
    base_host = "127.0.0.1"
    # noinspection HttpUrlsUsage
    base_port = "5000"
    # noinspection HttpUrlsUsage
    target_forms_url = "http://" + base_host + ":" + base_port + "/other/home"

    driver.get(target_forms_url)
    wait = WebDriverWait(driver, 10)

    # Step 1: Fully populate required fields
    # AND mandatory gender radio inputs to pass validation
    dropdown = Select(wait.until(ec.presence_of_element_located((By.ID, "city"))))
    dropdown.select_by_value("Tel Aviv")
    driver.find_element(By.ID, "first-name").send_keys("Duplicate")
    driver.find_element(By.ID, "last-name").send_keys("Check")
    driver.find_element(By.ID, "email").send_keys("test_dup@example.com")
    driver.find_element(By.ID, "mobile").send_keys("99999999")

    # FIX: Select mandatory gender radio button container field
    # to unblock submission validation gateway
    gender_radio = driver.find_element(By.ID, "female")
    gender_radio.click()

    # Step 2: Trigger submission to reach the subdirectory next page endpoint
    driver.find_element(By.ID, "submit-form").click()
    # noinspection HttpUrlsUsage
    wait.until(ec.url_contains("/other/next"))

    # Step 3: Trigger Browser Back Navigation to simulate user loop return
    driver.back()
    # noinspection HttpUrlsUsage
    wait.until(ec.url_contains("/other/home"))

    # Step 4: Verification Check - Assert that input fields are blanked out securely
    first_name_input = driver.find_element(By.ID, "first-name")
    assert first_name_input.get_attribute(
        "value") == "", ("Vulnerability Found: Form inputs persisted "
                         "after back routing navigation!")
