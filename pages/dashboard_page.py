# pages/dashboard_page.py
from asyncio import wait
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.login_page import LoginPage

class DashboardPage(LoginPage):
    # Locators
    MAIN_BACKGROUND_IMAGE = (By.TAG_NAME, "body")
    BRANDING_ICON = (By.CLASS_NAME, "branding-icon")
    LINKEDIN_ICON = (By.XPATH, "//p/a/img[@class='linkedin-icon']")
    ADD_NEW_CAR_BUTTON = (By.XPATH, "//nav/a[@href='/add_car']")
    DELETE_CAR_BUTTONS = (By.XPATH, "//div[@class='car-item']/form/button[@class='btn btn-danger']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert.alert-success")
    
    # Add Car Form Locators
    MAKE_INPUT = (By.XPATH, "//input[@id='make']")
    MODEL_INPUT = (By.XPATH, "//input[@id='model']")
    YEAR_SELECT = (By.XPATH, "//select/option")
    DIRECTOR_INPUT = (By.XPATH, "//input[@id='director']")
    MAIN_SETTINGS_INPUT = (By.ID, "main_settings")
    DESCRIPTION_INPUT = (By.XPATH, "//div/textarea[@name='description']")
    IMAGE_INPUT = (By.XPATH, "//input[@id='image_file']")
    SUBMIT_BUTTON = (By.XPATH, "//input[@id='submit']")
    LAST_CAR_ELEMENT_LOCATION = (By.XPATH, "//div/div/div/a")
    REVIEW_INPUT = (By.XPATH, "//form/textarea")
    SUBMIT_REVIEW_BUTTON = (By.ID, "submit")
    USERS_REVIEW_AREA = (By.XPATH, "//ul/li")
    AI_REVIEW_BUTTON = (By.ID, "ai-review-button")
    AI_REVIEW_INPUT = (By.ID, "review-input")

    # ADD_CAR_SUCCESS_MESSAGE = (By.XPATH, "//div/div[@class='alert alert-success']")
    # DELETE_SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert.alert-success")


    def is_add_new_car_visible(self):
        return self.is_element_visible(*self.ADD_NEW_CAR_BUTTON)

    def are_delete_buttons_visible(self):
        try:
            delete_buttons = self.find_elements(*self.DELETE_CAR_BUTTONS)
            return len(delete_buttons) > 0
        except TimeoutException:
            return False

    def add_new_car(self, make, model, year, director, settings, description, image_path):
        self.find_element(*self.MAKE_INPUT).send_keys(make)
        self.find_element(*self.MODEL_INPUT).send_keys(model)
        # Select year from dropdown
        year.click()
        self.find_element(*self.DIRECTOR_INPUT).send_keys(director)
        self.find_element(*self.MAIN_SETTINGS_INPUT).send_keys(settings)
        self.find_element(*self.DESCRIPTION_INPUT).send_keys(description)
        self.find_element(*self.IMAGE_INPUT).send_keys(image_path)
        self.find_element(*self.SUBMIT_BUTTON).click()
        return self.get_success_message() == f"Car {make} {model} added successfully!"

    def delete_last_car(self):
        delete_buttons = self.find_elements(*self.DELETE_CAR_BUTTONS)
        if len(delete_buttons) > 6:
            try:
                delete_buttons[-1].click()
                return self.get_success_message() == "Car deleted successfully!"
            except TimeoutException:
                return False
        return False

    def get_success_message(self):
        return self.find_element(*self.SUCCESS_MESSAGE).text

    def navigate_to_add_new_car_form(self):
        self.find_element(*self.ADD_NEW_CAR_BUTTON).click()

    def navigate_to_linkedin_page_and_get_current_url(self):
        self.find_element(*self.LINKEDIN_ICON).click()
        my_windows = self.driver.window_handles
        self.driver.switch_to.window(my_windows[1])
        return self.driver.current_url

    def get_main_background_image(self):
        return self.find_element(*self.MAIN_BACKGROUND_IMAGE).value_of_css_property("background-image")
    
    def get_branding_icon_url(self):
        return self.find_element(*self.BRANDING_ICON).get_attribute("src")
    
    def navigate_to_last_car_in_catalog(self):
        cars_element_list =self.find_elements(*self.LAST_CAR_ELEMENT_LOCATION)
        cars_element_list[-1].click()

    def add_manual_review(self, manual_review_input):
        self.find_element(*self.REVIEW_INPUT).send_keys(manual_review_input)
        self.find_element(*self.SUBMIT_REVIEW_BUTTON).click()

    def get_user_new_review(self):
        users_review_list = self.find_elements(*self.USERS_REVIEW_AREA)
        return users_review_list[-1].text
    
    def get_ai_review_by_clicking_ai_review_button(self, driver):
        self.find_element(*self.AI_REVIEW_BUTTON).click()
        ai_review = wait(lambda _driver: driver.find_element(By.ID, "review-input").get_attribute("value") != '')
        return ai_review
    
    def submit_ai_review(self):
        self.find_element(*self.SUBMIT_REVIEW_BUTTON).click()
