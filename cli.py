import argparse
from drivers.AlibabaDriver import AlibabaDriver
from drivers.AwsDriver import AwsDriver
from drivers.AzureDriver import AzureDriver
from drivers.GoogleDriver import GoogleDriver
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
    elif args.cloud == 'google':
        prices_drive = GoogleDriver()
    elif args.cloud == 'alibaba':
        prices_drive = AlibabaDriver()
    elif args.cloud == 'oracle':
        prices_drive = OracleDriver()

    prices_drive.get()


if __name__ == '__main__':
    main()
