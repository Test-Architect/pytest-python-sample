"""
Module: test_gallery

Description:
This module contains automated test scenarios for the CarSphere application, focusing on:
1. GUI elements and redirection testing for the CarSphere gallery.
2. User reviews functionality, including manual reviews and AI-generated reviews.

Key Areas Tested:
- **Main Page Background**: Ensures that the website background image is correct.
- **Branding and Social Links**: Verifies proper URL redirection for branding and LinkedIn icons.
- **User Reviews**: Tests user ability to add manual reviews and validate the AI-generated reviews functionality.

Test Classes:
1. `TestGUIAndRedirections`:
   - Tests GUI components and icon-based redirections (Scenarios 16-18).
2. `TestReviews`:
   - Tests user manual reviews and AI-generated reviews submission (Scenarios 19-20).

Test Scenarios:
- **Scenario_16**: Validate main page background image.
- **Scenario_17**: Validate the CarSphere branding icon redirection URL.
- **Scenario_18**: Validate LinkedIn icon redirection.
- **Scenario_19**: Test user manual review submission and its visibility.
- **Scenario_20**: Test AI review generation and submission functionality.

Fixtures:
- `chrome_driver_setup`: Provides a configured Chrome WebDriver for browser automation.
- `logger_setup`: Provides a logger instance for logging test execution details.

Preconditions:
- The CarSphere application must be running and accessible at the predefined URL.
- Chrome WebDriver must be installed and configured for Selenium.
- User accounts (e.g., admin and regular users) must exist in the system.
- AI review generation service must be functional for Scenario 20.

Usage:
Run the tests using pytest:
```bash
    pytest test_gallery.py
"""
import random
import string
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.dashboard_page import DashboardPage

@pytest.mark.usefixtures("chrome_driver_setup", "logger_setup")
class TestGUIAndRedirections:
    """
    Test Class: TestGUIAndRedirections

    This class groups all GUI-related tests and redirection validations for the CarSphere application.
    It focuses on verifying the correct appearance, behavior, and functionality of graphical elements on the Cars gallery page,
    ensuring a consistent user experience and proper navigation behavior.

    Key Objectives:
    1. Validate the main page background image to ensure it matches the expected design.
    2. Test branding icon functionality, ensuring it redirects correctly to the application's Home Page.
    3. Verify the LinkedIn icon redirection, confirming it navigates to the correct LinkedIn profile.

    Test Scenarios:
    - **Scenario_16**: Verify that the main page background image is displayed correctly.
    - **Scenario_17**: Validate that the CarSphere branding icon redirects to the Home Page.
    - **Scenario_18**: Confirm that the LinkedIn icon redirects to the 'Israel-Wasserman' LinkedIn profile.

    Fixtures:
    - `chrome_driver_setup`: Provides a Selenium Chrome WebDriver instance for browser automation.
    - `logger_setup`: Provides a logger instance for recording detailed test execution steps and results.

    Preconditions:
    - The CarSphere application must be running and accessible at the predefined URL.
    - Chrome WebDriver must be installed and configured for Selenium.
    - Proper internet access to validate external links (e.g., LinkedIn).

    Execution:
    Run the tests using pytest with the following markers:
    - **smoke**: For quick checks on GUI appearance (Scenario 16).
    - **system** and **functional**: For redirection and link functionality validation (Scenarios 17 and 18).
    """

    """Scenario_16"""
    @pytest.mark.smoke
    @pytest.mark.gui
    def test_016_main_page_background(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_016_main_page_background

        Test Description:
        This test verifies that the main website background image is displayed correctly on the CarSphere homepage.
        The test navigates to the homepage, retrieves the `background-image` CSS property, and compares it with the expected image URL.

        Test Steps:
        1. Open the CarSphere homepage in a Chrome browser.
        2. Maximize the browser window to ensure full visibility.
        3. Retrieve the CSS `background-image` property of the `<body>` element.
        4. Compare the retrieved background image URL to the expected URL.

        Assertions:
        - The background image URL matches the predefined expected URL.

        Preconditions:
        - The CarSphere application must be running and accessible at the predefined URL.
        - Chrome browser and WebDriver must be available for test execution.

        Parameters:
        :param chrome_driver_setup: Fixture that provides a configured Chrome WebDriver instance.
        :param logger_setup: Fixture that provides a logger instance for recording test execution logs.

        Test Results:
        - On Success: Logs indicate that the background image matches the expected URL, and the test passes.
        - On Failure: Logs the discrepancy in the background image and raises an `AssertionError`.

        :return: None. The test performs assertions and logs results.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        dashboard_page = DashboardPage(driver)

        dashboard_page.navigate_to_home_page()

        # Maximize window
        driver.maximize_window()

        # Get the main background image of the dashboard page
        logger.info("Getting the main background image of the dashboard page")
        dashboard_page_background_image = dashboard_page.get_main_background_image()
        logger.info(f"Main background image: {dashboard_page_background_image}")

        # Validate the main background image of the dashboard page
        logger.info("Validating the main background image of the dashboard page")
        assert dashboard_page_background_image == 'url("https://carsphere.onrender.com/static/background_image/background_showroom.jpg")', \
            "Main background image of the dashboard page is wrong. Expected - 'url(\"https://carsphere.onrender.com/static/background_image/background_showroom.jpg\")'"
        logger.info("Main background image of the dashboard page is correct")

        logger.info("Scenario_16 Passed")


    """Scenario_17"""
    @pytest.mark.system
    @pytest.mark.functional
    def test_017_branding_link(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_017_branding_link

        Test Description:
        This test verifies that the CarSphere branding image displays the correct source URL and ensures its functionality
        by validating that the branding icon links to the expected image location.

        Test Steps:
        1. Open the CarSphere homepage in a Chrome browser.
        2. Locate the branding icon element using its class name.
        3. Retrieve the `src` attribute (URL) of the branding icon.
        4. Compare the retrieved URL to the predefined expected branding image URL.

        Assertions:
        - The branding icon's source URL matches the expected image URL.

        Preconditions:
        - The CarSphere application must be running and accessible at the predefined URL.
        - Chrome browser and WebDriver must be available for test execution.

        Parameters:
        :param chrome_driver_setup: Fixture that provides a configured Chrome WebDriver instance for browser automation.
        :param logger_setup: Fixture that provides a logger instance for logging the test execution steps and results.

        Test Results:
        - On Success: Logs confirm that the branding icon's source matches the expected URL, and the test passes.
        - On Failure: Logs the discrepancy in the branding icon URL and raises an `AssertionError`.

        :return: None. The test validates the branding link and logs the outcome.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrom web driver' setup success")

        # Use POM page
        dashboard_page = DashboardPage(driver)

        dashboard_page.navigate_to_home_page()

        # Maximize window
        driver.maximize_window()

        # Validate the CarSphere branding icon redirection URL (shall be redirected to Home Page)
        branding_icon_url = dashboard_page.get_branding_icon_url()
        logger.info(f"Branding icon URL: {branding_icon_url}")

        # Validate the CarSphere branding icon redirection URL (shall be redirected to Home Page)
        assert branding_icon_url == "https://carsphere.onrender.com/static/background_image/branding.png", \
            "Branding icon URL is wrong. Expected - 'https://carsphere.onrender.com/static/background_image/branding.png'"
        logger.info("Branding icon URL is correct")

        logger.info("Scenario_17 Passed")

        
    """Scenario_18"""
    @pytest.mark.system
    @pytest.mark.functional
    def test_018_linkedin_icon_link(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_018_linkedin_icon_link

        Test Description:
        This test verifies that the LinkedIn icon on the CarSphere homepage redirects to the correct LinkedIn profile
        ("Israel-Wasserman" profile). The test ensures that the LinkedIn icon link functions properly.

        Test Steps:
        1. Open the CarSphere homepage in a Chrome browser.
        2. Locate the LinkedIn icon element using its XPath.
        3. Click the LinkedIn icon to open the redirection URL in a new browser tab.
        4. Switch to the new browser tab and retrieve the current URL.
        5. Verify that the URL contains the expected profile identifier: "israel-wasserman".

        Assertions:
        - The current URL in the new tab contains the expected LinkedIn profile identifier.

        Preconditions:
        - The CarSphere application must be running and accessible at the predefined URL.
        - Chrome browser and WebDriver must be available for test execution.
        - The LinkedIn profile link must be active and functional.

        Parameters:
        :param chrome_driver_setup: Fixture that provides a configured Chrome WebDriver instance for browser automation.
        :param logger_setup: Fixture that provides a logger instance for logging test execution details.

        Test Results:
        - On Success: Logs confirm that the LinkedIn icon redirects to the expected LinkedIn profile, and the test passes.
        - On Failure: Logs the discrepancy in the URL and raises an `AssertionError`.

        :return: None. The test validates LinkedIn icon functionality and logs the outcome.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        dashboard_page = DashboardPage(driver)

        dashboard_page.navigate_to_home_page()

        # Maximize window
        driver.maximize_window()

        # Navigate to the LinkedIn icon redirection URL and get the current URL
        logger.info("Validating that the LinkedIn icon redirection URL redirects to 'Israel Wasserman' LinkedIn profile")
        current_linkedin_url = dashboard_page.navigate_to_linkedin_page_and_get_current_url()
        logger.info(f"Current LinkedIn URL: {current_linkedin_url}") 
        
        # Validate that the LinkedIn icon redirection URL redirects to 'Israel Wasserman' LinkedIn profile
        assert "israel-wasserman" in current_linkedin_url, \
            "LinkedIn icon redirection URL is wrong. Expected - 'israel-wasserman'"
        logger.info("LinkedIn icon redirection URL is correct")
        logger.info("Scenario_18 Passed")


@pytest.mark.usefixtures("chrome_driver_setup", "logger_setup")
class TestReviews:
    """This class groups the users review testing (Manual review and AI review)"""

    """Scenario_19"""
    @pytest.mark.sanity
    @pytest.mark.functional
    def test_019_user_manual_review(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_019_user_manual_review

        Test Description:
        This test verifies that a user can successfully submit a manual review for a car and ensures the review appears in the
        'Users Review' section of the CarSphere application.

        Test Steps:
        1. Open the CarSphere homepage in a Chrome browser.
        2. Log in to the application using valid user credentials.
        3. Navigate to the car catalog and select the last car in the list.
        4. Submit a manual review with randomly generated text.
        5. Verify that a success message is displayed confirming the review submission.
        6. Ensure the newly submitted review appears in the 'Users Review' section.

        Assertions:
        1. The success message confirms that the review was successfully added.
        2. The review text appears correctly in the 'Users Review' area, matching the submitted content.

        Preconditions:
        - The CarSphere application must be running and accessible at the predefined URL.
        - Chrome browser and WebDriver must be available for test execution.
        - A user account with valid credentials (e.g., `user3`) must exist in the system.

        Parameters:
        :param chrome_driver_setup: Fixture that provides a configured Chrome WebDriver instance for browser automation.
        :param logger_setup: Fixture that provides a logger instance for logging test execution details.

        Test Results:
        - On Success: Logs confirm that the review was successfully submitted and appears in the 'Users Review' area.
        - On Failure: Logs detail the failure in review submission or visibility and raise an `AssertionError`.

        :return: None. The test validates manual review functionality and logs the outcome.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrom web driver' setup success")

        # Use POM page
        dashboard_page = DashboardPage(driver)
        dashboard_page.navigate_to_home_page()

        # Maximize window
        driver.maximize_window()
        # Loggin-in as a regular user
        dashboard_page.navigate_to_login_page()
        dashboard_page.login("user3", "user3")
        # Navigate the the last car(element) in the Cars gallery 
        dashboard_page.navigate_to_last_car_in_catalog()
        logger.info("Navigated to the last car in the Cars gallery")
        
        # Generate a manual user review input
        manual_review_input = "Auto Manual Review" + ''.join(random.choices(string.digits, k=3))
        logger.info(f"Manual review input: {manual_review_input}")

        # Add manual review and submit
        dashboard_page.add_manual_review(manual_review_input)

        # Assertion_1: Validate that review successfully submitted
        logger.info("Assertion_1: Validate that review successfully submitted")
        assert dashboard_page.get_success_message() == "Review added successfully!", \
            "Review do not added. Expected - review shall be added\nFirst part of Scenario_19 Failed"
        logger.info("Review added successfully")

        # Assertion_2: Validate that review appears in the 'Users Review' list
        logger.info("Assertion_2: Validate that review appears in the 'Users Review' area")
        assert dashboard_page.get_user_new_review() == f"user3: {manual_review_input}",\
            "user new review do not appears in the 'Users Review' area"
        logger.info("Review appears in the 'Users Review' area")
        logger.info("Scenario_19 Passed")


    """Scenario_20"""
    @pytest.mark.integration
    @pytest.mark.functional
    def test_020_user_ai_review(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_020_user_ai_review

        Test Description:
        This test verifies that a user can generate and submit a review using the AI review generation option
        in the CarSphere application. It ensures that the AI-generated review is successfully created and added to the system.

        Test Steps:
        1. Open the CarSphere homepage in a Chrome browser.
        2. Log in to the application using valid user credentials.
        3. Navigate to the car catalog and select the last car in the list.
        4. Click on the "AI Review" button to trigger the AI review generation process.
        5. Wait for the AI-generated review to populate the input field.
        6. Submit the generated review.
        7. Verify the success message confirming that the review was successfully added.

        Assertions:
        1. Validate that the AI review input field is populated with generated content (non-empty).
        2. Confirm that the success message indicates the review was successfully submitted.

        Preconditions:
        - The CarSphere application must be running and accessible at the predefined URL.
        - Chrome browser and WebDriver must be available for test execution.
        - A user account with valid credentials (e.g., `user3`) must exist in the system.
        - The AI review generation service must be functional and return a response within the timeout window.

        Parameters:
        :param chrome_driver_setup: Fixture that provides a configured Chrome WebDriver instance for browser automation.
        :param logger_setup: Fixture that provides a logger instance for logging test execution steps and results.

        Test Results:
        - On Success:
          - The AI-generated review is displayed in the input field.
          - The review submission success message is displayed, confirming successful addition of the review.
        - On Failure:
          - Logs detail issues with AI review generation or submission, and the test raises an `AssertionError`.

        :return: None. The test validates AI-generated review functionality and logs the outcome.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        dashboard_page = DashboardPage(driver)
        dashboard_page.navigate_to_login_page()
        # Loggin-in as a regular user
        dashboard_page.login("user3", "user3")
        # Navigate the the last car(element) in the Cars gallery 
        dashboard_page.navigate_to_last_car_in_catalog()
        # Maximize window
        driver.maximize_window()
        # Generate AI review by clicking on the "AI Review" button
        generated_ai_review = dashboard_page.get_ai_review_by_clicking_ai_review_button(driver)
        logger.info(f"Generated AI review returned from external service: {generated_ai_review}")
        # Assertion_1: Validate that AI review (from external API) generated successfully
        logger.info("Assertion_1: Validate that AI review (from external AI API) generated successfully")
        assert generated_ai_review != "" or "Sorry, could not generate a review at this time.", "Failed to generate AI review"
        logger.info("AI review successfully generated")

        # Assertion_2: Validate that AI review successfully submitted
        logger.info("Assertion_2: Validate that AI review successfully submitted")
        dashboard_page.submit_ai_review()
        success_message = dashboard_page.get_success_message()

        assert success_message == "Review added successfully!", "AI review failed to be submitted"
        logger.info("Review added successfully")

        logger.info("Scenario_20 Passed")