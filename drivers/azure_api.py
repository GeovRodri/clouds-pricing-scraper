import csv
import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.select import Select
from commons.utils import Utils


class PricesDriver(object):

    driver = None

    def __init__(self):
        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

    def get_price(self, url):
        headers = ['INSTANCE', 'CORE', 'RAM', 'TEMPORARY STORAGE', 'vCPU', 'ACTIVE vCPU / UNDERLYING vCPU',	'GPU']
        data, localizations = {}, []
        locations, instances, instances_keys = [], [], []

        self.driver.get(url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)

        text_element = self.driver.find_element_by_xpath("//div[@id='vm-tables']")

        """ Pegando o select de seleção de localização """
        options_localization, select_localization = self.get_options_localization(text_element)
        tables = text_element.find_elements_by_xpath("//table[@class='sd-table']")

        for option_localization in options_localization:
            data[option_localization.text] = []

            if option_localization.text not in localizations:
                locations.append({'Name': option_localization.text})
                localizations.append(option_localization.text)

            """ Selecionando uma opção"""
            select_localization.select_by_value(option_localization.get_attribute("value"))

            for table in tables:
                titles = []

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

                        data[option_localization.text].append(columns)

                        if columns['INSTANCE'] not in instances_keys:
                            instances.append(columns)
                            instances_keys.append(columns['INSTANCE'])
                            columns[option_localization.text] = columns['PAY AS YOU GO']
                        else:
                            index = instances_keys.index(columns['INSTANCE'])
                            obj = instances[index]
                            obj[option_localization.text] = columns['PAY AS YOU GO']
                    else:
                        ths = tr.find_elements_by_tag_name("th")
                        for th in ths:
                            if th.text not in titles:
                                titles.append(th.text)

        """ Convertendo para JSON e imprimindo na tela """
        data_json = json.dumps(data, indent=4)
        pprint(data_json)
        self.driver.close()

        with open('Azure_Regions.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=list(locations[0].keys()), delimiter=';')
            w.writeheader()
            w.writerows(locations)

        with open('Azure.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            headers = headers + localizations
            w = csv.DictWriter(f, fieldnames=headers, delimiter=';')
            w.writeheader()

            for instance in instances:
                obj = {}
                for header in headers:
                    obj[header] = instance.get(header, '-')

                w.writerow(obj)

    def get_options_localization(self, text_element):
        select_localization_element = text_element.find_element_by_xpath("//select[@id='region-selector']")
        select_localization = Select(select_localization_element)
        options_localization = select_localization.options
        return options_localization, select_localization


if __name__ == "__main__":
    prices_drive = PricesDriver()
    prices_drive.get_price("https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/")

