from multiprocessing import Lock

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.Log import Log
from commons.Utils import Utils


class Selenium:

    lock = None  # Utilizado para ter apenas uma execução no selenium por vez
    driver = None

    def __init__(self, url):
        self.lock = Lock()
        self._initialize_driver(url)

    def __del__(self):
        self.driver.close()

    def _initialize_driver(self, url):
        try:
            self.lock.acquire()
            """Initialises the webdriver"""
            capabilities = DesiredCapabilities.FIREFOX.copy()
            self.driver = webdriver.Remote(command_executor="localhost:4444/wd/hub", desired_capabilities=capabilities)

            self.driver.get(url)
            utils = Utils(self.driver)
            utils.wait_for(utils.page_has_loaded)
        finally:
            self.lock.release()

    def get_tables(self):
        tables = None

        try:
            self.lock.acquire()

            """ Buscando tabelas na página de possuem valor ($). O while é para garantir o retorno dos dados """
            while tables is None or len(tables) == 0:
                Log.debug("Buscando dados das tabelas")
                tables = self.driver.find_elements_by_xpath(
                    '//table//td[starts-with(descendant::*/text(), "$") or starts-with(text(), "$")]/../../..')
        finally:
            self.lock.release()

        return tables

    def find_element_by_tag_name(self, element, tag_name):
        try:
            self.lock.acquire()
            result = element.find_element_by_tag_name(tag_name)
        finally:
            self.lock.release()

        return result

    def find_elements_by_tag_name(self, element, tag_name):
        try:
            self.lock.acquire()
            result = element.find_elements_by_tag_name(tag_name)
        finally:
            self.lock.release()

        return result

    def find_elements_by_xpath(self, xpath, element=None):
        if element is None:
            element = self.driver

        try:
            self.lock.acquire()
            result = element.find_elements_by_xpath(xpath)
        finally:
            self.lock.release()

        return result

    def find_element_by_xpath(self, xpath, element=None):
        if element is None:
            element = self.driver

        try:
            self.lock.acquire()
            result = element.find_element_by_xpath(xpath)
        finally:
            self.lock.release()

        return result

    def execute_script(self, script):
        try:
            self.lock.acquire()
            result = self.driver.execute_script(script)
        finally:
            self.lock.release()

        return result
