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

                for field in fields:
                    field_data = machine.get(field, None)
                    filters_field = [x for x in filters if x["field"] == field]

                    if 'pricing' in field:
                        field_data = self.extract_pricing(field_data)

                    for filter_field in filters_field:
                        comparator = filter_field["comparator"]
                        field_comparator = "'" + field_data + "'"

                        if str(filter_field["value"]).isnumeric():
                            field_comparator = Utils.only_numbers(field_comparator)

                        if eval("{} {} {}".format(field_comparator, comparator, filter_field["value"])) is False:
                            remove_machine = True

                    if remove_machine is True:
                        break

                    item[field] = field_data

                if remove_machine is False:
                    items[machine_key] = item
            result[collection_name] = items

        return result

    def extract_pricing(self, field_data):
        pricing_obj = {}
        for price_key in field_data:
            price_obj = field_data[price_key]
            pricing_obj[price_key] = {}

            if isinstance(price_obj, dict):
                for type_price_key in price_obj:
                    type_price = price_obj[type_price_key]
                    pricing_obj[price_key][type_price_key] = Utils.get_price(type_price)
            else:
                pricing_obj[price_key]['price'] = Utils.get_price(price_obj)

        return pricing_obj


api.add_resource(Prices, '/')

if __name__ == '__main__':
    app.run(debug=True)
