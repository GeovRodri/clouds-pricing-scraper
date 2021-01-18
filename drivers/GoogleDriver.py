import asyncio
from time import sleep

from requests_html import HTML

from commons.BaseSeleniumDriver import BaseSeleniumDriver
from commons.Log import Log
from models.Chrome import Chrome


class GoogleDriver(BaseSeleniumDriver):

    def __init__(self):
        self.url = "https://cloud.google.com/compute/all-pricing"
        self.collection_name = 'google'
        super().__init__()


    def search(self):
        titles = []

        # Inicializando a sessão e pegando as tabelas
        Chrome.get_url(self.url, self.after_load_url)
        frames = Chrome.driver.html.page.frames

        for index, frame in enumerate(frames):
            if frame.url == self.url or frame.url == 'about:blank':
                continue

            html = asyncio.get_event_loop().run_until_complete(frame.content())
            if 'Machine type' not in html:
                continue

            Log.debug(f'Frame {index} de {len(frames)}')
            Chrome.driver._html = HTML(session=frame, url=frame.url, html=html)
            Chrome.driver._html.page = frame

            """ Pegando o select de seleção de localização """
            localizations = self.get_localizations()

            """ Interagindo sobre as localizações """
            idx = 0
            for localization in localizations:
                idx += 1
                Log.debug('Mudando a localização para {}. {} de {}'.format(localization, idx, len(localizations)))
                """ Selecionando a opção para processar as informações dela """
                self.select_option(localization)
                self.tables = Chrome.get_tables()

                for table in self.tables:
                    self.process_table(table, titles, localization)


    def select_option(self, localization):
        """ Selecionando uma opção"""
        options = Chrome.find_elements_by_xpath("//md-option//div[@class='md-text'][contains(text(),'{}')]/.."
                                                .format(localization))
        for option in options:
            asyncio.get_event_loop().run_until_complete(
                Chrome.execute_script("() => document.getElementById('{}').click()".format(option.attrs['id'])))
            sleep(2)
            asyncio.get_event_loop().run_until_complete(
                Chrome.execute_script("() => { "
                                      "         var element = document.getElementsByClassName('md-select-backdrop')[0];"
                                      "         if (element) element.click(); "
                                      "} "))

    def get_localizations(self):
        options = []
        options_page = Chrome.find_elements_by_xpath("//md-option//div[@class='md-text']")
        for option in options_page:
            text = option.text
            if text not in options and len(text) > 0:
                options.append(text)

        return options
