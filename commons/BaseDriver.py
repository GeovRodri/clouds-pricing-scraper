import datetime
from pymongo import MongoClient
from commons.Log import Log


class BaseDriver:

    url = ''
    collection_name = 'default'
    tables = None
    columns = {}
    collection_database = None

    def __init__(self):
        client = MongoClient('localhost', 27017)
        database = client['clouds-price']
        self.collection_database = database[self.collection_name]

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
        Log.debug('Adicionando dados da {} ao banco de dados.'.format(self.collection_name))
        self.columns['_id'] = datetime.datetime.now()
        self.collection_database.insert(self.columns, check_keys=False)
