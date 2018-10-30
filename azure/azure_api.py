import csv
import json
import requests


class Prices(object):

    def get_price(self):
        locations = []
        locations_keys = []

        instances = []
        instances_keys = []

        headers = ['Size', 'Clock speed (ACU/Core)', 'CPU cores;Memory (GiB)', 'Local HDD (GiB)', 'NICs (Max)',
                   'Network bandwidth']

        # url = 'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json'
        # json_prices = requests.get(url)
        json_prices = open('aws.json').read()

        all_prices = json.loads(json_prices)
        products = all_prices['products']
        on_demand = all_prices['terms']['OnDemand']

        for product_key in products:
            product = products[product_key]

            sku = product['sku']
            location = product['attributes'].get('location', None)
            if location is None:
                continue

            if location not in locations_keys:
                locations.append({'Name': location})
                locations_keys.append(location)

            instance_type = product['attributes'].get('instanceType', None)

            if instance_type not in instances_keys:
                obj = {
                    'Instance Type': product['attributes'].get('instanceType', None),
                    'GPUs': instance_type,
                    'vCPU': product['attributes'].get('vcpu', None),
                    'Memory (GiB)': product['attributes'].get('memory', None),
                    'Storage (GB)': product['attributes'].get('storage', None),
                    'Networking Performance': product['attributes'].get('networkPerformance', None),
                    'Physical Processor': product['attributes'].get('physicalProcessor', None),
                    'Clock Speed (GHz)': product['attributes'].get('clockSpeed', None),
                    'Intel AVX': product['attributes'].get('intelAvxAvailable', '-'),
                    'Intel AVX2': product['attributes'].get('intelAvx2Available', '-'),
                    'Intel Turbo': product['attributes'].get('intelTurboAvailable', '-'),
                    'EBS OPT': product['attributes'].get('ebsOptimized', '-'),
                    'Enhanced Network': product['attributes'].get('enhancedNetworkingSupported', '-')
                }

                instances.append(obj)
                instances_keys.append(instance_type)
            else:
                index = instances_keys.index(instance_type)
                obj = instances[index]

            offers = on_demand.get(sku, None)

            if offers is not None:
                offers_keys = list(offers.keys())

                dimensions = offers[offers_keys[0]]['priceDimensions']
                dimensions_keys = list(dimensions.keys())

                obj[location] = dimensions[dimensions_keys[0]]['pricePerUnit']['USD']

        with open('AWS_Regions.csv', 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=list(locations[0].keys()), delimiter=';')
            w.writeheader()
            w.writerows(locations)

        with open('AWS.csv', 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.DictWriter(f, fieldnames=headers + locations_keys, delimiter=';')
            w.writeheader()
            w.writerows(instances)


if __name__ == "__main__":
    prices = Prices()
    prices.get_price()

