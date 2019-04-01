from selenium.common.exceptions import WebDriverException

from commons.BaseDriver import BaseDriver
from commons.Log import Log
from models.Selenium import Selenium


class BaseSeleniumDriver(BaseDriver):

    url = ''
    collection_name = 'default'
    tables = None

    def search(self):
        titles = []

        """ Inicializando selenium """
        Selenium.get_url(self.url)
        self.tables = Selenium.get_tables()

        """ Pegando o select de seleção de localização """
        localizations = self.get_localizations()

        """ Interagindo sobre as localizações """
        idx = 0
        for localization in localizations:
            idx += 1
            Log.debug('Mudando a localização para {}. {} de {}'.format(localization, idx, len(localizations)))
            """ Selecionando a opção para processar as informações dela """
            self.select_option(localization)

            for table in self.tables:
                # Se der erro no selenium restartar o processamento
                success = False

                while success is False:
                    try:
                        self.process_table(table, titles, localization)
                        success = True
                    except WebDriverException as e:
                        Log.error("Erro ao buscar uma table. Erro: {}".format(str(e)))
                        Selenium.get_url(self.url)

    def process_table(self, table, titles, localization):
        thead = Selenium.find_element_by_tag_name(table, "thead")
        tbody = Selenium.find_element_by_tag_name(table, "tbody")

        """ Buscando as colunas. Tem sites que utilizam o td no lugar do th """
        ths = Selenium.find_elements_by_tag_name(thead, "th")
        if len(ths) <= 0:
            ths = Selenium.find_elements_by_tag_name(thead, "td")

        for th in ths:
            if th.text not in titles:
                titles.append(th.text)

        trs_body = Selenium.find_elements_by_tag_name(tbody, "tr")
        for tr in trs_body:
            tds = Selenium.find_elements_by_tag_name(tr, "td")
            index, key = 0, None

            for td in tds:
                text_th = titles[index]
                index += 1

                # pulando itens que não possuem texto. Ex: botões na tabela
                if td.text == "" or td.text is None:
                    continue

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

    def select_option(self, localization):
        raise NotImplementedError()

    def get_localizations(self):
        raise NotImplementedError()
