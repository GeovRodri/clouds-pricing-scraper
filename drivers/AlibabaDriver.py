from commons.BaseDriver import BaseDriver
from models.Chrome import Chrome


class AlibabaDriver(BaseDriver):

    def __init__(self):
        self.url = "https://www.alibabacloud.com/product/ecs"
        self.collection_name = 'alibaba'
        super().__init__()

    def search(self):
        """ Inicializando selenium """
        Chrome.get_url(self.url)

        localizations = self.get_localizations()
        xpath_products = "//*[contains(@class, 'reseller-band-color')]//div[contains(@class, 'box')]"
        cards = Chrome.find_elements_by_xpath(xpath_products)
        products_os = self.get_os()

        for product_os in products_os:
            self.select_option(product_os)

            for localization in localizations:
                self.select_option(localization)
                index_card = 1

                for card in cards:
                    card_xpath = xpath_products + '[{}]'.format(index_card)
                    price = Chrome.find_element_by_xpath(card_xpath + "//*[contains(@class, 'price')]").text
                    items = Chrome.find_elements_by_xpath(card_xpath + "//li")
                    key = "{}_{}".format(index_card, product_os)

                    if key not in self.columns:
                        self.columns[key] = {}

                    for item in items:
                        """ Pegando o titulo e a valor, como os dois estão juntos estou considerando o que está em negrito
                         é o valor e o restante o titulo"""
                        value = item.find_element_by_tag_name('b').text
                        title = str(item.text).replace(value, '')
                        self.columns[key][title] = value

                    """ Pegando os valores dos produtos"""
                    if 'pricing' not in self.columns[key]:
                        self.columns[key]['pricing'] = {}

                    if localization not in self.columns[key]['pricing']:
                        self.columns[key]['pricing'][localization] = {}

                    self.columns[key]['pricing'][localization]['price'] = price
                    index_card += 1

    def select_option(self, localization):
        select = Chrome.find_element_by_xpath('//a[contains(text(),"{}")]'.format(localization))
        select.click()

    def get_localizations(self):
        options = []
        selects = Chrome.find_elements_by_xpath("//*[contains(@class,'get-regions')]//dd")

        for element in selects:
            options.append(element.text)

        return options

    def get_os(self):
        options = []
        selects = Chrome.find_elements_by_xpath("//*[contains(@class,'get-os')]//dd")

        for element in selects:
            options.append(element.text)

        return options
