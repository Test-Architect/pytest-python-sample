"""
Module: test_auth

Description:
This module contains automated test scenarios for user authentication in the CarSphere application,
including Sign-up, Login, and Logout functionality.
The tests ensure proper behavior of the authentication system for both 'admin' and 'non-admin' users.

Key Functionalities Tested:
1. **Sign-Up**:
   - Registering new users with valid credentials.
   - Preventing registration of existing users.
   - Rejecting mismatched passwords during registration.
2. **Login**:
   - Validating successful login with correct credentials for 'admin' and 'non-admin' users.
   - Ensuring login rejection with incorrect credentials.
3. **Logout**:
   - Verifying that 'admin' and 'non-admin' users can log out successfully.

Test Classes:
1. `TestSignUpUser`:
   - Tests user registration functionality (Scenarios 1-3).
2. `TestLoginUser`:
   - Tests user login functionality for both valid and invalid credentials (Scenarios 4-7).
3. `TestLogoutUsers`:
   - Tests user logout functionality for 'admin' and 'non-admin' users (Scenarios 8-9).

Test Scenarios:
- **Scenario_1**: Sign up a new user with valid credentials.
- **Scenario_2**: Attempt to sign up with an existing username.
- **Scenario_3**: Reject registration when password and confirm password do not match.
- **Scenario_4**: Log in as 'admin' with valid credentials.
- **Scenario_5**: Attempt to log in as 'admin' with invalid credentials.
- **Scenario_6**: Log in as 'non-admin' user with valid credentials.
- **Scenario_7**: Attempt to log in as 'non-admin' user with invalid credentials.
- **Scenario_8**: Log out as 'admin' user.
- **Scenario_9**: Log out as 'non-admin' user.

Fixtures:
- `chrome_driver_setup`: Provides a Selenium Chrome WebDriver instance for browser automation.
- `logger_setup`: Provides a logger instance for recording detailed test execution steps and results.

Preconditions:
- The CarSphere application must be running and accessible at the predefined URL.
- Chrome WebDriver must be installed and configured for Selenium.
- User accounts for 'admin' and 'non-admin' roles must exist where applicable.
- Internet access must be available for API calls (e.g., fetching existing users).

Usage:
Run the tests using pytest with the following command:
```bash
pytest test_auth.py
"""
import string
import random
import time
from selenium.webdriver.common.by import By
import pytest
import requests
import json
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage


@pytest.mark.usefixtures("chrome_driver_setup", "logger_setup")
class TestSignUpUser:
    """
    Test Class: TestSignUpUser

    Description:
    This class groups all automated test scenarios for user sign-up functionality in the CarSphere application.
    The tests validate different aspects of the sign-up process, including successful registration,
    handling of duplicate users, and validation for mismatched passwords.

    Key Test Scenarios:
    1. **Scenario_1**: Test successful sign-up of a new user with valid credentials.
    2. **Scenario_2**: Ensure that signing up with an existing username is rejected.
    3. **Scenario_3**: Validate that the system blocks registration when the password and confirm password fields do not match.

    Test Goals:
    - Verify that users can sign up successfully with valid and unique credentials.
    - Ensure proper error handling and messaging for invalid sign-up attempts.
    - Confirm system behavior for edge cases such as mismatched passwords or duplicate usernames.

    Preconditions:
    - The CarSphere application must be running and accessible at the predefined URL.
    - Chrome browser and WebDriver must be available for test execution.
    - A database of existing users is accessible through an API for validation purposes.

    Fixtures:
    - `chrome_driver_setup`: Initializes and provides a Selenium WebDriver instance for browser automation.
    - `logger_setup`: Provides a logger instance to log detailed information about test execution.

    Test Scenarios:
    - `test_001_signup_new_user`: Validates user registration with random valid credentials.
    - `test_002_signup_existing_user_shall_rejected`: Ensures that duplicate usernames cannot be registered.
    - `test_003_mismatch_confirm_password`: Verifies that mismatched passwords are blocked with appropriate feedback.

    :return: None. The tests perform assertions and log results.
    """

    """Scenario_1."""
    @pytest.mark.sanity
    @pytest.mark.regression
    @pytest.mark.functional
    def test_001_signup_new_user(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_001_signup_new_user

        Description:
        This test verifies that a new user can successfully sign up to the CarSphere application
        using valid and unique credentials. It includes the generation of a random username,
        validation against the database to ensure uniqueness, and confirmation of successful registration.

        Test Steps:
        1. Navigate to the CarSphere home page.
        2. Redirect to the 'Sign Up' page.
        3. Generate a random, unique username by querying existing users from the database.
        4. Populate the sign-up form with:
           - First name
           - Last name
           - Unique username
           - Matching password and confirm password.
        5. Submit the form.
        6. Validate that a success message confirms the registration.

        Assertions:
        - The success message should contain the correct welcome message, indicating successful registration.

        Preconditions:
        - The CarSphere application is running and accessible.
        - The `/get-users` API endpoint is functional and returns existing users.
        - The `Chrome WebDriver` and browser are available for test execution.

        Postconditions:
        - The test generates a new user account with random credentials and appends them to the `users.txt` file.

        Logs and Outputs:
        - Logs details about the random username generation and registration process.
        - On failure, logs the issue and raises an AssertionError.
        - On success, logs a confirmation message.

        Example Success Message:
        "Welcome, QAAuto_FirstName QAAuto_LastName and thanks for registration!"

        :param chrome_driver_setup: Fixture for initializing the Chrome WebDriver.
        :param logger_setup: Fixture for initializing the logger.
        :return: None
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM pages
        register_page = RegisterPage(driver)
        dhasboad = DashboardPage(driver)

        # Navigate to home page
        register_page.navigate_to_home_page()
        logger.info("Redirected to application 'Home Page'")

        # Redirection to 'SignUp' page
        register_page.navigate_to_register_page()
        logger.info("redirect to 'register' page'")

        # Generate new random username and password
        existing_users = register_page.get_users_list_from_api()
        random_username = register_page.generate_new_random_username(existing_users)
        random_password = register_page.generate_new_random_password()
        logger.info(f"new random username created: username: {random_username}, password: {random_password}")

        # Writing the new random username to logger, and also the const password
        logger.info(f"new random username created: username: {random_username}, password: {random_password}")
     
        # Copying the new random 'username' and 'password' into a local 'users.txt' file
        try:
            with open("../users.txt", "a") as users_file:
                users_file.write(f"\nusername: {random_username}, password: {random_password}")
        except Exception as e:
            logger.error(e, "\nAdding the new random username credentials to 'users.txt' file failed")

        # Continue populating the SignUp form and signing-up a new user
        register_page.fill_and_submit_registration_form(first_name="QAAuto_FirstName",
                                             last_name="QAAuto_LastName",
                                              username=random_username,
                                              password=random_password,
                                              confirm_password=random_password)
        success_message = dhasboad.get_success_message()
        assert success_message == """Welcome, QAAuto_FirstName QAAuto_LastName and thanks for registration!\n\n!!! You're already logged-in. Let's Begin !!!""", \
            "Failed to SignUp a new user"
        logger.info("Scenario_1 Passed")


    """Scenario_2."""
    @pytest.mark.regression
    @pytest.mark.functional
    def test_002_signup_existing_user_shall_rejected(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_002_signup_existing_user_shall_rejected

        Description:
        This test verifies that the system correctly rejects a sign-up attempt when using
        an existing username that already exists in the database.
        The test confirms the display of an appropriate error message to inform the user.

        Test Steps:
        1. Navigate to the CarSphere home page.
        2. Redirect to the 'Sign Up' page.
        3. Retrieve a list of existing usernames from the database using the `/get-users` API.
        4. Populate the sign-up form with:
           - First name
           - Last name
           - Existing username
           - Valid password and confirm password.
        5. Submit the form.
        6. Validate that the system rejects the sign-up attempt and displays an error message.

        Assertions:
        - The error message should explicitly state that the username already exists and prompt the user to choose another.

        Expected Error Message:
        "Username '{username}' already exist, please try another username."

        Preconditions:
        - The CarSphere application is running and accessible.
        - The `/get-users` API endpoint is functional and provides a list of existing usernames.
        - Chrome WebDriver and browser are available for automation.

        Postconditions:
        - No changes are made to the user database.
        - The test ensures existing usernames remain unaffected.

        Logs and Outputs:
        - Logs the retrieved list of existing usernames.
        - Logs the username being tested.
        - On failure, logs the issue and raises an `AssertionError`.
        - On success, logs a confirmation message.

        :param chrome_driver_setup: Fixture for initializing the Chrome WebDriver.
        :param logger_setup: Fixture for initializing the logger.
        :return: None
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")
        
        # Use POM page
        register_page = RegisterPage(driver)

        logger.info("redirect to 'register page'")
        register_page.navigate_to_home_page()
        register_page.navigate_to_register_page()

        # selecting any existing 'username' from DB
        existing_usernames = json.loads(requests.get("https://carsphere.onrender.com/get-users").text)
        # print(existing_usernames)
        username = ''
        logger.debug(type(existing_usernames))
        for name in existing_usernames:
            if name != 'admin':
                username = name
                break
        logger.info(f"username: {username}")
        password = "1235"
        logger.info(f"username: {username}\npassword: {password}")
        # Continue populating the Signup form and trying to signing-up an existing username
        register_page.fill_and_submit_registration_form(first_name="QAAuto_FirstName",
                                             last_name="QAAuto_LastName",
                                             username=username,
                                             password=password,
                                             confirm_password=password)
        # register_page.click_signup_button()
        alert_danger = register_page.get_alert_danger_message()
        logger.info(f"alert_danger: {alert_danger}")
        assert (f"Username '{username}' already exist, "
                f"please try another username.") in alert_danger, \
                "Signing-up an existing user shall not be allowed"
        logger.info("Scenario_2 Passed")


    """Scenario_3."""
    @pytest.mark.regression
    @pytest.mark.functional
    def test_003_mismatch_confirm_password(self, chrome_driver_setup, logger_setup):
        """
        Test Scenario: test_003_mismatch_confirm_password

        Description:
        This test verifies that the system blocks user registration when the 'Password'
        and 'Confirm Password' fields do not match. The test checks that the application
        displays an appropriate error message with a visual indication (red text).

        Test Steps:
        1. Navigate to the CarSphere home page.
        2. Redirect to the 'Sign Up' page.
        3. Generate a new random username that does not already exist in the database.
        4. Populate the sign-up form:
           - First Name
           - Last Name
           - Random Username
           - Password (value: "1234")
           - Confirm Password (value: "8888")
        5. Submit the form.
        6. Validate that:
           - An error message "Passwords are not match" is displayed.
           - The error message is displayed in red (`rgba(255, 0, 0, 1)`).

        Assertions:
        - The system should display the correct error message.
        - The error message should appear with the expected visual styling (red color).

        Preconditions:
        - The CarSphere application is running and accessible.
        - The `/get-users` API endpoint is functional for retrieving existing usernames.
        - Chrome WebDriver is available for automation.

        Postconditions:
        - No user is added to the database when passwords do not match.

        Logs and Outputs:
        - Logs the generated random username and mismatched password values.
        - Logs the validation results for error message and styling.
        - On failure, logs the issue and raises an `AssertionError`.

        :param chrome_driver_setup: Fixture for initializing the Chrome WebDriver.
        :param logger_setup: Fixture for initializing the logger.
        :return: None
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        register_page = RegisterPage(driver)

        # Navigate to home page
        register_page.navigate_to_home_page()
        register_page.navigate_to_register_page()
        logger.info("Redirected to 'registration' page")
        
        # Generating a new random 'username' and checking that it do not already included in the DB
        # First: getting a list of all existing usernames from DB
        response = requests.get("https://carsphere.onrender.com/get-users")
        existing_users = response.text
        logger.debug(f"All existing users in DB:\n{existing_users}")
        # Second: Generating a new random username and checking that it is not exist already in DB
        random_username = existing_users[0]
        while random_username in existing_users:
            random_username = "Auto_username" + ''.join(random.choices(string.digits, k=3))
        # Preparing not matches passwords for 'Password' and 'Confirm password' fields
        password_input = "1234"
        confirm_password_input = "8888"
        # Writing the new random username,password,confirm_password to the log.
        logger.info(f"New random username: username:"
                    f" {random_username}, password: {password_input}, confirm_password: {confirm_password_input}")
        # Copying the new random 'username' and 'password' into a local 'users.txt' file
        try:
            with open("../users.txt", "a") as users_file:
                users_file.write(f"\nusername: {random_username}, "
                                 f"password: {password_input}, confirm_password: {confirm_password_input}")
        except Exception as e:
            logger.error(e, "\nAdding the new random username credentials to 'users.txt' file failed")
        # Continue populating the SignUp form and signing-up a new user
        register_page.fill_and_submit_registration_form(first_name="QAAuto_FirstName",
                                             last_name="QAAuto_LastName",
                                             username=random_username,
                                             password=password_input,
                                             confirm_password=confirm_password_input)
        mismatch_password_alert, mismatch_password_alert_expected_color = register_page.get_alert_mismatch_password_message()
        assert mismatch_password_alert == "Passwords are not match", \
            "Failed to display the mismatch password alert"
        assert mismatch_password_alert_expected_color == "rgba(255, 0, 0, 1)", \
            "Failed to display the mismatch password alert in red color"
        logger.info("Scenario_3 Passed")


@pytest.mark.usefixtures("chrome_driver_setup", "logger_setup")
class TestLoginUser:
    """
    Test Class: TestLoginUser

    Description:
    This class contains test cases to verify the functionality of the 'Login' feature in the CarSphere application.
    The tests cover both positive and negative scenarios for 'admin' and 'non-admin' users, ensuring secure
    authentication and appropriate error handling when invalid credentials are provided.

    Key Objectives:
    - Validate successful login with valid credentials for both 'admin' and 'non-admin' users.
    - Ensure login attempts with invalid credentials are rejected with appropriate error messages.
    - Verify application responses for various authentication conditions.

    Test Scenarios:
    - **Scenario_4**: Verify successful login for the 'admin' user using valid credentials.
    - **Scenario_5**: Validate login failure for the 'admin' user with invalid credentials.
    - **Scenario_6**: Verify successful login for a 'non-admin' user using valid credentials.
    - **Scenario_7**: Validate login failure for a 'non-admin' user with invalid credentials.

    Test Flow:
    1. Navigate to the 'Home Page' and redirect to the 'Login' page.
    2. Populate the login form with test credentials:
       - Username
       - Password
    3. Submit the login form and validate system responses:
       - Success message for valid credentials.
       - Error message for invalid credentials.

    Assertions:
    - Correct success message is displayed for successful logins.
    - Correct error message is displayed for failed logins.

    Fixtures:
    - `chrome_driver_setup`: Provides a preconfigured Chrome WebDriver instance for browser automation.
    - `logger_setup`: Provides a logger instance for recording test execution details.

    Preconditions:
    - The CarSphere application must be running and accessible at the predefined URL.
    - Chrome WebDriver must be installed and configured for Selenium.
    - 'Admin' and 'non-admin' user accounts with appropriate credentials must exist in the system.

    Logs and Outputs:
    - Logs include details on navigation, input data, expected/actual results, and validation outcomes.
    - On failure, appropriate errors are logged, and assertions are raised.

    Post-conditions:
    - Browser instance is closed after each test execution to clean up resources.
    """

    """Scenario_4."""
    @pytest.mark.system
    @pytest.mark.functional
    def test_004_admin_login_valid_credentials(self, chrome_driver_setup, logger_setup):
        """
        Test Case: test_004_admin_login_valid_credentials

        Test Description:
        This test verifies that an 'admin' user can successfully log in to the CarSphere application using valid credentials.

        Test Steps:
        1. Navigate to the application's Home Page.
        2. Redirect to the 'Login' page by clicking on the 'Login' link in the navigation bar.
        3. Populate the login form with valid 'admin' credentials:
           - Username: "admin"
           - Password: "admin"
        4. Submit the login form.
        5. Validate that a success message is displayed, indicating a successful login.

        Expected Result:
        - A success alert with the message "Welcome, Administrator Manager!" is displayed upon successful login.

        Assertions:
        - Verify that the actual success message matches the expected message.

        Fixtures:
        - `chrome_driver_setup`: Provides a preconfigured Chrome WebDriver instance for browser automation.
        - `logger_setup`: Provides a logger instance for recording test execution details.

        Logs and Outputs:
        - Logs details of navigation, input data, expected/actual results, and validation outcomes.
        - Logs success or failure based on the test assertion.

        Post-condition:
        - The browser instance is closed after test execution to clean up resources.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        login_page = LoginPage(driver)

        # Navigate to login page
        logger.info("Redirect to 'login' page")
        login_page.navigate_to_login_page()
        # Trying to Login as 'admin' user with valid password
        login_page.login('admin', 'admin')

        login_success_message = login_page.get_success_alert_message()
        expected_login_success_message = "Welcome, Administrator Manager!"
        assert login_success_message == expected_login_success_message, "Faild to login as 'asdmin' user"
        logger.info("Scenario_4 Passed")

    """Scenario_5"""
    @pytest.mark.system
    @pytest.mark.functional
    def test_005_admin_login_invalid_credentials(self, chrome_driver_setup, logger_setup):
        """
        Test Case: test_005_admin_login_invalid_credentials

        Test Description:
        This test verifies that an 'admin' user attempting to log in with invalid credentials is rejected and an appropriate error message is displayed.

        Test Steps:
        1. Navigate to the application's Home Page.
        2. Redirect to the 'Login' page by clicking on the 'Login' link in the navigation bar.
        3. Populate the login form with invalid 'admin' credentials:
           - Username: "admin"
           - Password: "1234" (invalid)
        4. Submit the login form.
        5. Validate that an error message is displayed, indicating login failure.

        Expected Result:
        - An error alert with the message "Login Unsuccessful. Please check username and password" is displayed.

        Assertions:
        - Verify that the actual error message matches the expected message.

        Fixtures:
        - `chrome_driver_setup`: Provides a preconfigured Chrome WebDriver instance for browser automation.
        - `logger_setup`: Provides a logger instance for recording test execution details.

        Logs and Outputs:
        - Logs details of navigation, input data, expected/actual results, and validation outcomes.
        - Logs success or failure based on the test assertion.

        Post-condition:
        - The browser instance is closed after test execution to clean up resources.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        login_page = LoginPage(driver)

        # Navigate to login page
        logger.info("Redirect to 'login' page")
        login_page.navigate_to_login_page()

        logger.info("Entering invalid 'admin'credentials and clicking on the submit button")
        login_page.login('admin', '1234')

        logger.info("Getting the unsuccessful alert message")
        login_unsuccessful_message = login_page.get_unsuccessful_alert_message()
        logger.info(f"unsuccessful alert message: {login_unsuccessful_message}")

        logger.info("Validating the unsuccessful alert message")
        expected_login_unsuccessful_message = "Login Unsuccessful. Please check username and password"
        assert login_unsuccessful_message == expected_login_unsuccessful_message, \
            "Login as 'admin' with invalid password should not be allowed"
        logger.info("Scenario_5 Passed")



    """Scenario_6"""
    @pytest.mark.sanity
    @pytest.mark.system
    @pytest.mark.functional
    def test_006_non_admin_login_valid_credentials(self, chrome_driver_setup, logger_setup):
        """
        Test Case: test_006_non_admin_login_valid_credentials

        Test Description:
        This test verifies that a 'non-admin' user can successfully log in using valid credentials, and the application displays the correct success message.

        Test Steps:
        1. Navigate to the application's Home Page.
        2. Redirect to the 'Login' page by clicking on the 'Login' link in the navigation bar.
        3. Populate the login form with valid credentials for a non-admin user:
           - Username: "user3"
           - Password: "user3"
        4. Submit the login form.
        5. Validate that the success message is displayed upon successful login.

        Expected Result:
        - A success alert with the message "Welcome, user3 user3!" is displayed.

        Assertions:
        - Verify that the actual success message matches the expected message.

        Fixtures:
        - `chrome_driver_setup`: Provides a preconfigured Chrome WebDriver instance for browser automation.
        - `logger_setup`: Provides a logger instance for recording test execution details.

        Logs and Outputs:
        - Logs details of navigation, input data, expected/actual results, and validation outcomes.
        - Logs success or failure based on the test assertion.

        Post-condition:
        - The browser instance is closed after test execution to clean up resources.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        # Loging-in as 'non-admin' user with valid credenatials
        login_page.login('user3', 'user3')

        logger.info("Getting the success alert message")
        login_success_message = login_page.get_success_alert_message()
        expected_login_success_message = "Welcome, user3 user3!"
        logger.info(f"Success alert message: {login_success_message}")
        
        logger.info("Validate login success for 'non-admin' user with valid credentials")
        assert login_success_message == expected_login_success_message, \
            "Login as 'non-admin' user with valid credentials should be allowed."
        logger.info("Scenario_6 Passed")

    """Scenario_7"""
    @pytest.mark.system
    @pytest.mark.functional
    def test_007_non_admin_login_invalid_credentials(self, chrome_driver_setup, logger_setup):
        """
        Test Case: test_007_non_admin_login_invalid_credentials

        Test Description:
        This test verifies that a 'non-admin' user attempting to log in with invalid credentials is rejected, and the appropriate error message is displayed.

        Test Steps:
        1. Navigate to the application's Home Page.
        2. Redirect to the 'Login' page by clicking on the 'Login' link in the navigation bar.
        3. Populate the login form with invalid credentials for a non-admin user:
           - Username: "user3"
           - Password: "user" (invalid password).
        4. Submit the login form.
        5. Validate that the correct error message is displayed for an unsuccessful login attempt.

        Expected Result:
        - An error alert with the message "Login Unsuccessful. Please check username and password" is displayed.

        Assertions:
        - Verify that the actual error message matches the expected error message.

        Fixtures:
        - `chrome_driver_setup`: Provides a preconfigured Chrome WebDriver instance for browser automation.
        - `logger_setup`: Provides a logger instance for recording test execution details.

        Logs and Outputs:
        - Logs details of navigation, input data, expected/actual results, and validation outcomes.
        - Logs success or failure based on the test assertion.

        Post-condition:
        - The browser instance is closed after test execution to clean up resources.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        login_page.login('user3', 'user')
        login_unsuccessful_message = login_page.get_unsuccessful_alert_message()
        expected_login_unsuccessful_message = "Login Unsuccessful. Please check username and password"
        assert login_unsuccessful_message == expected_login_unsuccessful_message, \
            "Login as 'non-admin' user with invalid password should not be allowed"
        logger.info("Scenario_7 Passed")

@pytest.mark.usefixtures("chrome_driver_setup", "logger_setup")
class TestLogoutUsers:
    """
    Test Class: TestLogoutUsers

    This class groups all functional and regression tests related to the 'Logout' functionality in the CarSphere application.
    The tests focus on verifying that both 'admin' and 'non-admin' users can successfully log out and receive the expected success message.

    Key Objectives:
    1. Validate that an 'admin' user can log out successfully and see the correct logout confirmation message.
    2. Ensure that a 'non-admin' user can also log out successfully and see the appropriate success message.
    3. Confirm consistent application behavior and user feedback for the logout process.

    Test Scenarios Included:
    - **Scenario_8**: Verify that the 'admin' user can log out successfully.
    - **Scenario_9**: Verify that the 'non-admin' user can log out successfully.

    Fixtures:
    - `chrome_driver_setup`: Provides a configured Chrome WebDriver instance for browser automation.
    - `logger_setup`: Provides a logger instance for detailed test execution logging.

    Preconditions:
    - The CarSphere application is running and accessible at the predefined URL.
    - Chrome browser is installed, configured, and available for automation.
    - 'Admin' and 'non-admin' user accounts exist in the application.

    Post-conditions:
    - After each test, the browser instance is closed to release resources.

    Expected Results:
    - Both 'admin' and 'non-admin' users should see the logout confirmation message: **"You have been logged out."**

    Markers:
    - `@pytest.mark.regression`: Indicates that the tests are critical for validating system stability during changes.
    - `@pytest.mark.functional`: Ensures that the logout functionality works as intended.
    """

    """Scenario_8"""
    @pytest.mark.regression
    @pytest.mark.functional
    def test_008_logout_admin(self, chrome_driver_setup, logger_setup):
        """
        Test Case: test_008_logout_admin

        Test Description:
        This test verifies that an 'admin' user can successfully log out of the CarSphere application and receives the expected logout confirmation message.

        Test Steps:
        1. Navigate to the application's Home Page.
        2. Redirect to the 'Login' page by clicking on the 'Login' link in the navigation bar.
        3. Log in using valid 'admin' credentials:
           - Username: "admin"
           - Password: "admin"
        4. Click on the 'Logout' button located in the navigation bar.
        5. Validate that the logout confirmation message is displayed.

        Expected Result:
        - A success alert with the message **"You have been logged out."** is displayed.

        Assertions:
        - Verify that the actual logout success message matches the expected logout success message.

        Fixtures:
        - `chrome_driver_setup`: Provides a preconfigured Chrome WebDriver instance for browser automation.
        - `logger_setup`: Provides a logger instance for recording test execution details.

        Logs and Outputs:
        - Logs navigation steps, input actions, expected/actual results, and validation outcomes.
        - Logs success or failure based on the test assertion.

        Post-condition:
        - The browser instance is closed after test execution to clean up resources.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        # Logging in as 'admin' user
        logger.info("Logging in as 'admin' user")
        login_page.login('admin', 'admin')

        # Logging out as 'admin' user
        logger.info("Logging out as 'admin' user")
        login_page.logout()

        # Getting the success alert message
        logout_success_message = login_page.get_success_alert_message()
        logger.info(f"Success alert message: {logout_success_message}")

        expected_logout_success_message = "You have been logged out."
        assert logout_success_message == expected_logout_success_message, \
            "Logout as 'admin' user should be allowed."
        logger.info("'Scenario_8 Passed")

    """Scenario_9"""
    @pytest.mark.regression
    @pytest.mark.functional
    def test_009_logout_non_admin(self, chrome_driver_setup, logger_setup):
        """
        Test Case: test_009_logout_non_admin

        Test Description:
        This test verifies that a 'non-admin' user can successfully log out of the CarSphere application and receives the expected logout confirmation message.

        Test Steps:
        1. Navigate to the application's Home Page.
        2. Redirect to the 'Login' page by clicking on the 'Login' link in the navigation bar.
        3. Log in using valid 'non-admin' credentials:
           - Username: "user3"
           - Password: "user3"
        4. Click on the 'Logout' button located in the navigation bar.
        5. Validate that the logout confirmation message is displayed.

        Expected Result:
        - A success alert with the message **"You have been logged out."** is displayed.

        Assertions:
        - Verify that the actual logout success message matches the expected logout success message.

        Fixtures:
        - `chrome_driver_setup`: Provides a preconfigured Chrome WebDriver instance for browser automation.
        - `logger_setup`: Provides a logger instance for recording test execution details.

        Logs and Outputs:
        - Logs navigation steps, input actions, expected/actual results, and validation outcomes.
        - Logs success or failure based on the test assertion.

        Post-condition:
        - The browser instance is closed after test execution to clean up resources.
        """
        logger = logger_setup
        logger.debug("'Logger' setup success")
        driver = chrome_driver_setup
        logger.debug("'Chrome web driver' setup success")

        # Use POM page
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()

        # Logging in as 'non-admin' user
        logger.info("Logging in as 'non-admin' user")
        login_page.login('user3', 'user3')

        # Logging out as 'non-admin' user
        logger.info("Logging out as 'non-admin' user")
        login_page.logout()

        # Getting the success alert message
        logout_success_message = login_page.get_success_alert_message()
        logger.info(f"Success alert message: {logout_success_message}")

        # Validating the success alert message
        expected_logout_success_message = "You have been logged out."
        assert logout_success_message == expected_logout_success_message, \
            "Logout as 'non-admin' user should be allowed."
        logger.info("'Scenario_9 Passed")
