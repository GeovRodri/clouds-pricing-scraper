from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.Utils import Utils


class BaseDriver:

    url = ''
    driver = None

    def __init__(self):
        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

        self.driver.get(self.url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
