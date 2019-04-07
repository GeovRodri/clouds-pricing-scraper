import asyncio
from time import sleep

from commons.BaseSeleniumDriver import BaseSeleniumDriver
from models.Chrome import Chrome


class OracleDriver(BaseSeleniumDriver):

    def __init__(self):
        self.url = 'https://cloud.oracle.com/iaas/pricing'
        self.collection_name = 'oracle'
        super().__init__()

    def select_option(self, localization):
        pass

    def get_localizations(self):
        return ['default']

    def after_load_url(self):
        sleep(5)
        asyncio.get_event_loop().run_until_complete(Chrome.execute_script('() => document.documentElement.innerHTML'))
