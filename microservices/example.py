from selenium import webdriver
from route_utils import RouteUtils


class EXAMPLE(RouteUtils):
    """
    For every microservice create separated class that will inherit from RouteUtils class and have specified route
    """

    # specific selectors for microservice
    selector_menu_class = "ui-panelmenu-panel"
    selector_menuoption_id = "menuform:nav_%%OPTION%%"

    def __init__(self, environment: str):
        super().__init__()
        self.data_dict = self.get_url_and_user("EXAMPLE", environment=environment)
        self.name_generator = self.get_screen_name("EXAMPLE")

    def route(self, driver: webdriver, path: str):
        """
        Full selenium script with all click and screenshot saving
        :param driver: used webdriver
        :param path: local path where screenshots will be saved
        :return:
        """

        self.perform_login(driver, path)
        driver.save_screenshot(f"{path}{next(self.name_generator)}")

#       Create your own selenium path and use driver.save_screenshot(f"{path}{next(self.name_generator)}") for saving
#       screenshots under the correct name in the correct order
