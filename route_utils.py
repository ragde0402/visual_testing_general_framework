from selenium.webdriver.common.by import By
from selenium import webdriver
import csv


class RouteUtils:

    #shared variables
    data_dict = None
    name_generator = None

    # General selectors
    selector_username_input_id = "login:user"
    selector_password_input_id = "login:password"
    selector_login_button_id = "login:loginbutton"

    # General list of all screenshot name as dictionary microservice_name: list_of_screenshot_names in pattern
    # Microservice name as prefix and including file extension for example .png
    dict_of_screen_names_for_microservice = {"EXAMPLE": ["EXAMPLE_login_site.png"],
                                             "DUCKDUCKGO": ["DUCKDUCKGO_main_page.png", "DUCKDUCKGO_settings_page.png"],}

    def __init__(self):
        pass

    @staticmethod
    def get_url_and_user(microservice: str, environment: str):
        """

        :param microservice: name of microservice
        :param environment: environment corresponding to one from environments.csv headers
        :return: dictionary containing url and required user data
        """
        with open("environments.csv", "r") as file:
            result = {}
            for row in csv.DictReader(file):
                print(row)
                if row["service variable"] == microservice + "_ROOT_URL":
                    result["url"] = row[environment]
                if row["service variable"] == microservice + "_USER":
                    result["user"] = row[environment]
                if row["service variable"] == microservice + "_PASS":
                    result["password"] = row[environment]
            return result

    def get_screen_name(self, microservice: str):
        """

        :param microservice: name of microservice
        :return: generator that return only next name of screenshot for given microservice name
        """
        for name in self.dict_of_screen_names_for_microservice[microservice]:
            yield name

    def perform_login(self, driver: webdriver, path: str):
        """
        Example of general method that can be used in all microservices
        :param driver: used webdriver
        :param path: local path where screenshot will be saved
        :return:
        """
        driver.delete_all_cookies()
        driver.get(self.data_dict["url"])

        if "viewExpired" in driver.current_url:
            driver.find_element(By.TAG_NAME, "button").click()

        driver.save_screenshot(f"{path}{next(self.name_generator)}")

        driver.find_element(By.ID, self.selector_username_input_id).send_keys(self.data_dict["user"])
        driver.find_element(By.ID, self.selector_password_input_id).send_keys(self.data_dict["password"])
        driver.find_element(By.ID, self.selector_login_button_id).click()

