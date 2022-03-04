"""this module will contain the rest functionality for the project"""
from flask import Flask, request, jsonify

from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.record_not_found import RecordNotFound
from custom_exceptions.string_too_long import StringTooLong
from data_entities.account import Account
from data_entities.customer import Customer
from data_layer.dao_package.account_dao import AccountDao
from data_layer.dao_package.customer_dao import CustomerDao
from service_layer.service_layer_package.account_service_implementation import AccountSlImp
from service_layer.service_layer_package.customer_service_implementation import CustomerSlImp

"""installed flask api from pypi"""

"""
nested_dict = { 'dictA': {'key_1': 'value_1'},
                'dictB': {'key_2': 'value_2'}}

print(nested_dict)
"""

app: Flask = Flask(__name__)

customer_data_layer_object = CustomerDao()
customer_service_layer_object = CustomerSlImp(customer_data_layer_object)
accounts_data_layer_object = AccountDao()
accounts_service_layer_object = AccountSlImp(accounts_data_layer_object)


@app.route("/customer/create", methods=["POST"])
def create_customer():
    try:
        customer_data: dict = request.get_json()
        new_customer = Customer(0, customer_data["firstName"], customer_data["lastName"])
        result = customer_service_layer_object.sl_create_customer(new_customer.first_name, new_customer.last_name)
        result_dictionary = result.convert_to_dictionary_json_friendly()
        result_json = jsonify(result_dictionary)
        return result_json, 201
    except IncorrectDataField as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400
    except RecordNotFound as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400


@app.route("/customer/<customer_id>/info", methods=["GET"])
def get_customer(customer_id: str):
    try:
        sanitized_id = customer_service_layer_object.sl_check_for_int_convertible_arg(customer_id)
        customer_info = customer_service_layer_object.sl_get_customer_by_id(sanitized_id)
        customer_dictionary = customer_info.convert_to_dictionary_json_friendly()
        return jsonify(customer_dictionary), 200
    except IncorrectDataField as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400
    except RecordNotFound as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400


@app.route("/customer/<customer_id>/update", methods=["POST"])
def update_customer(customer_id: str):
    try:
        sanitized_id = customer_service_layer_object.sl_check_for_int_convertible_arg(customer_id)
        customer_data: dict = request.get_json()
        updated_customer = customer_service_layer_object.sl_update_customer_by_id(sanitized_id,
                                                                                  customer_data["firstName"],
                                                                                  customer_data["lastName"])
        result_dictionary = updated_customer.convert_to_dictionary_json_friendly()
        return jsonify(result_dictionary), 200
    except IncorrectDataField as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400
    except RecordNotFound as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400
    except StringTooLong as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400


@app.route("/customer/<customer_id>/delete", methods=["GET"])
def delete_customer(customer_id: str):
    try:
        sanitized_id = customer_service_layer_object.sl_check_for_int_convertible_arg(customer_id)
        customer_deleted_bool = customer_service_layer_object.sl_delete_customer_by_id(sanitized_id)
        return "Customer record removed is " + str(customer_deleted_bool), 200
    except IncorrectDataField as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400
    except RecordNotFound as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400


@app.route("/customer/<customer_id>/accounts/create", methods=["POST"])
def create_customer_account(customer_id: str):
    try:
        account_data: dict = request.get_json()
        sanitized_id = customer_service_layer_object.sl_check_for_int_convertible_arg(customer_id)
        sanitized_balance = customer_service_layer_object.sl_check_for_float_convertible_arg(account_data["accountBalance"])
        # attempt to retrieve customer to trigger record not found to prevent non customers from creating accounts
        check_for_existing_customer = customer_service_layer_object.sl_get_customer_by_id(sanitized_id)
        new_account = Account(0, sanitized_id, sanitized_balance)
        result = accounts_service_layer_object.sl_create_account(new_account.customer_id, new_account.account_balance)
        result_dictionary = result.convert_to_dictionary_json_friendly()
        result_json = jsonify(result_dictionary)
        return result_json, 201
    except IncorrectDataField as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400
    except RecordNotFound as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400


@app.route("/customer/<customer_id>/accounts/<account_id>/info", methods=["GET"])
def get_customer_account(customer_id: str, account_id: str):
    try:
        sanitized_account_id = customer_service_layer_object.sl_check_for_int_convertible_arg(account_id)
        account_info = accounts_service_layer_object.sl_get_account_info_by_id(sanitized_account_id)
        account_dictionary = account_info.convert_to_dictionary_json_friendly()
        return jsonify(account_dictionary), 200
    except IncorrectDataField as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400
    except RecordNotFound as e:
        message = {
            "message": str(e)
        }
        return jsonify(message), 400

"""
@app.route("/customer/<customer_id>/accounts/update", methods=["POST"])
def update_customer_account():
    pass


@app.route("/customer/<customer_id>/accounts/delete", methods=["POST"])
def delete_customer_account():
    pass
"""

app.run()
