import logging
from config import *
import numpy as np
import os
import cv2
import csv
from microservices.example import *
from svn_utils import SVN_UTILS


def compare_images(svn_url: str, user: str, password: str, microservice: str, csv_base_file: str, archive_svn: str, environment: str):
    """
    Method compare all images taken during route pass with its reference storred in svn

    :param svn_url: url address to remote svn
    :param user: if svn requires authentication
    :param password: if svn requires authentication
    :param microservice: name of microservice, corresponding to name of class and data saved in environments.csv
    :param csv_base_file: name of csv file where results will be saved
    :param archive_svn: svn directory where archive will be saved
    :param environment: environment corresponding to one of the headers in environments.csv
    :return:
    """
    options = webdriver.FirefoxOptions()
    options.accept_insecure_certs = True
    options.add_argument(width)
    options.add_argument(height)
    driver = webdriver.Remote(options=options, command_executor=executor)

    # working with reference files taken previously and saved in svn
    basic_url = f"{os.getcwd()}/tmp/"

    _ = SVN_UTILS(svn_url, user, password, basic_url)

    for file in os.listdir(f"{os.getcwd()}/tmp"):
        if not file.endswith(".png"):
            continue
        logging.debug(f"FILE: {file}")
        blank = cv2.imread("blank.png")
        color = cv2.imread(f"{basic_url}{file}")
        gray = cv2.cvtColor(color, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 200, apertureSize=3)
        cv2.imwrite('edges.png', edges)
        min_line_length = 50
        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                                minLineLength=min_line_length, maxLineGap=80)

        a, b, c = lines.shape
        for i in range(a):
            cv2.line(blank, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 0), 3,
                     cv2.LINE_AA)
            cv2.imwrite(f'{file.split(".")[0]}_reference.png', blank)

    microservice_object = globals()[microservice](environment)


    os.mkdir(f"{os.getcwd()}/tmp_current")

    basic_url = f"{os.getcwd()}/tmp_current/"

    list_of_screens = [basic_url + filename for filename in microservice_object.dict_of_screen_names_for_microservice[microservice]]

    # making screenshots
    microservice_object.route(driver, basic_url)

    for file in list_of_screens:
        blank = cv2.imread("blank.png")
        color = cv2.imread(file)
        gray = cv2.cvtColor(color, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 200, apertureSize=3)
        cv2.imwrite('edges.png', edges)
        min_line_length = 50
        lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                                minLineLength=min_line_length, maxLineGap=80)

        a, b, c = lines.shape
        for i in range(a):
            cv2.line(blank, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 0), 3,
                     cv2.LINE_AA)
            cv2.imwrite(f'{file}_new', blank)

        one = cv2.imread(f'{file}_new')
        two = cv2.imread(f'{file.split("/")[-1].split(".")[0]}_reference.png')

        errorL2 = cv2.norm(one, two, cv2.NORM_L2)
        similarity = 1 - errorL2 / (1080 * 1720)
        print('Similarity = ', similarity)

        if similarity < 0.99:
            os.system(f'cp {file} {archive_svn}')

        with open(csv_base_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            csvwriter.writerow([microservice, file.split("/")[-1].split(".")[0], similarity])

    os.system(f'rm -rf {os.getcwd()}/tmp')
    driver.quit()


