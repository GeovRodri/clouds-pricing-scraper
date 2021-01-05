import asyncio
from time import sleep

from commons.BaseSeleniumDriver import BaseSeleniumDriver
from models.Chrome import Chrome


class AlibabaDriver(BaseSeleniumDriver):

    def __init__(self):
        self.url = "https://www.alibabacloud.com/product/ecs-pricing-list/en"
        self.collection_name = 'alibaba'
        super().__init__()

    def select_option(self, localization):
        asyncio.get_event_loop().run_until_complete(Chrome.click_using_text_and_tag(localization, 'button'))
        sleep(2)

    def get_localizations(self):
        asyncio.get_event_loop().run_until_complete(Chrome.click_using_text_and_tag('Mid East And India', 'div'))
        asyncio.get_event_loop().run_until_complete(Chrome.click_using_text_and_tag('Europe And America', 'div'))
        selects = asyncio.get_event_loop().run_until_complete(Chrome.driver.html.page.evaluate('REGION_DATA'))
        return [_['label'] for _ in selects.values()]
