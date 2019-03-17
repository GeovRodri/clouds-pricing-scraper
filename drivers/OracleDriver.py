from commons.BaseSeleniumDriver import BaseSeleniumDriver


class OracleDriver(BaseSeleniumDriver):

    def __init__(self):
        self.url = 'https://cloud.oracle.com/iaas/pricing'
        self.collection_name = 'oracle'
        super().__init__()

    def select_option(self, localization):
        pass

    def get_localizations(self):
        return ['default']
