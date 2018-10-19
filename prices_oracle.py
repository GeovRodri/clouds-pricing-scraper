import json
from pprint import pprint
from time import sleep

import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.select import Select


class PricesDriver(object):

    driver = None

    def __init__(self):
        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

    def get_price(self, url):
        titles, data = [], {}
        self.driver.get(url)
        self.wait_for(self.page_has_loaded)
        # sleep(30)

        text_element = self.driver.find_element_by_xpath("//h4[contains(text(), 'Bare Metal Instances')]/parent::div"
                                                         "/parent::div/parent::div/parent::div/parent::div")

        data["default"] = []
        trs = text_element.find_elements_by_tag_name("tr")

        is_title = True
        for tr in trs:
            columns, index = {}, 0
            tds = tr.find_elements_by_tag_name("td")

            for td in tds:
                if is_title is True:
                    titles.append(td.text)
                else:
                    text_th = titles[index]
                    columns[text_th] = td.text
                    index += 1

            if is_title is True:
                is_title = False
            else:
                data["default"].append(columns)

        """ Convertendo para JSON e imprimindo na tela """
        data_json = json.dumps(data, indent=4)
        pprint(data_json)
        self.driver.close()

    def wait_for(self, condition_function):
        start_time = time.time()
        while time.time() < start_time + 3:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception('Timeout waiting for {}'.format(condition_function.__name__))

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

if __name__ == "__main__":
    prices_drive = PricesDriver()
    prices_drive.get_price("https://cloud.oracle.com/iaas/pricing")

