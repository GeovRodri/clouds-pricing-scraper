import json
from pprint import pprint

import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.Utils import Utils


class BaseDriver:

    url = ''
    driver = None
    tables = None

    def __init__(self):
        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

        self.driver.get(self.url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)

        """ Buscando tabelas na página de possuem valor ($) """
        self.tables = self.driver.find_elements_by_xpath('//table//td[starts-with(., "$")]/../../..')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def save_json(self, name, data):
        """ Convertendo para JSON e imprimindo na tela """
        data_json = json.dumps(data, indent=4)
        path_file = 'results/' + name

        os.makedirs(os.path.dirname(path_file), exist_ok=True)
        with open(path_file, 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            f.write(data_json)
