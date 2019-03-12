from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement

from commons.BaseDriver import BaseDriver
from commons.Utils import Utils


class AlibabaDriver(BaseDriver):

    select = None

    def __init__(self):
        self.url = "https://www.alibabacloud.com/product/ecs"
        self.name_file = 'azure'

        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

        self.driver.get(self.url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)

        super().__init__()

    def search(self):
        localizations = self.get_localizations()
        cards = self.driver.find_elements_by_xpath("//*[contains(@class, 'products ')]//div[contains(@class, 'box')]")

        for localization in localizations:
            self.select_option(localization)

            for card in cards:
                key = card.text.strip()
                itens = card.find_elements_by_tag_name("li")

                """ Pegando os valores dos produtos"""
                if 'pricing' not in self.columns[key]:
                    self.columns[key]['pricing'] = {}

                if localization not in self.columns[key]['pricing']:
                    self.columns[key]['pricing'][localization] = {}

                price = card.find_element_by_xpath("//*[contains(@class, 'price')]")
                self.columns[key]['pricing'][localization]['price'] = price.text

    def select_option(self, localization):
        select = self.select.find_element_by_xpath("//*[contains(text(),'{}')]".format(localization))
        select.click()

    def get_localizations(self):
        options = []
        self.select = self.driver.find_element_by_xpath("//*[contains(@class,'get-regions')]")
        selects = self.driver.find_elements_by_xpath("//dd")

        for element in selects:
            options.append(element.text)

        return options
