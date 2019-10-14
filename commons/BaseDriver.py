import csv

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
        # mongo = MongoDAO()
        # mongo.insert(self.collection_name, self.columns)
        locations = []
        instances = []
        headers = []

        for item in self.columns:
            if self.collection_name == 'aws':
                obj = {
                    'Instance Type': self.columns[item].get('instanceType', None),
                    'vCPU': self.columns[item].get('vcpu', None),
                    'Memory (GiB)': self.columns[item].get('memory', None),
                    'Storage (GB)': self.columns[item].get('storage', None),
                    'Networking Performance': self.columns[item].get('networkPerformance', None),
                    'Physical Processor': self.columns[item].get('physicalProcessor', None),
                    'Clock Speed (GHz)': self.columns[item].get('clockSpeed', None),
                    'Intel AVX': self.columns[item].get('intelAvxAvailable', '-'),
                    'Intel AVX2': self.columns[item].get('intelAvx2Available', '-'),
                    'Intel Turbo': self.columns[item].get('intelTurboAvailable', '-'),
                    'EBS OPT': self.columns[item].get('ebsOptimized', '-'),
                    'Enhanced Network': self.columns[item].get('enhancedNetworkingSupported', '-')
                }
            else:
                obj = self.columns[item].copy()
                del obj['pricing']

            headers = list(set(headers) | set(obj.keys()))

            for x in self.columns[item].get('pricing', []):
                if self.collection_name == 'azure':
                    if 'Pay as you go' in obj:
                        del obj['Pay as you go']

                    if 'One year reserved\n(% Savings)' in obj:
                        del obj['One year reserved\n(% Savings)']

                    if 'Three year reserved\n(% Savings)' in obj:
                        del obj['Three year reserved\n(% Savings)']

                    if 'Pay as you go' in self.columns[item]['pricing'][x]:
                        obj[x] = self.columns[item]['pricing'][x].get('Pay as you go', None)
                elif self.collection_name == 'google':
                    if 'Preço (US$)' in self.columns[item]['pricing'][x]:
                        obj[x] = self.columns[item]['pricing'][x].get('Preço (US$)', None)
                else:
                    obj[x] = self.columns[item]['pricing'][x]

                exists = [y for y in locations if y['name'] == x]
                if len(exists) == 0:
                    locations.append({'name': x})

            instances.append(obj)

        for item in instances:
            for header in headers:
                if header not in item:
                    item[header] = 'N/A'

        with open(f'{self.collection_name}_Regions.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=list(locations[0].keys()), delimiter=';')
            w.writeheader()
            w.writerows(locations)

        with open(f'{self.collection_name}.csv', 'w', newline='', encoding='utf-8') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=headers, delimiter=';')
            w.writeheader()
            w.writerows(instances)
