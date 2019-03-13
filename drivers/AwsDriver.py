from urllib.request import urlopen

import ijson

from commons.BaseDriver import BaseDriver


class AwsDriver(BaseDriver):

    def __init__(self):
        self.url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json"
        self.name_file = 'aws'
        super().__init__()

    def search(self):
        f = urlopen(self.url)
        products_pages = ijson.items(f, 'products')
        on_demand_pages = ijson.basic_parse(f, 'terms.OnDemand')

        for products in products_pages:
            for product_key in products:
                product = products[product_key]
                sku = product['sku']
                location = product['attributes'].get('location', None)

                instance_type = product['attributes'].get('instanceType', None)
                if instance_type is None:
                    continue

                if instance_type not in self.columns:
                    self.columns[instance_type] = product['attributes']
                    """ Removendo campos de localização """
                    del self.columns[instance_type]['location']
                    del self.columns[instance_type]['locationType']
                    self.columns[instance_type]['pricing'] = {}

                """ Pegando os valores do produto """
                offers = None
                for on_demand in on_demand_pages:
                    on_demand.get(sku, None)

                if offers is not None:
                    offers_keys = list(offers.keys())

                    dimensions = offers[offers_keys[0]]['priceDimensions']
                    dimensions_keys = list(dimensions.keys())
                    price = dimensions[dimensions_keys[0]]['pricePerUnit']['USD']

                    if price != '0.0000000000':
                        self.columns[instance_type]['pricing'][location] = price
