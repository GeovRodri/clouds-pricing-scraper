import asyncio
from time import sleep
from commons.BaseSeleniumDriver import BaseSeleniumDriver
from models.Chrome import Chrome


class GoogleDriver(BaseSeleniumDriver):

    def __init__(self):
        self.url = "https://cloud.google.com/compute/pricing"
        self.collection_name = 'google'
        super().__init__()

    def select_option(self, localization):
        """ Selecionando uma opção"""
        options = Chrome.find_elements_by_xpath("//md-option//div[@class='md-text'][contains(text(),'{}')]/.."
                                                .format(localization))
        for option in options:
            asyncio.get_event_loop().run_until_complete(
                Chrome.execute_script("() => document.getElementById('{}').click()".format(option.attrs['id'])))
            sleep(2)
            asyncio.get_event_loop().run_until_complete(
                Chrome.execute_script("() => { "
                                      "         var element = document.getElementsByClassName('md-select-backdrop')[0];"
                                      "         if (element) element.click(); "
                                      "} "))

    def get_localizations(self):
        options = []
        options_page = Chrome.find_elements_by_xpath("//md-option//div[@class='md-text']")
        for option in options_page:
            text = option.text
            if text not in options and len(text) > 0:
                options.append(text)

        return options
