import ijson
from urllib.request import urlopen
from commons.BaseDriver import BaseDriver


class AwsDriver(BaseDriver):

    def __init__(self):
        self.url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json"
        self.collection_name = 'aws'
        super().__init__()

    def search(self):
        response = urlopen(self.url)
        pages = ijson.parse(response)
        sku_location = {}

        location = None
        instance_type = None
        sku = None

        for prefix, event, value in pages:
            if prefix == '':
                continue

            if 'products' in prefix and event == 'string':
                if 'location' == prefix:
                    location = value
                elif 'instanceType' in prefix:
                    instance_type = value
                    self.columns[instance_type] = {}
                    self.columns[instance_type]['pricing'] = {}
                elif 'sku' in prefix:
                    sku = value

                if sku is not None and location is not None and instance_type is not None:
                    sku_location[sku] = {'location': location, 'instance_type': instance_type}

                    if 'attributes' in prefix and 'location' not in prefix and 'instanceType' not in prefix:
                        prefix_keys = prefix.split('.')
                        self.columns[instance_type][prefix_keys[(len(prefix_keys) - 1)]] = value

            elif 'terms.OnDemand' in prefix and event == 'string':
                prefix_keys = prefix.split('.')
                index_on_demand = prefix_keys.index('OnDemand')
                offer_key = prefix_keys[(index_on_demand + 1)]

                location = sku_location[offer_key]['location']
                instance_type = sku_location[offer_key]['instance_type']

                if 'pricePerUnit.USD' in prefix and value != '0.0000000000' and instance_type is not None:
                    self.columns[instance_type]['pricing'][location] = value
