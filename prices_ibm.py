import json
from pprint import pprint
from time import sleep

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.select import Select


class PricesDriver(object):

    driver = None
    capabilities = None

    def __init__(self):
        """Initialises the webdriver"""
        self.capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=self.capabilities)

    def get_price(self, url):
        titles, data = ['processor', 'memory ram', 'hard drives', 'network' 'price', 'price'], {}
        self.driver.get(url)
        self.wait_for(self.page_has_loaded)

        """ A IBM trabalha com um ifram dentro do site, então antes de fazer tudo tem que pegar esse iframe"""
        frames = self.driver.find_elements_by_tag_name("iframe")
        for frame in frames:
            src_fram = frame.get_attribute('src')
            driver_frame = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                            desired_capabilities=self.capabilities)
            driver_frame.get(src_fram)
            sleep(10)
            print(driver_frame.page_source)
            print('---------------------------------------------------------------------')

            try:
                text_element = self.driver.find_element_by_xpath("//div[@class='view-content']")
            except NoSuchElementException:
                """ Como se tem vários frames, se não tiver o elemento ir para o proximo """
                driver_frame.close()
                continue

            if text_element is not None:
                """ Pegando o select de seleção de localização """
                options_localization, select_localization = self.get_options_localization()

                for option_localization in options_localization:
                    data[option_localization.text] = []

                    """ Selecionando uma opção"""
                    select_localization.select_by_value(option_localization.get_attribute("value"))
                    self.wait_for(self.page_has_loaded)

                    cards = text_element.find_elements_by_tag_name("ibm-card")

                    for card in cards:
                        columns, index = {}, 0
                        columns['name'] = card.find_element_by_tag_name("h4")
                        lis = card.find_elements_by_tag_name("li")

                        for li in lis:
                            columns[titles[index]].append(li.text)
                            index += 1

                        data[option_localization.text].append(columns)

                """ Convertendo para JSON e imprimindo na tela """
                data_json = json.dumps(data, indent=4)
                pprint(data_json)
                driver_frame.close()

        self.driver.close()

    def get_options_localization(self):
        form_element = self.driver.find_element_by_xpath("//form")

        select_localization_element = form_element.find_element_by_tag_name("select")
        select_localization = Select(select_localization_element)
        options_localization = select_localization.options
        return options_localization, select_localization

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

