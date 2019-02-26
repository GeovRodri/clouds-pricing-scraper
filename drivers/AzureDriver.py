from selenium.webdriver.support.select import Select
from commons.BaseDriver import BaseDriver


class AzureDriver(BaseDriver):

    def __init__(self):
        self.url = "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/"
        super().__init__()

    def get_price(self):
        headers = ['INSTANCE', 'CORE', 'RAM', 'TEMPORARY STORAGE', 'vCPU', 'ACTIVE vCPU / UNDERLYING vCPU',	'GPU']
        data, localizations = {}, []
        locations, instances, instances_keys = [], [], []

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

        self.save_json('oracle', instances)

    def get_options_localization(self, text_element):
        select_localization_element = text_element.find_element_by_xpath("//select[@id='region-selector']")
        select_localization = Select(select_localization_element)
        options_localization = select_localization.options
        return options_localization, select_localization
