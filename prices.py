import json
from pprint import pprint
from time import sleep
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
        sleep(30)

        text_element = self.driver.find_element_by_xpath("//h3[text() = 'Bare Metal']"
                                                         "/parent::div"
                                                         "/parent::div[@class='row']")
        options_localization, select_localization = self.get_options_localization(text_element)

        for option_localization in options_localization:
            data[option_localization.text] = []

            select_localization.select_by_value(option_localization.get_attribute("value"))
            trs = text_element.find_elements_by_tag_name("tr")

            for tr in trs:
                tds = tr.find_elements_by_tag_name("td")
                if len(tds) > 0:
                    columns = {}
                    index = 0

                    for td in tds:
                        text_th = titles[index]
                        if text_th not in columns:
                            columns[text_th] = []

                        columns[text_th].append(td.text)
                        index += 1

                    data[option_localization.text].append(columns)
                else:
                    ths = tr.find_elements_by_tag_name("th")
                    for th in ths:
                        text_th = th.text
                        titles.append(text_th)

        data_json = json.dumps(data, indent=4)
        pprint(data_json)
        self.driver.close()

    def get_options_localization(self, text_element):
        select_localization_element = text_element.find_element_by_tag_name("select")
        select_localization = Select(select_localization_element)
        options_localization = select_localization.options
        return options_localization, select_localization


if __name__ == "__main__":
    prices_drive = PricesDriver()
    prices_drive.get_price("https://www.ctl.io/pricing/")

