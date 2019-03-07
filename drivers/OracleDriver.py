from commons.BaseDriver import BaseDriver


class OracleDriver(BaseDriver):

    def __init__(self):
        self.url = 'https://cloud.oracle.com/iaas/pricing'
        self.name_file = 'oracle'
        super().__init__()

    def select_option(self, localization):
        pass

    def get_localizations(self):
        return ['default']
