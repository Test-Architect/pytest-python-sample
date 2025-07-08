"""
conftest.py - Shared fixtures for Selenium WebDriver and logging setup.

This module contains fixtures that are used for setting up a Selenium WebDriver for testing web applications,
as well as configuring a logger for recording test logs. These fixtures can be used across multiple test files
in the same project.

Fixtures:
    - chrome_driver_setup: Sets up a headless Chrome WebDriver instance.
    - logger_setup: Configures a logger for capturing debug-level logs into a file.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import logging

@pytest.fixture
def chrome_driver_setup():
    """
    Fixture for setting up a headless Chrome WebDriver instance.

    This fixture initializes a Chrome WebDriver using the WebDriver Manager to handle the
    driver installation. It configures the driver to run in headless mode and includes an
    option to keep the browser open for debugging purposes.

    Returns:
       WebDriver: An instance of Selenium's Chrome WebDriver.
    """
    service = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture
def logger_setup():
    """
    Fixture for setting up a logger to capture and store logs during tests.

    This fixture creates a logger instance configured to write logs to a file named 'test_third.log'.
    The logs are formatted with timestamps, logger names, log levels, and messages. The logger is
    set to capture all logs at the DEBUG level or higher.

    Returns:
        Logger: A configured logging.Logger instance.
    """
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler('../test_third.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)
    return logger
