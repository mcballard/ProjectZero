"""this module contains test for the service layer customer interactions"""
from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.record_not_found import RecordNotFound
from custom_exceptions.string_too_long import StringTooLong
from data_layer.dao_package.customer_dao import CustomerDao
from service_layer.service_layer_package.customer_service_implementation import CustomerSlImp

test_customer_dao = CustomerDao()
test_customer_object = CustomerSlImp(test_customer_dao)
test_customer_1 = test_customer_dao.create_customer(0, "first", "last")


def test_create_customer_non_string_first_name():
    try:
        result = test_customer_object.sl_create_customer(4, "this")
    except IncorrectDataField as e:
        assert str(e) == "The name value must be a string."


def test_create_customer_non_string_last_name():
    try:
        test_customer_object.sl_create_customer("this", 4)
    except IncorrectDataField as e:
        assert str(e) == "The name value must be a string."


def test_create_customer_first_name_over_twenty():
    try:
        test_customer_object.sl_create_customer("this is a really ridiculously long name", "this")
    except StringTooLong as e:
        assert str(e) == "The name value must be a string less than 20 characters."


def test_create_customer_last_name_over_twenty():
    try:
        test_customer_object.sl_create_customer("this", "this is a really ridiculously long name")
    except StringTooLong as e:
        assert str(e) == "The name value must be a string less than 20 characters."


def test_get_customer_by_id_non_int():
    try:
        result = test_customer_object.sl_get_customer_by_id(1.0)
    except IncorrectDataField as e:
        assert str(e) == "The customer id must be an integer."


def test_update_customer_non_string_first_name():
    try:
        result = test_customer_object.sl_update_customer_by_id(0, 4, "change")
    except IncorrectDataField as e:
        assert str(e) == "The name value must be a string."


def test_update_customer_non_string_last_name():
    try:
        result = test_customer_object.sl_update_customer_by_id(0, "this", 4)
    except IncorrectDataField as e:
        assert str(e) == "The name value must be a string."


def test_update_customer_first_name_over_twenty():
    try:
        result = test_customer_object.sl_update_customer_by_id(0, "this is a really ridiculously long name", "this")
    except StringTooLong as e:
        assert str(e) == "The name value must be a string less than 20 characters."


def test_update_customer_last_name_over_twenty():
    try:
        result = test_customer_object.sl_update_customer_by_id(0, "this", "this is a really ridiculously long name")
    except StringTooLong as e:
        assert str(e) == "The name value must be a string less than 20 characters."


def test_check_for_int_convertible_id_success():
    new_id = test_customer_object.sl_check_for_int_convertible_arg("1")
    assert type(new_id) == int


def test_check_for_float_convertible_id_is_non_convertible():
    try:
        new_id = test_customer_object.sl_check_for_int_convertible_arg("not convertible")
    except IncorrectDataField as e:
        assert str(e) == "The input from the api is not convertible to integer."


def test_check_for_float_convertible_id_success():
    new_id = test_customer_object.sl_check_for_float_convertible_arg("1")
    assert type(new_id) == float


def test_check_for_float_convertible_is_non_convertible():
    try:
        new_id = test_customer_object.sl_check_for_float_convertible_arg("not convertible")
    except IncorrectDataField as e:
        assert str(e) == "The input from the api is not convertible to float."


def test_delete_customer_by_id_record_not_found():
    try:
        return_value = test_customer_object.sl_delete_customer_by_id(1000)
    except RecordNotFound as e:
        assert str(e) == "Customer record not found."
