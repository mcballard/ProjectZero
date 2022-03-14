"""this module contains test for the account data object"""
from unittest import mock
from unittest.mock import patch, MagicMock

from custom_exceptions.negative_balance import NegativeBalance
from custom_exceptions.record_not_found import RecordNotFound
from data_layer.dao_package.account_dao import AccountDao

account_dao_test_object = AccountDao()

# positive tests


def test_create_account_success():
    result = account_dao_test_object.create_account(-1, 4, 1000)
    assert result.account_id != -1


def test_get_account_info_by_id_success():
    account_dao_test_object.get_account_info_by_id = MagicMock(result_value=True)
    result = account_dao_test_object.get_account_info_by_id(7)
    assert result


def test_get_all_account_info_by_customer_id_success():
    id_check = False
    result = account_dao_test_object.get_all_accounts_by_customer_id(4)
    for i in result:
        if i.customer_id == 4:
            id_check = True
        else:
            id_check = False
    assert id_check


def test_update_account_by_id_success():
    account_dao_test_object.update_account_by_id = MagicMock(return_value=7)
    result = account_dao_test_object.update_account_by_id(7, 100)
    assert result == 7


# will fail unless updated with valid id
def test_delete_account_by_id_success():
    account_dao_test_object.delete_account_by_id = MagicMock(return_value=True)
    is_removed = account_dao_test_object.delete_account_by_id(1)
    assert is_removed is True

# negative tests
"""
@patch("stubs_and_mocks.Divider.division")

    mock.side_effect = ZeroDivisionError() # use .side_effect = Exception() to actually raise the exception you want
    result = calculator.even_odd_check(10) #number does not matter: when the division method is called it will raise our ZeroDivisionError Exception
    assert result == "You can't divide by 0, please try again"


so far we have been stubbing our methods, however, we sometimes will need to test not the results of a method, but
the inputs, or path of execution, to the method. In these cases we want to do mocking


def test_make_sure_input_gets_to_division_method():
    calculator.divider_object.division = MagicMock(return_value=5) # it is good practice to return the expected value
    calculator.even_odd_check(10)
    calculator.divider_object.division.assert_called_with(10)

"""


@patch("tests.test_account_dao.account_dao_test_object.create_account")
def test_create_account_negative_balance(mock):
    mock.side_effect = NegativeBalance("Cannot have negative account balance.")
    try:
        result = account_dao_test_object.create_account(0, 1, -1)
        assert False
    except NegativeBalance as e:
        assert str(e) == "Cannot have negative account balance."


@patch("tests.test_account_dao.account_dao_test_object.get_account_info_by_id")
def test_get_record_by_id_record_not_found(mock):
    mock.side_effect = RecordNotFound("Record not found.")
    try:
        result = account_dao_test_object.get_account_info_by_id(8000)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Record not found."


@patch("tests.test_account_dao.account_dao_test_object.get_all_accounts_by_customer_id")
def test_get_all_records_by_id_no_records_found(mock):
    mock.side_effect = RecordNotFound("No accounts for this customer found.")
    try:
        result = account_dao_test_object.get_all_accounts_by_customer_id(1000)
    except RecordNotFound as e:
        assert str(e) == "No accounts for this customer found."


@patch("tests.test_account_dao.account_dao_test_object.delete_account_by_id")
def test_delete_record_by_id_record_not_found(mock):
    mock.side_effect = RecordNotFound("Record not found.")
    try:
        result = account_dao_test_object.delete_account_by_id(1000)
        assert False
    except RecordNotFound as e:
        assert str(e) == "Record not found."
