import random
import string
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import requests
from pages.login_page import LoginPage

class RegisterPage(LoginPage):
    NAV_LINKS = (By.XPATH, "//nav/a")
    FIRST_NAME = (By.XPATH, "//input[@id='firstname']")
    LAST_NAME = (By.XPATH, "//input[@id='lastname']")
    USERNAME = (By.XPATH, "//input[@id='username']")
    PASSWORD = (By.XPATH, "//input[@id='password']")
    CONFIRM_PASSWORD = (By.XPATH, "//input[@id='confirm_password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Sign Up']")

    def navigate_to_register_page(self):
        links = self.find_elements(*self.NAV_LINKS)
        for link in links:
            if "register" in link.get_attribute("href"):
                link.click()
                break

    def get_users_list_from_api(self):
        response = requests.get("https://carsphere.onrender.com/get-users")
        existing_users = response.text
        return existing_users
    
    def generate_new_random_username(self, existing_users):
        random_username = existing_users[0]
        while random_username in existing_users:
            random_username = "Auto_username" + ''.join(random.choices(string.digits, k=3))
        return random_username
    
    def generate_new_random_password(self):
        password = "1234"
        return password

    def fill_and_submit_registration_form(self, first_name, last_name, username, password, confirm_password):
        self.find_element(*self.FIRST_NAME).send_keys(first_name)
        self.find_element(*self.LAST_NAME).send_keys(last_name)
        self.find_element(*self.USERNAME).send_keys(username)
        self.find_element(*self.PASSWORD).send_keys(password)
        self.find_element(*self.CONFIRM_PASSWORD).send_keys(confirm_password)
        self.find_element(*self.SUBMIT_BUTTON).click()

    def get_alert_danger_message(self):
        return self.find_element(By.CSS_SELECTOR, ".alert.alert-danger").text
    
    def get_alert_mismatch_password_message_color(self):
        return self.find_element(By.ID, "confirm_pass").value_of_css_property("color")
    
    def get_alert_mismatch_password_message(self):
        mismatch_password_alert = self.find_element(By.ID, "confirm_pass").text
        mismatch_password_alert_expected_color = self.get_alert_mismatch_password_message_color()
        return mismatch_password_alert, mismatch_password_alert_expected_color
        
