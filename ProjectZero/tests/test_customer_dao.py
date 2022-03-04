"""this module contains customer data object testing code"""
from custom_exceptions.record_not_found import RecordNotFound
from data_layer.dao_package.account_dao import AccountDao
from data_layer.dao_package.customer_dao import CustomerDao

test_customer_object = CustomerDao()
test_account_dao = AccountDao()
test_customer_1 = test_customer_object.create_customer(0, "first", "last")

# positive test


def test_create_customer_success():
    result = test_customer_object.create_customer(0, "matt", "bananas")
    assert result.customer_id != 0


def test_get_customer_by_id_success():
    result = test_customer_object.get_customer_by_id(2)
    assert result.customer_id == 2


def test_get_customer_by_id_record_not_found():
    try:
        result = test_customer_object.get_customer_by_id(0)
    except RecordNotFound as e:
        assert str(e) == "Customer record not found."


def test_update_customer_first_name_success():
    result = test_customer_object.update_customer(1, "matt", "last")
    assert result.first_name != "first"


def test_update_customer_last_name_success():
    result = test_customer_object.update_customer(1, "first", "bananas")
    assert result.last_name != "last"


def test_delete_customer_by_id_success():
    result = test_customer_object.delete_customer_by_id(1)
    assert result


def test_delete_customer_by_id_record_not_found():
    try:
        result = test_customer_object.delete_customer_by_id(1000)
    except RecordNotFound as e:
        assert str(e) == "Customer record not found."
