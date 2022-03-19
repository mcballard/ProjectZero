from flask import Flask, request, jsonify

from custom_exceptions.incomplete_column_dictionary import IncompleteColumnDictionary
from data_entities.testing_implemented_table_object import TestRowObject
from data_layer.dao_package.testing_db_access_object import TestingDBAccessObject
from service_layer.service_layer_package.testing_service_layer_object import TestServiceLayerImplementation

testing_db_access_object = TestingDBAccessObject()
testing_service_layer_object = TestServiceLayerImplementation(testing_db_access_object)

app: Flask = Flask(__name__)


@app.route("/table_row_object", methods=["POST"])
def create_table_row_object():
    try:
        table_row_data: dict = request.get_json()
        sanitized_table_row_data = testing_service_layer_object.sanitize_json_from_api(table_row_data)
        table_row_to_create = TestRowObject(sanitized_table_row_data)
        new_table_row_in_db = testing_service_layer_object.create_record_business_logic_data_manipulation(table_row_to_create)
        response_table_data = jsonify(new_table_row_in_db)
        return response_table_data, 201
    except IncompleteColumnDictionary as e:
        message = {
            str(e)
        }
        return jsonify(message), 400

