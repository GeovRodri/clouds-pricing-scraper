import argparse

from drivers.AwsDriver import AwsDriver
from drivers.AzureDriver import AzureDriver
from drivers.CtlDriver import CtlDriver
from drivers.GoogleDriver import GoogleDriver
from drivers.IbmDriver import IbmDriver
from drivers.OracleDriver import OracleDriver


def main():
    parser = argparse.ArgumentParser()
    prices_drive = None

    parser.add_argument("cloud", help='Digite a cloud desejada', type=str)

    args = parser.parse_args()
    if args.cloud == 'aws':
        prices_drive = AwsDriver()
    elif args.cloud == 'azure':
        prices_drive = AzureDriver()
    elif args.cloud == 'ctl':
        prices_drive = CtlDriver()
    elif args.cloud == 'google':
        prices_drive = GoogleDriver()
    elif args.cloud == 'ibm':
        prices_drive = IbmDriver()
    elif args.cloud == 'oracle':
        prices_drive = OracleDriver()

    prices_drive.get_price()


if __name__ == '__main__':
    main()
