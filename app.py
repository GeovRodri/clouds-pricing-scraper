import wtforms_json
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource

from commons.Utils import Utils
from daos.MongoDAO import MongoDAO
from forms import FindCloudsForm

app = Flask(__name__)
api = Api(app)
mongo = MongoDAO()
cors = CORS(app, resources={r"/*": {"origins": "*"}})
wtforms_json.init()


class Prices(Resource):

    def post(self):
        form = FindCloudsForm.from_json(request.json)

        if form.validate() is False:
            return {"errors": form.errors}, 400

        collections = mongo.get_collections()
        result = {}

        for collection_name in collections:
            last_data = list(mongo.find_last(collection_name))[0]
            fields = form.data['select'].get(collection_name, [])
            filters = form.data['filters'].get(collection_name, [])
            items = {}

            if fields is None or len(fields) == 0:
                result[collection_name] = {}
                continue

            del last_data['_id']
            for machine_key in last_data:
                item = {}
                machine = last_data[machine_key]
                remove_machine = False

                for field_list in fields:
                    field_split = str(field_list).split('.')
                    field = field_split[0]
                    field_data = machine.get(field, None)
                    filters_field = [x for x in filters if x["field"] == field]

                    if 'pricing' in field:
                        field_data = self.extract_pricing(field_data, field_split[1])
                        # O filtro de região tem que ser realizada junto a de preço
                        filters_field = filters_field + [x for x in filters if x["field"] == 'region']

                    for filter_field in filters_field:
                        comparator = filter_field["comparator"]
                        field_comparator = ''
                        value_filter = filter_field["value"]

                        if isinstance(field_data, list) is False:
                            field_comparator = "'" + str(field_data) + "'"

                        # Removendo . caso seja um número decimal
                        if str(value_filter).replace('.', '').isnumeric():
                            field_comparator = Utils.only_numbers(field_comparator)
                        else:
                            # Se não for um número, adicionar " para considerar como string na hora do eval
                            value_filter = '"' + value_filter + '"'

                        # Realizando o filtro por preço
                        if 'pricing' in field:
                            prices = []

                            for price_obj in field_data:
                                item_comparator = price_obj['price']

                                if filter_field["field"] == 'region':
                                    item_comparator = '"' + price_obj['region'] + '"'

                                if eval("{} {} {}".format(item_comparator, comparator, value_filter)):
                                    prices.append(price_obj)

                            if len(prices) == 0:
                                remove_machine = True

                            field_data = prices
                            continue

                        if eval("{} {} {}".format(field_comparator, comparator, value_filter)) is False:
                            remove_machine = True

                    if remove_machine is True:
                        break

                    item[field] = field_data

                if remove_machine is False:
                    items[machine_key] = item
            result[collection_name] = items

        return result

    def extract_pricing(self, field_data, field_name):
        pricing_obj = []
        for price_key in field_data:
            price_obj = field_data[price_key]

            if isinstance(price_obj, dict):
                type_price = price_obj[field_name]
                price = Utils.get_price(type_price)
                pricing_obj.append({"region": price_key, "price": price})
            else:
                price = Utils.get_price(price_obj)
                pricing_obj.append({"region": price_key, "price": price})

        return pricing_obj


api.add_resource(Prices, '/')

if __name__ == '__main__':
    app.run(debug=True)
