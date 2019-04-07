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
            Chrome.execute_script("$('#{}').click()".format(option.get_attribute("id")))
            sleep(2)
            Chrome.execute_script("$('.md-select-backdrop').click()")

    def get_localizations(self):
        options = []
        options_page = Chrome.find_elements_by_xpath("//md-option//div[@class='md-text']")
        for option in options_page:
            text = option.get_attribute('textContent')
            if text not in options and len(text) > 0:
                options.append(text)

        return options
