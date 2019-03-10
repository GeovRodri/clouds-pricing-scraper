import json
import os
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.Utils import Utils


class BaseDriver:

    url = ''
    name_file = 'default'
    tables = None
    columns = {}

    def get(self):
        self.search()
        self.save_json()

    def search(self):
        raise NotImplementedError()

    def save_json(self):
        """ Convertendo para JSON e imprimindo na tela """
        data_json = json.dumps(self.columns, indent=4)
        path_file = 'results/' + self.name_file

        os.makedirs(os.path.dirname(path_file), exist_ok=True)
        with open(path_file, 'w', newline='', encoding='utf-8') as f:
            f.write(data_json)
