"""this module contains test for the account data object"""
from custom_exceptions.negative_balance import NegativeBalance
from custom_exceptions.record_not_found import RecordNotFound
from data_layer.dao_package.account_dao import AccountDao

account_dao_test_object = AccountDao()

# positive tests


def test_create_account_success():
    result = account_dao_test_object.create_account(-1, 4, 1000)
    assert result.account_id != -1


def test_get_account_info_by_id_success():
    result = account_dao_test_object.get_account_info_by_id(1)
    assert result


def test_get_all_account_info_by_customer_id_success():
    id_check = False
    result = account_dao_test_object.get_all_accounts_by_customer_id(1)
    for i in result:
        if i.customer_id == 1:
            id_check = True
        else:
            id_check = False
    assert id_check


def test_update_account_by_id_success():
    result = account_dao_test_object.update_account_by_id(1, 100)
    assert result.account_id == 1


# will fail unless updated with valid id
def test_delete_account_by_id_success():
    is_removed = account_dao_test_object.delete_account_by_id(1)
    assert is_removed is True


# negative tests
def test_create_account_negative_balance():
    try:
        result = account_dao_test_object.create_account(4, 0, -1)
        assert False
    except NegativeBalance as e:
        assert str(e) == "Cannot have negative account balance."


def test_get_record_by_id_record_not_found():
    try:
        result = account_dao_test_object.get_account_info_by_id(8000)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."


def test_get_all_records_by_id_no_records_found():
    try:
        result = account_dao_test_object.get_all_accounts_by_customer_id(1000)
    except RecordNotFound as e:
        assert str(e) == "No records found."


def test_delete_record_by_id_record_not_found():
    try:
        result = account_dao_test_object.delete_account_by_id(1000)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Could not find record in database."
