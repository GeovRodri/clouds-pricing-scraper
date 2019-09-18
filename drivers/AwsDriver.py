import ijson
from urllib.request import urlopen
from commons.BaseDriver import BaseDriver


class AwsDriver(BaseDriver):

    def __init__(self):
        self.url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json"
        self.collection_name = 'aws'
        super().__init__()

    def is_blank(self, my_string):
        return not (my_string and str(my_string).strip())

    def search(self):
        response = urlopen(self.url)
        pages = ijson.parse(response)
        sku_location = {}

        location = None
        instance_type = None
        sku = None
        operating_system = None
        attributes = {}

        for prefix, event, value in pages:
            if self.is_blank(prefix) is True or self.is_blank(value) is True:
                continue

            if 'products' in prefix and event == 'string':
                prefix_keys = prefix.split('.')
                last_key = str(prefix_keys[(len(prefix_keys) - 1)])

                if 'location' == last_key:
                    location = value
                elif 'instanceType' == last_key:
                    instance_type = value
                    attributes['pricing'] = {}
                elif 'operatingSystem' == last_key:
                    operating_system = value
                elif 'sku' == last_key:
                    """ Ao trocar o sku reiniciar todas as variaveis e inserir os atributos ao dicionario """
                    if sku is not None and sku != value and instance_type is not None and operating_system == 'Linux':
                        self.columns[instance_type] = attributes
                        location = None
                        instance_type = None
                    
                    attributes = {}
                    sku = value

                if sku is not None and location is not None and instance_type is not None:
                    sku_location[sku] = {'location': location, 'instance_type': instance_type}

                if 'attributes' in prefix and 'location' not in prefix and 'instanceType' not in prefix:
                    attributes[last_key] = value

            elif 'terms.OnDemand' in prefix and event == 'string':
                prefix_keys = prefix.split('.')
                index_on_demand = prefix_keys.index('OnDemand')
                offer_key = prefix_keys[(index_on_demand + 1)]

                if offer_key in sku_location:
                    location = sku_location[offer_key]['location']
                    instance_type = sku_location[offer_key]['instance_type']

                    if 'pricePerUnit.USD' in prefix and value != '0.0000000000' and instance_type is not None:
                        self.columns[instance_type]['pricing'][location] = value
