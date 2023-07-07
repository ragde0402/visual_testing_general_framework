import argparse
import os
import comparing
import test
from config import *
from svn_utils import SVN_UTILS
from microservices.example import *
from ftp_utils import FTP_UTILS
from helpers import helper


def take_screenshot_and_save_in_storage(url: str,
                                        user: str,
                                        password: str,
                                        microservice: str,
                                        environment: str,
                                        storage: str):
    options = webdriver.FirefoxOptions()
    options.accept_insecure_certs = True
    options.add_argument(width)
    options.add_argument(height)
    driver = webdriver.Remote(options=options, command_executor=executor)

    basic_url = f"{os.getcwd()}/tmp/"
    if storage == "svn":
        svn_object = SVN_UTILS(url, user, password, basic_url)

        # removing all previous files in svn
        svn_object.clear_svn()

        list_of_screens = helper(microservice, environment, driver, basic_url)

        svn_object.add_files(list_of_screens)

    elif storage == "ftp":
        ftp_object = FTP_UTILS(url, user, password, microservice)
        ftp_object.delete_all_files_in_directory()

        list_of_screens = helper(microservice, environment, driver, basic_url)

        ftp_object.upload_all_files(list_of_screens)

    # removing local files and folders
    os.system(f'rm -rf {os.getcwd()}/tmp')

    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_source")
    parser.add_argument("-U", "--url")
    parser.add_argument("-u", "--user")
    parser.add_argument("-p", "--password")
    parser.add_argument("-n", "--name")
    parser.add_argument("-m", "--method")
    parser.add_argument("-c", "--csvfile")
    parser.add_argument("-a", "--archive")
    parser.add_argument("-e", "--environment")
    args = parser.parse_args()

    storage = args.data_source
    address = f"{args.url}/{args.name.upper()}/" if storage != "zip" else f"{args.name.upper()}"

    if args.method == "new_screenshots":
        take_screenshot_and_save_in_storage(address,
                                            args.user,
                                            args.password,
                                            args.name.upper(),
                                            args.environment.upper(), storage)
    elif args.method == "check_screenshots":
        comparing.compare_images(address,
                                 args.user,
                                 args.password,
                                 args.name.upper(),
                                 args.csvfile,
                                 args.archive,
                                 args.environment.upper())
    elif args.method == "test":
        test.test(args.name.upper(),
                  args.environment.upper())
