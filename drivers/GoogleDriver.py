import csv
import json
from pprint import pprint
from time import sleep
from commons.BaseDriver import BaseDriver


class GoogleDriver(BaseDriver):

    def __init__(self):
        self.url = "https://cloud.google.com/compute/pricing"
        super().__init__()

    def get_price(self):
        titles, data = [], {}
        instances, instances_keys = [], []

        """ Pegando o select de seleção de localização """
        localizations = self.get_options_localization()

        for localization in localizations:
            data[localization] = []
            self.select_option(localization)

            for table in self.tables:
                trs = table.find_elements_by_tag_name("tr")
                for tr in trs:
                    tds = tr.find_elements_by_tag_name("td")

                    """ Verificando se é titulo """
                    if len(tds) <= 0:
                        ths = tr.find_elements_by_tag_name("th")
                        for th in ths:
                            if th.text not in titles:
                                titles.append(th.text)

                        continue

                    columns, index = {}, 0
                    for td in tds:
                        text_th = titles[index]

                        """ Se for um valor agrupar em princing, se não só adicionar como uma coluna """
                        if str(td.text).startswith('$'):
                            if 'pricing' not in columns:
                                columns['pricing'] = {}

                            if localization not in columns['pricing']:
                                columns['pricing'][localization] = {}

                            columns['pricing'][localization][text_th] = td.text
                        else:
                            if text_th not in columns:
                                columns[text_th] = {}

                            columns[text_th] = td.text

                        index += 1

                    data[localization].append(columns)

                    if columns['Tipo de máquina'] not in instances_keys:
                        columns[localization] = columns['Preço (US$)']
                        instances.append(columns)
                        instances_keys.append(columns['Tipo de máquina'])
                    else:
                        index = instances_keys.index(columns['Tipo de máquina'])
                        obj = instances[index]
                        obj[localization] = columns['Preço (US$)']

        self.save_json('google', data)

    def select_option(self, localization):
        """ Selecionando uma opção"""
        options = self.driver.find_elements_by_xpath("//md-option//div[@class='md-text'][contains(text(),'{}')]/.."
                                                     .format(localization))
        for option in options:
            self.driver.execute_script("$('#{}').click()".format(option.get_attribute("id")))
            sleep(2)
            self.driver.execute_script("$('.md-select-backdrop').click()")

    def get_options_localization(self):
        options = []
        options_page = self.driver.find_elements_by_tag_name("md-option")
        for option in options_page:
            if option.text not in options and len(option.text) > 0:
                options.append(option.text)

        return options
