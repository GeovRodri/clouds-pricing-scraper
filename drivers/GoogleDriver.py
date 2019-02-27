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
        titles, columns = [], {}

        """ Pegando o select de seleção de localização """
        localizations = self.get_options_localization()

        for localization in localizations:
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

                    index = 0
                    for td in tds:
                        text_th = titles[index]
                        key = None

                        if index == 0:
                            key = td.text

                        if key not in columns:
                            columns[key] = {}

                        """ Se for um valor agrupar em princing, se não só adicionar como uma coluna """
                        if str(td.text).startswith('$'):
                            if 'pricing' not in columns[key]:
                                columns[key]['pricing'] = {}

                            if localization not in columns[key]['pricing']:
                                columns[key]['pricing'][localization] = {}

                            columns[key]['pricing'][localization][text_th] = td.text
                        else:
                            if text_th not in columns[key]:
                                columns[key][text_th] = {}

                            columns[key][text_th] = td.text

                        index += 1

        self.save_json('google', columns)

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
        options_page = self.driver.find_elements_by_class_name("md-text")
        for option in options_page:
            if option.text not in options and len(option.text) > 0:
                options.append(option.text)

        return options
