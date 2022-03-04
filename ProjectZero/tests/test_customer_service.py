"""this module contains test for the service layer customer interactions"""
from custom_exceptions.incorrect_data_field import IncorrectDataField
from custom_exceptions.string_too_long import StringTooLong
from data_layer.dao_package.customer_dao import CustomerDao
from service_layer.servie_layer_package.customer_service_implementation import CustomerSlImp

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


def test_delete_customer_by_id_non_int():
    try:
        result = test_customer_object.sl_delete_customer_by_id(2.0)
    except IncorrectDataField as e:
        assert str(e) == "The customer id must be an integer."

