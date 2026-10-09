import pytest
from typing import Generator
from models.models import Product
from repositories import product_repository


# ==============================================================================
# GLOBAL FIXTURES (Shared across all test modules)
# ==============================================================================

@pytest.fixture(autouse=True)
def db_cleaner() -> Generator[None, None, None]:
    """
    Setup & Teardown Hook: Resets the simulated database before every individual test
    to guarantee isolation and eliminate test-ordering side effects.
    """
    product_repository.reset_db()
    yield  # Runs the actual test function
    # Teardown logic can be safely added here if necessary in the future


@pytest.fixture
def seeded_product() -> Product:
    """
    Data Seeding Fixture: Seeds a valid baseline product into the repository.
    Used cleanly by any test requiring an existing database entity.
    """
    prod = Product(name="Laptop", price=999.99, image="laptop.png")
    product_repository.create_product(prod)
    return prod


# ==============================================================================
# PYTEST HTML REPORT CUSTOMIZATION (Metadata Enhancement)
# ==============================================================================

def pytest_html_report_title(report) -> None:
    """
    Customizes the main headline/title inside the generated HTML report file.
    """
    report.title = "QA Automation Final Project - Product System Integration Tests"


@pytest.hookimpl(tryfirst=True)
def pytest_metadata(metadata: dict) -> None:
    """
    Modifies and injects custom student/project metadata into the HTML report header table.
    """
    # Remove unnecessary environment details to keep the report professional
    metadata.pop("JAVA_HOME", None)
    metadata.pop("Plugins", None)

    # Inject student-specific presentation details
    metadata["Project Name"] = "Product Management System Automation Testing"
    metadata["Student Name"] = "Snir Kanias"
    metadata["Target Layer"] = "Data Repository & Business Logic Integration"
    metadata["Automation Framework"] = "Pytest-HTML Core"
    metadata["Status"] = "Final Submission Ready"
