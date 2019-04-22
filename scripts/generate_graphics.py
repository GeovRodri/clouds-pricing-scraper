import re
from itertools import cycle

import matplotlib
import numpy
import pymongo
import argparse
import matplotlib.pyplot as plt
from sshtunnel import SSHTunnelForwarder
from datetime import timedelta, datetime
import matplotlib.dates as mdates


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
            if key not in pricing:
                pricing[key] = {}

            item = data[key]
            regions = item['pricing']
            for region in regions:
                prices = regions[region]

                if region not in pricing[key]:
                    pricing[key][region] = {}

                if isinstance(prices, list):
                    for price in prices:
                        if price not in pricing[key][region]:
                            pricing[key][region][price] = {'t': [], 'p': []}

                        pricing[key][region][price]['t'].append(date)

                        price_number = float(re.sub('[^0-9.,]', '', prices[price]))
                        pricing[key][region][price]['p'].append(price_number)
                else:
                    price_number = float(re.sub('[^0-9.,]', '', prices))
                    pricing[key][region]["price"] = {'t': [date], 'p': [price_number]}

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
                ax.plot_date(dates, prices, 'b-', c=cycol.__next__(), drawstyle='steps-pre')
                ax.set_xticks(dates)

        ax.legend(regions, bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set(xlabel='data (s)', ylabel='preço (p)', title=type_cloud)
        ax.grid()

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%d"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%Y-%d"))
        _ = plt.xticks(rotation=90)

        fig.savefig("graphics/" + args.collection + "/" + type_cloud + ".png")
        plt.show()

    server.close()


if __name__ == '__main__':
    main()
