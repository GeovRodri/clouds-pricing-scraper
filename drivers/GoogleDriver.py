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
                self.driver.execute_script("$('.md-select-backdrop').click()")

            for table in tables:
                finish = False

                trs = table.find_elements_by_tag_name("tr")
                for tr in trs:
                    if finish is True:
                        continue

                    tds = tr.find_elements_by_tag_name("td")

                    """ Verificando se é td(valores) ou th(titulos) """
                    if len(tds) > 0:
                        if len(tds) != 5:
                            continue

                        columns, index = {}, 0

                        for td in tds:
                            text_th = titles[index]
                            if text_th not in columns:
                                columns[text_th] = []

                            columns[text_th] = td.text
                            index += 1

                        if columns['Tipo de máquina'] is not None and columns['Preço (US$)'] is not None \
                                and columns['Memória'] is not None:
                            data[localization].append(columns)

                            if columns['Tipo de máquina'] not in instances_keys:
                                columns[localization] = columns['Preço (US$)']
                                instances.append(columns)
                                instances_keys.append(columns['Tipo de máquina'])
                            else:
                                index = instances_keys.index(columns['Tipo de máquina'])
                                obj = instances[index]
                                obj[localization] = columns['Preço (US$)']
                    else:
                        ths = tr.find_elements_by_tag_name("th")
                        if len(ths) != 5 or ths[1].text == 'Item':
                            finish = True
                            continue

                        for th in ths:
                            if th.text not in titles:
                                titles.append(th.text)

        """ Convertendo para JSON e imprimindo na tela """
        data_json = json.dumps(data, indent=4)
        pprint(data_json)

        with open('Google_Regions.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=list(locations[0].keys()), delimiter=';')
            w.writeheader()
            w.writerows(locations)

        with open('Google.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            titles.remove('Preço (US$)')
            titles.remove('Preço preemptivo (US$)')

            w = csv.DictWriter(f, fieldnames=titles + localizations, delimiter=';')
            w.writeheader()
            for instance in instances:
                del instance['Preço (US$)']
                del instance['Preço preemptivo (US$)']
                w.writerow(instance)

    def get_options_localization(self):
        options = []
        options_name = []

        options_page = self.driver.find_elements_by_tag_name("md-option")
        for option in options_page:
            if option.text not in options and len(option.text) > 0:
                options.append(option.text)
                options_name.append({'Name': option.text})

        return options, options_name
