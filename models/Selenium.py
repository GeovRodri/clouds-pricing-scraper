from multiprocessing import Lock

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.Log import Log
from commons.Utils import Utils


class Selenium:

    lock = Lock()  # Utilizado para ter apenas uma execução no selenium por vez
    driver = None

    def __del__(self):
        self.driver.close()

    @staticmethod
    def initialize_driver():
        try:
            Selenium.lock.acquire()
            """Initialises the webdriver"""
            capabilities = DesiredCapabilities.FIREFOX.copy()
            Selenium.driver = webdriver.Remote(command_executor="localhost:4444/wd/hub", desired_capabilities=capabilities)
        finally:
            Selenium.lock.release()

    @staticmethod
    def get_url(url):
        Selenium.driver.get(url)
        utils = Utils(Selenium.driver)
        utils.wait_for(utils.page_has_loaded)

    @staticmethod
    def get_tables():
        tables = None

        try:
            Selenium.lock.acquire()

            """ Buscando tabelas na página de possuem valor ($). O while é para garantir o retorno dos dados """
            while tables is None or len(tables) == 0:
                Log.debug("Buscando dados das tabelas")
                tables = Selenium.driver.find_elements_by_xpath(
                    '//table//td[starts-with(descendant::*/text(), "$") or starts-with(text(), "$")]/../../..')
        finally:
            Selenium.lock.release()

        return tables

    @staticmethod
    def find_element_by_tag_name(element, tag_name):
        try:
            Selenium.lock.acquire()
            result = element.find_element_by_tag_name(tag_name)
        finally:
            Selenium.lock.release()

        return result

    @staticmethod
    def find_elements_by_tag_name(element, tag_name):
        try:
            Selenium.lock.acquire()
            result = element.find_elements_by_tag_name(tag_name)
        finally:
            Selenium.lock.release()

        return result

    @staticmethod
    def find_elements_by_xpath(xpath, element=None):
        if element is None:
            element = Selenium.driver

        try:
            Selenium.lock.acquire()
            result = element.find_elements_by_xpath(xpath)
        finally:
            Selenium.lock.release()

        return result

    @staticmethod
    def find_element_by_xpath(xpath, element=None):
        if element is None:
            element = Selenium.driver

        try:
            Selenium.lock.acquire()
            result = element.find_element_by_xpath(xpath)
        finally:
            Selenium.lock.release()

        return result

    @staticmethod
    def execute_script(script):
        try:
            Selenium.lock.acquire()
            result = Selenium.driver.execute_script(script)
        finally:
            Selenium.lock.release()

        return result
