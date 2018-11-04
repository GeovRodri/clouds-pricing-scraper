import configparser
import adal
import os
import requests
from azure.mgmt.commerce.models import RateCardQueryParameters
from msrestazure.azure_active_directory import AADTokenCredentials


class Prices(object):

    def get_price(self):
        currency = 'USD'
        locale = 'en-US'
        region = 'US'

        locations = []
        locations_keys = []

        instances = []
        instances_keys = []

        headers = ['Size', 'Clock speed (ACU/Core)', 'CPU cores;Memory (GiB)', 'Local HDD (GiB)', 'NICs (Max)',
                   'Network bandwidth']

        authority_host_uri = 'https://login.microsoftonline.com'
        tenant = '85bf2e1d-3d45-4132-9d91-c35396e877d4'
        authority_uri = authority_host_uri + '/' + tenant
        resource_uri = 'https://management.core.windows.net/'
        client_id = '34688905-7185-496b-9027-f6e172322810'

        context = adal.AuthenticationContext(authority_uri, api_version=None)
        code = context.acquire_user_code(resource_uri, client_id)
        print(code['message'])
        mgmt_token = context.acquire_token_with_device_code(resource_uri, code, client_id)
        credentials = AADTokenCredentials(mgmt_token, client_id)

        url = "https://management.azure.com:443/subscriptions/2bed4f87-fd56-40e9-9afa-27446d7856d2/providers/Microsoft.Commerce/RateCard?api-version=2016-08-31-preview&$filter=Currency eq '{currencyId}' and Locale eq '{localeId}' and RegionInfo eq '{regionId}'"\
            .format(currencyId=currency, localeId=locale, regionId=region)
        json_prices = requests.get(url, allow_redirects=False, headers={'Authorization': 'Bearer {}'.format(credentials.token['access_token'])})
        print(json_prices)


if __name__ == "__main__":
    prices = Prices()
    prices.get_price()

