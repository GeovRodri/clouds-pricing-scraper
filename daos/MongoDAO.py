import datetime
import pymongo
from pymongo import MongoClient
from commons.Log import Log


class MongoDAO:
    database = None

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.database = client['clouds-price']

    def insert(self, collection_name, columns):
        collection_name = collection_name
        collection_database = self.database[collection_name]

        Log.debug('Adicionando dados da {} ao banco de dados.'.format(collection_name))
        columns['_id'] = datetime.datetime.now()
        collection_database.insert(columns, check_keys=False)

    def find_last(self, collection_name):
        collection_name = collection_name
        collection_database = self.database[collection_name]

        return collection_database.find({}, ).sort("_id", pymongo.DESCENDING).limit(1)

    def get_collections(self):
        return self.database.collection_names()
