from selenium.webdriver.support.select import Select
from commons.BaseSeleniumDriver import BaseSeleniumDriver
from models.Selenium import Selenium


class AzureDriver(BaseSeleniumDriver):

    def __init__(self):
        self.url = "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/"
        self.collection_name = 'azure'
        super().__init__()

    def select_option(self, localization):
        """ Selecionando uma opção"""
        select_localization_element = Select(Selenium.find_element_by_xpath("//select[@id='region-selector']"))
        select_localization_element.select_by_visible_text(localization)

    def get_localizations(self):
        options = []
        select_localization_element = Selenium.find_element_by_xpath("//select[@id='region-selector']")
        select_localization = Select(select_localization_element)

        for option in select_localization.options:
            options.append(option.text)

        return options
