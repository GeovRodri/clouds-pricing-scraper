from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.select import Select
from commons.BaseDriver import BaseDriver
from commons.Utils import Utils


class AlibabaDriver(BaseDriver):

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
        print(localizations)

    def select_option(self, localization):
        raise NotImplementedError()

    def get_localizations(self):
        options = []
        elements = self.driver.find_element_by_xpath("//*[contains(@class,'get-regions')]//dd")

        for element in elements:
            options.append(element.text())

        return options
