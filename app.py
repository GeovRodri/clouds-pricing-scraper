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
                remove_machine = False
                machine = last_data[machine_key]
                item, general_configurations, price_configurations = {}, {}, []

                """ Montando o objeto """
                for field_list in fields:
                    field_split = str(field_list).split('.')
                    field = field_split[0]
                    field_data = machine.get(field, None)

                    if 'pricing' in field:
                        price_configurations = self.extract_pricing(field_data, field_split[1])

                item = [{**general_configurations, **x} for x in price_configurations]

                """ Realizando a filtragem dos resultados """
                for filter_obj in filters:
                    field_filter = filter_obj["field"]
                    comparator = filter_obj["comparator"]
                    value_filter = filter_obj["value"]

                    field_data = "'" + item.get(field_filter, None) + "'"

                    # Removendo . caso seja um número decimal
                    if str(value_filter).replace('.', '').isnumeric():
                        field_data = Utils.only_numbers(field_data)
                    else:
                        # Se não for um número, adicionar " para considerar como string na hora do eval
                        value_filter = '"' + value_filter + '"'

                    if eval("{} {} {}".format(field_data, comparator, value_filter)) is False:
                        remove_machine = True

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
