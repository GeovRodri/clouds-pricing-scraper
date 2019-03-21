import datetime
from pymongo import MongoClient
from commons.Log import Log


class MongoDAO:

    collection_database = None
    collection_name = None

    def __init__(self, collection_name):
        client = MongoClient('localhost', 27017)
        database = client['clouds-price']
        self.collection_name = collection_name
        self.collection_database = database[collection_name]

    def insert(self, columns):
        Log.debug('Adicionando dados da {} ao banco de dados.'.format(self.collection_name))
        columns['_id'] = datetime.datetime.now()
        self.collection_database.insert(columns, check_keys=False)
