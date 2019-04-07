import asyncio

from commons.BaseSeleniumDriver import BaseSeleniumDriver
from models.Chrome import Chrome


class AzureDriver(BaseSeleniumDriver):

    def __init__(self):
        self.url = "https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/"
        self.collection_name = 'azure'
        super().__init__()

    def select_option(self, localization):
        """ Selecionando uma opção"""
        option = Chrome.find_elements_by_xpath("//select[@id='region-selector']//option[text() = '{}']"
                                               .format(localization))[0]
        asyncio.get_event_loop().run_until_complete(Chrome.select_option("region-selector", option.attrs['value']))

    def get_localizations(self):
        options = []
        options_elements = Chrome.find_elements_by_xpath("//select[@id='region-selector']//option")

        for option in options_elements:
            options.append(option.text)

        return options
