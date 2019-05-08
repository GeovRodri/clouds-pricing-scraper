import re
import pymongo
import argparse
import matplotlib
from itertools import cycle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sshtunnel import SSHTunnelForwarder
import plotly.offline as py
import plotly.graph_objs as go


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ssh_host", help='Host SSH', type=str)
    parser.add_argument("ssh_user", help='User SSH', type=str)
    parser.add_argument("ssh_pass", help='Password SSH', type=str)
    parser.add_argument("collection", help='Collection', type=str)

    args = parser.parse_args()
    server = SSHTunnelForwarder(
        args.ssh_host,
        ssh_username=args.ssh_user,
        ssh_password=args.ssh_pass,
        remote_bind_address=('127.0.0.1', 27017)
    )

    server.start()
    client = pymongo.MongoClient('127.0.0.1', server.local_bind_port)
    connection = client['clouds-price']

    alibaba_collection = connection.get_collection(args.collection)
    datas = alibaba_collection.find()

    pricing = {}
    for data in datas:
        date = data['_id']
        del data['_id']

        for key in data:
            item = data[key]
            if 'pricing' not in item:
                continue

            if key not in pricing:
                pricing[key] = {}

            regions = item['pricing']
            for region in regions:
                prices = regions[region]

                if region not in pricing[key]:
                    pricing[key][region] = {}

                if isinstance(prices, dict):
                    for price in prices:
                        if price not in pricing[key][region]:
                            pricing[key][region][price] = {'t': [], 'p': []}

                        pricing[key][region][price]['t'].append(date)

                        idx_start_price = str(prices[price]).find('$')
                        space_idx = str(prices[price]).find(' ')
                        barra_idx = str(prices[price]).find('/')

                        if space_idx == -1:
                            space_idx = 1000

                        if barra_idx == -1:
                            barra_idx = 1000

                        idx_end_price = min(space_idx, barra_idx)
                        extract_price = prices[price][idx_start_price: idx_end_price]
                        print('Before value: {}     after value: {}'.format(prices[price], extract_price))

                        string_price_number = re.sub('[^0-9.,]', '', extract_price)
                        if string_price_number is None or string_price_number == "":
                            string_price_number = "0"

                        price_number = float(string_price_number)
                        pricing[key][region][price]['p'].append(price_number)
                else:
                    if "price" not in pricing[key][region]:
                        pricing[key][region]["price"] = {'t': [], 'p': []}

                    price_number = float(re.sub('[^0-9.,]', '', prices))
                    pricing[key][region]["price"]['t'].append(date)
                    pricing[key][region]["price"]['p'].append(price_number)

    for type_cloud in pricing:
        fig, ax = plt.subplots()
        regions = []
        cycol = cycle('bgrcmk')

        for region in pricing[type_cloud]:
            for price in pricing[type_cloud][region]:
                if (price + "_" + region) not in regions:
                    regions.append((price + "_" + region))

                dates = pricing[type_cloud][region][price]['t']
                prices = pricing[type_cloud][region][price]['p']

                dates = matplotlib.dates.date2num(dates)
                ax.plot(dates, prices, 'b-', c=cycol.__next__(), drawstyle='steps-pre')
                ax.set_xticks(dates)

        lgd = ax.legend(regions, bbox_to_anchor=(0., 1.02, 1., .102), loc='lower center', ncol=2)
        ax.set(xlabel='data (s)', ylabel='preço (p)', title=type_cloud)
        ax.grid()

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d-%m"))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(plt.gca().get_xticklabels(), rotation=45, ha="right")

        plt.tight_layout()
        filename = re.sub('[^A-Za-z0-9]+', '', type_cloud)
        # fig.savefig("graphics/" + args.collection + "/" + filename + ".png", mode="expand")
        fig.savefig("graphics/" + args.collection + "/" + filename + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')

    server.close()


if __name__ == '__main__':
    main()
