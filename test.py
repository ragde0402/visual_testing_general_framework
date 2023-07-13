from microservices.example import *
from microservices.duckduckgo import *
from config import *
import os


def test(microservice: str, environment: str):
    """
    Method for local testing of selenium scripts
    :param microservice: name of microservice
    :param environment: environment corresponding to one from environments.csv
    :return:
    """
    basic_url = f"{os.getcwd()}/tmp_current/"
    options = webdriver.FirefoxOptions()
    options.accept_insecure_certs = True
    options.add_argument(width)
    options.add_argument(height)
    options.binary_location = "C:\Program Files\Mozilla Firefox\\firefox.exe" #Add your location
    driver = webdriver.Firefox(options=options)

    microservice_object = globals()[microservice](environment)
    microservice_object.route(driver, basic_url)

