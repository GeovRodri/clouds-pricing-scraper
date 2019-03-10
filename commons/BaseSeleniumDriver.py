from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.BaseDriver import BaseDriver
from commons.Utils import Utils


class BaseSeleniumDriver(BaseDriver):

    url = ''
    name_file = 'default'
    driver = None
    tables = None
    columns = {}

    def __init__(self):
        """Initialises the webdriver"""
        capabilities = DesiredCapabilities.FIREFOX.copy()
        self.driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub",
                                       desired_capabilities=capabilities)

        self.driver.get(self.url)
        utils = Utils(self.driver)
        utils.wait_for(utils.page_has_loaded)

        """ Buscando tabelas na página de possuem valor ($). O while é para garantir o retorno dos dados """
        while self.tables is None:
            self.tables = self.driver.find_elements_by_xpath(
                '//table//td[starts-with(descendant::*/text(), "$") or starts-with(text(), "$")]/../../..')

    def __del__(self):
        self.driver.close()

    def search(self):
        titles = []

        """ Pegando o select de seleção de localização """
        localizations = self.get_localizations()

        """ Interagindo sobre as localizações """
        for localization in localizations:
            """ Selecionando a opção para processar as informações dela """
            self.select_option(localization)

            for table in self.tables:
                thead = table.find_element_by_tag_name("thead")
                tbody = table.find_element_by_tag_name("tbody")

                """ Buscando as colunas. Tem sites que utilizam o td no lugar do th """
                ths = thead.find_elements_by_tag_name("th")
                if len(ths) <= 0:
                    ths = thead.find_elements_by_tag_name("td")

                for th in ths:
                    if th.text not in titles:
                        titles.append(th.text)

                trs_body = tbody.find_elements_by_tag_name("tr")
                for tr in trs_body:
                    tds = tr.find_elements_by_tag_name("td")
                    index, key = 0, None

                    for td in tds:
                        text_th = titles[index]

                        if key is None:
                            key = td.text

                        if key not in self.columns:
                            self.columns[key] = {}

                        """ Se for um valor agrupar em princing, se não só adicionar como uma coluna """
                        if str(td.text).startswith('$'):
                            if 'pricing' not in self.columns[key]:
                                self.columns[key]['pricing'] = {}

                            if localization not in self.columns[key]['pricing']:
                                self.columns[key]['pricing'][localization] = {}

                            self.columns[key]['pricing'][localization][text_th] = td.text
                        else:
                            if text_th not in self.columns[key]:
                                self.columns[key][text_th] = {}

                            self.columns[key][text_th] = td.text

                        index += 1

    def select_option(self, localization):
        raise NotImplementedError()

    def get_localizations(self):
        raise NotImplementedError()
