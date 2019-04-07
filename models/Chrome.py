from multiprocessing import Lock
from requests_html import HTMLSession, HTMLResponse, Element, HTML
from commons.Log import Log


class Chrome:

    lock = Lock()  # Utilizado para ter apenas uma execução no selenium por vez
    driver: HTMLResponse = None
    session: HTMLSession = None

    @staticmethod
    def close_selenium():
        Chrome.session.close()

    @staticmethod
    def initialize_driver():
        try:
            Chrome.lock.acquire()
            Chrome.session = HTMLSession()
        finally:
            Chrome.lock.release()

    @staticmethod
    def get_url(url):
        try:
            Chrome.lock.acquire()
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            Chrome.driver: HTMLResponse = Chrome.session.get(url, headers={'User-Agent': user_agent})
            Chrome.driver.html.render(keep_page=True)
        finally:
            Chrome.lock.release()

    @staticmethod
    def get_tables():
        try:
            Chrome.lock.acquire()

            """ Buscando tabelas na página de possuem valor ($)"""
            Log.debug("Buscando dados das tabelas")
            tables = Chrome.driver.html.xpath(
                '//table//td[starts-with(descendant::*/text(), "$") or starts-with(text(), "$")]/../../..')
        finally:
            Chrome.lock.release()

        return tables

    @staticmethod
    def find_element_by_tag_name(element: Element, tag_name):
        try:
            Chrome.lock.acquire()
            result = element.find(tag_name, first=True)
        finally:
            Chrome.lock.release()

        return result

    @staticmethod
    def find_elements_by_tag_name(element, tag_name):
        try:
            Chrome.lock.acquire()
            result = element.find(tag_name)
        finally:
            Chrome.lock.release()

        return result

    @staticmethod
    def find_elements_by_xpath(xpath, element=None):
        if element is None:
            element = Chrome.driver

        try:
            Chrome.lock.acquire()
            result = element.html.xpath(xpath)
        finally:
            Chrome.lock.release()

        return result

    @staticmethod
    def find_element_by_xpath(xpath, element=None):
        if element is None:
            element = Chrome.driver

        try:
            Chrome.lock.acquire()
            result = element.html.xpath(xpath, first=True)
        finally:
            Chrome.lock.release()

        return result

    @staticmethod
    async def execute_script(script):
        try:
            Chrome.lock.acquire()
            page = Chrome.driver.html.page
            await page.evaluate(script)

            content = await page.content()
            html = HTML(url=Chrome.driver.url, html=content.encode('utf-8'), default_encoding='utf-8')
            Chrome.driver.html.__dict__.update(html.__dict__)
            Chrome.driver.html.page = page
        finally:
            Chrome.lock.release()

    @staticmethod
    async def select_option(selector, option):
        try:
            Chrome.lock.acquire()
            script = '() => { document.getElementById("' + selector + '").value="' + option + '"; ' \
                     'return document.getElementById("' + selector + '").dispatchEvent(new Event("change")); }'
            page = Chrome.driver.html.page
            await page.evaluate(script)

            content = await page.content()
            html = HTML(url=Chrome.driver.url, html=content.encode('utf-8'), default_encoding='utf-8')
            Chrome.driver.html.__dict__.update(html.__dict__)
            Chrome.driver.html.page = page
        finally:
            Chrome.lock.release()

    @staticmethod
    def replace_right(source, target, replacement, replacements=None):
        return replacement.join(source.rsplit(target, replacements))
