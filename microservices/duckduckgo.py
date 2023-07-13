from selenium.webdriver.common.by import By
from selenium import webdriver
from route_utils import RouteUtils


class DUCKDUCKGO(RouteUtils):
    """
    For every microservice create separated class that will inherit from RouteUtils class and have specified route
    """

    # specific selectors for microservice
    selector_menu_button_xpath = "//a[contains(@class,'header__button--menu')]"
    selector_setting_menuoption_xpath = "//ul[@class='nav-menu__list']//ul//li[@class='nav-menu__item']"

    def __init__(self, environment: str):
        super().__init__()
        self.data_dict = self.get_url_and_user("DUCKDUCKGO", environment=environment)
        self.name_generator = self.get_screen_name("DUCKDUCKGO")

    def route(self, driver: webdriver, path: str):
        """
        Full selenium script with all click and screenshot saving
        :param driver: used webdriver
        :param path: local path where screenshots will be saved
        :return:
        """

        driver.get(self.data_dict["url"])
        driver.save_screenshot(f"{path}{next(self.name_generator)}")
        driver.find_element(By.XPATH, self.selector_menu_button_xpath).click()
        driver.find_element(By.XPATH, self.selector_setting_menuoption_xpath).click()
        driver.save_screenshot(f"{path}{next(self.name_generator)}")

#       Create your own selenium path and use driver.save_screenshot(f"{path}{next(self.name_generator)}") for saving
#       screenshots under the correct name in the correct order
