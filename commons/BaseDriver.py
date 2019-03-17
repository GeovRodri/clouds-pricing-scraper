import datetime
import json
import os

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from commons.Utils import Utils


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
        self.search()
        self.save_json()

    def search(self):
        raise NotImplementedError()

    def save_json(self):
        self.columns['_id'] = datetime.datetime.now()
        self.collection_database.insert(self.columns, check_keys=False)
