from commons.Log import Log
from daos.MongoDAO import MongoDAO


class BaseDriver:

    url = ''
    collection_name = 'default'
    tables = None
    columns = {}

    def __init__(self):
        self.tables = None
        self.columns = {}

    def get(self):
        try:
            Log.debug('Iniciando processamento dos dados da {}.'.format(self.collection_name))
            self.search()
            self.save_json()
        except Exception as e:
            Log.error('Erro ao buscar os dados da {}: '.format(self.collection_name) + str(e))

    def search(self):
        raise NotImplementedError()

    def save_json(self):
        mongo = MongoDAO(self.collection_name)
        mongo.insert(self.columns)
