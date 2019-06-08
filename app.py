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
        filters = form.data['filters']
        labels = form.data['labels']
        limit = form.data['limit']
        price_label = ''
        items = []

        for collection_name in collections:
            last_data = list(mongo.find_last(collection_name))[0]
            fields = form.data['select'].get(collection_name, [])

            del last_data['_id']
            for machine_key in last_data:
                machine = last_data[machine_key]
                price_configurations = []
                general_configurations = {'type': machine_key, 'cloud': collection_name}

                """ Montando o objeto """
                for index, field_list in enumerate(fields):
                    field_split = str(field_list).split('.')
                    field = field_split[0]
                    field_data = machine.get(field, None)

                    if 'pricing' in field:
                        price_configurations = self.extract_pricing(field_data, field_split[1])
                        price_label = labels[index]
                    else:
                        general_configurations[labels[index]] = field_data

                items = items + [{**general_configurations, price_label: {**x}} for x in price_configurations]

        # Ordenando a lista pelos valores
        items.sort(key=lambda elem: elem[price_label]['price'])

        """ Realizando a filtragem dos resultados """
        list_filtered = []
        has_filter = False

        for filter_obj in filters:
            items_to_remove = []
            has_filter = True

            for item in items:
                field_filter = filter_obj["field"]
                comparator = filter_obj["comparator"]
                value_filter = filter_obj["value"]

                field_data = "'" + str(item.get(field_filter, '')) + "'"

                # Removendo . caso seja um número decimal
                if str(value_filter).replace('.', '').isnumeric():
                    field_data = Utils.only_numbers(field_data)
                else:
                    # Se não for um número, adicionar " para considerar como string na hora do eval
                    value_filter = '"' + value_filter + '"'

                if eval("{} {} {}".format(field_data, comparator, value_filter)) is True:
                    list_filtered.append(item)

            for item in items_to_remove:
                del items[item]

        if has_filter is True:
            items = list_filtered

        if limit is not None:
            items = items[:limit]

        return items

    def extract_pricing(self, field_data, field_name):
        pricing_obj = []

        if field_data is None:
            return []

        for price_key in field_data:
            price_obj = field_data[price_key]

            if isinstance(price_obj, dict):
                type_price = price_obj.get(field_name, '0')
                price = Utils.get_price(type_price)

                if price != 0:
                    pricing_obj.append({"region": price_key, "price": price})
            else:
                price = Utils.get_price(price_obj)
                if price != 0:
                    pricing_obj.append({"region": price_key, "price": price})

        return pricing_obj


api.add_resource(Prices, '/')

if __name__ == '__main__':
    app.run(debug=True)
