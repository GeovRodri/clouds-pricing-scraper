from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.BaseDriver import BaseDriver
from commons.Utils import Utils


class AlibabaDriver(BaseDriver):

    def __init__(self):
        self.url = "https://www.alibabacloud.com/product/ecs"
        self.name_file = 'alibaba'

        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

        self.driver.get(self.url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)
        super().__init__()

    def __del__(self):
        self.driver.close()

    def search(self):
        localizations = self.get_localizations()

        for localization in localizations:
            cards = self.driver.find_elements_by_xpath("//*[contains(@class, 'products')]//div[contains(@class, 'box')]")
            self.select_option(localization)

            for card in cards:
                price = card.find_element_by_xpath("//*[contains(@class, 'price')]").text
                """ considerando a key como price """
                key = price
                items = card.find_elements_by_tag_name("li")

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

    def select_option(self, localization):
        self.driver.execute_script("$(\".get-regions a:contains('{}')\")[0].click()".format(localization))

    def get_localizations(self):
        options = []
        selects = self.driver.find_elements_by_xpath("//*[contains(@class,'get-regions')]//dd")

        for element in selects:
            options.append(element.text)

        return options
