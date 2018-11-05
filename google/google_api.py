import csv
import json
from pprint import pprint
from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.select import Select

from utils import Utils


class PricesDriver(object):

    driver = None

    def __init__(self):
        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

    def get_price(self, url):
        titles, data = [], {}
        instances, instances_keys = [], []

        self.driver.get(url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)

        tables = self.driver.find_elements_by_xpath("//table//th[contains(text(),'Tipo de máquina')]/../../..")

        """ Pegando o select de seleção de localização """
        localizations, locations = self.get_options_localization()

        for localization in localizations:
            data[localization] = []

            """ Selecionando uma opção"""
            options = self.driver.find_elements_by_xpath("//md-option//div[@class='md-text'][contains(text(),'{}')]/.."
                                                         .format(localization))
            for option in options:
                self.driver.execute_script("$('#{}').click()".format(option.get_attribute("id")))
                sleep(2)

            for table in tables:
                trs = table.find_elements_by_tag_name("tr")
                for tr in trs:
                    tds = tr.find_elements_by_tag_name("td")

                    """ Verificando se é td(valores) ou th(titulos) """
                    if len(tds) > 0:
                        columns, index = {}, 0

                        for td in tds:
                            text_th = titles[index]
                            if text_th not in columns:
                                columns[text_th] = []

                            columns[text_th] = td.text
                            index += 1

                        if 'Tipo de máquina' in columns and 'Preço (US$)' in columns and 'Memória' in columns:
                            data[localization].append(columns)

                            if columns['Tipo de máquina'] not in instances_keys:
                                instances.append(columns)
                                instances_keys.append(columns['Tipo de máquina'])
                            else:
                                index = instances_keys.index(columns['Tipo de máquina'])
                                obj = instances[index]
                                obj[localization] = columns['Preço (US$)']
                    else:
                        ths = tr.find_elements_by_tag_name("th")
                        for th in ths:
                            titles.append(th.text)

        """ Convertendo para JSON e imprimindo na tela """
        data_json = json.dumps(data, indent=4)
        pprint(data_json)
        self.driver.close()

        with open('Google_Regions.csv', 'w', newline='') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=list(locations[0].keys()), delimiter=';')
            w.writeheader()
            w.writerows(locations)

        with open('Google.csv', 'w', newline='') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=titles + localizations, delimiter=';')
            w.writeheader()
            w.writerows(instances)

    def get_options_localization(self):
        options = []
        options_name = []

        options_page = self.driver.find_elements_by_tag_name("md-option")
        for option in options_page:
            if option.text not in options and len(option.text) > 0:
                options.append(option.text)
                options_name.append({'Name': option.text})

        return options, options_name


if __name__ == "__main__":
    prices_drive = PricesDriver()
    prices_drive.get_price("https://cloud.google.com/compute/pricing")
