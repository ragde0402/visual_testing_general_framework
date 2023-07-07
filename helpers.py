

def helper(microservice, environment, driver, basic_url):
    # Creation of object from class coresponding to microservice name including correct environment
    microservice_object = globals()[microservice](environment)

    # calling selenium script to go through microservice and screenshot creation
    microservice_object.route(driver, basic_url)

    # Adding files to remote svn
    list_of_screens = [basic_url + filename for filename in
                       microservice_object.dict_of_screen_names_for_microservice[microservice]]
    return list_of_screens
