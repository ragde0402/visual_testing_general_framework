from selenium.webdriver import FirefoxOptions, Remote
import argparse
import os
import comparing
import test
from config import *
from svn_utils import SVN_UTILS
from microservices.example import *


def take_screenshot_and_save_in_svn(svn_url: str, user: str, password: str, microservice: str, environment: str):
    options = webdriver.FirefoxOptions()
    options.accept_insecure_certs = True
    options.add_argument(width)
    options.add_argument(height)
    driver = webdriver.Remote(options=options, command_executor=executor)

    basic_url = f"{os.getcwd()}/tmp/"

    svn_object = SVN_UTILS(svn_url, user, password, basic_url)

    # removing all previous files in svn
    svn_object.clear_svn()

    # Creation of object from class coresponding to microservice name including correct environment
    microservice_object = globals()[microservice](environment)

    # calling selenium script to go through microservice and screenshot creation
    microservice_object.route(driver, basic_url)

    # Adding files to remote svn
    list_of_screens = [basic_url + filename for filename in microservice_object.dict_of_screen_names_for_microservice[microservice]]
    svn_object.add_files(list_of_screens)

    # removing local files and folders
    os.system(f'rm -rf {os.getcwd()}/tmp')

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--svn_url")
    parser.add_argument("-u", "--user")
    parser.add_argument("-p", "--password")
    parser.add_argument("-n", "--name")
    parser.add_argument("-m", "--method")
    parser.add_argument("-c", "--csvfile")
    parser.add_argument("-a", "--archive")
    parser.add_argument("-e", "--environment")
    args = parser.parse_args()

    if args.method == "new_screenshots":
        take_screenshot_and_save_in_svn(f"{args.svn_url}/{args.name.upper()}/",
                                        args.user,
                                        args.password,
                                        args.name.upper(),
                                        args.environment.upper())
    elif args.method == "check_screenshots":
        comparing.compare_images(f"{args.svn_url}/{args.name.upper()}/",
                                 args.user,
                                 args.password,
                                 args.name.upper(),
                                 args.csvfile,
                                 args.archive,
                                 args.environment.upper())
    elif args.method == "test":
        test.test(args.name.upper(), args.environment.upper())
