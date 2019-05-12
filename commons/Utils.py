import re


class Utils:

    @staticmethod
    def get_price(price):
        idx_start_price = str(price).find('$')
        space_idx = str(price).find(' ')
        barra_idx = str(price).find('/')

        if idx_start_price == -1:
            idx_start_price = 0

        if space_idx == -1:
            space_idx = 1000

        if barra_idx == -1:
            barra_idx = 1000

        idx_end_price = min(space_idx, barra_idx)
        extract_price = price[idx_start_price: idx_end_price]

        string_price_number = re.sub('[^0-9.,]', '', extract_price)
        if string_price_number is None or string_price_number == "":
            string_price_number = "0"

        return float(string_price_number)

    @staticmethod
    def only_numbers(price):
        string = re.sub('[^0-9.,]', '', price)
        string = string.replace(',', '.')

        if string is None or string == "":
            string = "0"

        return float(string)
